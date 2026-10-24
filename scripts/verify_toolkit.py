#!/usr/bin/env python3
"""Run read-only repository checks and optional OpenCode discovery checks."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROFILE_DIR = ROOT / "profiles"
SKILLS_DIR = ROOT / ".agents" / "skills"
CONTEXT7_URL = "https://mcp.context7.com/mcp"
ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
SECRET_SHAPE_RE = re.compile(r"(?:gh[pousr]_[A-Za-z0-9_]{25,}|sk-[A-Za-z0-9_-]{24,}|Bearer\s+[A-Za-z0-9._~-]{24,})")


def _powershell(command: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    executable = "pwsh" if _find_executable("pwsh") else "powershell"
    return subprocess.run(
        [executable, "-NoProfile", "-NonInteractive", "-Command", command],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def _find_executable(name: str) -> str | None:
    from shutil import which

    return which(name)


def run_opencode(*args: str, config: Path | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if config is not None:
        env["OPENCODE_CONFIG"] = str(config.resolve())
    if os.name == "nt":
        # The package installs a PowerShell shim on Windows; keep all arguments constant or safely quoted.
        def quote(value: str) -> str:
            return "'" + value.replace("'", "''") + "'"

        command = "& opencode " + " ".join(quote(value) for value in args)
        return _powershell(command, env)
    return subprocess.run(
        ["opencode", *args], cwd=ROOT, env=env, capture_output=True, text=True, timeout=120, check=False
    )


def parse_opencode_json(result: subprocess.CompletedProcess[str]) -> Any:
    if result.returncode != 0:
        raise ValueError("OpenCode exited with a nonzero status")
    output = ANSI_RE.sub("", result.stdout).strip()
    return json.loads(output)


def static_checks() -> list[str]:
    from generate_adapters import expected_files, validate_rendered

    passed: list[str] = []
    manifest = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1:
        raise ValueError("unsupported source manifest schema")
    sources = manifest.get("sources")
    if not isinstance(sources, list) or len(sources) != 11:
        raise ValueError("expected exactly the existing 11 upstream snapshots")
    listed_paths: set[str] = set()
    for source in sources:
        for key in ("id", "url", "pinned_commit", "license", "compatibility", "upstream_path"):
            if not source.get(key):
                raise ValueError(f"source entry is missing {key}")
        if not re.fullmatch(r"[0-9a-f]{40}", str(source["pinned_commit"])):
            raise ValueError(f"{source['id']} does not have a full pinned commit")
        listed_paths.add(str(source["upstream_path"]).replace("\\", "/").split("/")[1])
    actual_paths = {path.name for path in (ROOT / "upstream").iterdir() if path.is_dir()}
    if listed_paths != actual_paths:
        raise ValueError(f"source directory mismatch: missing={sorted(listed_paths - actual_paths)}, extra={sorted(actual_paths - listed_paths)}")
    passed.append("11 pinned sources, licenses, and snapshot directories align")

    protocol_path = ROOT / "AGENTS.md"
    protocol = protocol_path.read_text(encoding="utf-8")
    if protocol_path.stat().st_size >= 32 * 1024:
        raise ValueError("AGENTS.md exceeds Codex's documented default 32 KiB instruction budget")
    required = [
        "# UNIVERSAL AI EXECUTION PROTOCOL",
        "# 1. THE PRIMARY DIRECTIVE",
        "# 2. INTERPRET THE REQUEST",
        "# 3. PREFLIGHT: UNDERSTAND THE ENVIRONMENT",
        "# 4. SELECT TOOLS INTELLIGENTLY",
        "# 5. RESEARCH BEFORE IMPLEMENTATION",
        "# 6. CHOOSE THE RIGHT EXECUTION MODE",
        "# 7. ARCHITECTURE AND PLANNING",
        "# 8. IMPLEMENT THE REAL SOLUTION",
        "# 9. GIT, FILES, AND CHANGE MANAGEMENT",
        "# 10. TEST-DRIVEN VERIFICATION",
        "# 11. SECURITY AND TRUST BOUNDARIES",
        "# 12. PERFORMANCE, COST, AND CONTEXT EFFICIENCY",
        "# 13. ITERATE UNTIL THE ACCEPTANCE CRITERIA ARE MET",
        "# 14. DOCUMENTATION AND REPRODUCIBILITY",
        "# 15. FINAL ACCEPTANCE GATE",
        "# 16. REQUIRED FINAL RESPONSE",
        "# 17. NON-NEGOTIABLE BEHAVIOR",
    ]
    missing_sections = [heading for heading in required if heading not in protocol]
    if missing_sections:
        raise ValueError("AGENTS.md is missing required protocol sections: " + ", ".join(missing_sections))
    passed.append(f"complete canonical protocol present ({protocol_path.stat().st_size} bytes)")

    profiles = sorted(PROFILE_DIR.glob("*.json"))
    if {profile.stem for profile in profiles} != {"ecc", "gstack", "memory", "research", "security", "superpowers"}:
        raise ValueError("selectable profile set differs from the six documented profiles")
    for profile in profiles:
        config = json.loads(profile.read_text(encoding="utf-8"))
        skills = config.get("skills", [])
        paths = skills.get("paths", []) if isinstance(skills, dict) else skills
        if not paths or not isinstance(paths, list):
            raise ValueError(f"{profile.name} does not declare a skill source")
        for relative in paths:
            target = (ROOT / relative).resolve()
            if ROOT.resolve() not in target.parents or not target.is_dir():
                raise ValueError(f"{profile.name} has a missing or escaping skill path: {relative}")
    base = json.loads((ROOT / "opencode.json").read_text(encoding="utf-8"))
    if set(base.get("mcp", {})) != {"context7"} or not base["mcp"]["context7"].get("enabled"):
        raise ValueError("base OpenCode config must enable only the intended Context7 MCP server")
    if "skills" in base and base["skills"]:
        raise ValueError("base OpenCode config must not select a specialist profile")
    passed.append("OpenCode base and six selective profiles are structurally valid")

    skill_names: set[str] = set()
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            raise ValueError(f"skill is missing SKILL.md: {skill_dir.name}")
        body = skill_file.read_text(encoding="utf-8")
        if not body.startswith("---\n") or "\n---\n" not in body[4:]:
            raise ValueError(f"skill frontmatter is invalid: {skill_dir.name}")
        frontmatter = body.split("\n---\n", 1)[0]
        name = re.search(r"(?m)^name:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*$", frontmatter)
        description = re.search(r"(?m)^description:\s*(\S.*)$", frontmatter)
        if not name or name.group(1) != skill_dir.name or not description:
            raise ValueError(f"skill name or description is invalid: {skill_dir.name}")
        if name.group(1) in skill_names:
            raise ValueError(f"duplicate skill name: {name.group(1)}")
        skill_names.add(name.group(1))
    if len(skill_names) != 5:
        raise ValueError(f"expected five shared toolkit-authored skills, found {len(skill_names)}")
    passed.append("five shared Agent Skills have valid names and frontmatter")

    generated = expected_files()
    validate_rendered(generated)
    drift = [path.relative_to(ROOT).as_posix() for path, expected in generated.items() if not path.is_file() or path.read_text(encoding="utf-8") != expected]
    if drift:
        raise ValueError("generated adapter drift: " + ", ".join(drift))
    passed.append(f"{len(generated)} generated adapters and MCP templates match their sources")

    secret_files = [ROOT / "AGENTS.md", ROOT / "opencode.json", CONTEXT7_FILE(), *generated.keys()]
    for file in dict.fromkeys(secret_files):
        if file.exists() and SECRET_SHAPE_RE.search(file.read_text(encoding="utf-8", errors="replace")):
            raise ValueError(f"secret-shaped value found in {file.relative_to(ROOT).as_posix()}")
    passed.append("no credential-shaped strings found in canonical or generated configuration")

    checker = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_upstreams.py"), "--offline"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if checker.returncode != 0:
        raise ValueError("scripts/check_upstreams.py --offline failed")
    passed.append("existing offline upstream manifest/profile check passes")
    return passed


def CONTEXT7_FILE() -> Path:
    return ROOT / "adapters" / "mcp" / "context7.json"


def opencode_checks() -> list[str]:
    if not _find_executable("opencode"):
        raise ValueError("OpenCode CLI is not installed")
    passed: list[str] = []
    config = parse_opencode_json(run_opencode("debug", "config"))
    if set(config.get("mcp", {})) != {"context7"}:
        raise ValueError("OpenCode resolved config does not expose only Context7")
    passed.append("OpenCode root configuration resolves")

    for profile in sorted(PROFILE_DIR.glob("*.json")):
        resolved = parse_opencode_json(run_opencode("debug", "config", config=profile))
        if set(resolved.get("mcp", {})) != {"context7"}:
            raise ValueError(f"OpenCode profile {profile.stem} altered the intended base MCP server")
        discovered = parse_opencode_json(run_opencode("debug", "skill", "--pure", config=profile))
        if not isinstance(discovered, list):
            raise ValueError(f"OpenCode profile {profile.stem} returned an unexpected skill listing")
        configured = json.loads(profile.read_text(encoding="utf-8")).get("skills", [])
        paths = configured.get("paths", []) if isinstance(configured, dict) else configured
        local_locations: list[Path] = []
        for item in discovered:
            location = item.get("location")
            if not isinstance(location, str):
                continue
            try:
                local_locations.append(Path(location).resolve())
            except OSError:
                continue
        for relative in paths:
            source = (ROOT / relative).resolve()
            if not any(source == item or source in item.parents for item in local_locations):
                raise ValueError(f"OpenCode did not discover skills under {profile.stem}:{relative}")
        passed.append(f"OpenCode profile {profile.stem}: config resolves and skill paths are discovered")

    discovered = parse_opencode_json(run_opencode("debug", "skill", "--pure"))
    root_skills = []
    for item in discovered:
        location = item.get("location")
        if not isinstance(location, str):
            continue
        try:
            resolved = Path(location).resolve()
            resolved.relative_to(SKILLS_DIR.resolve())
            root_skills.append(item.get("name"))
        except (OSError, ValueError):
            continue
    expected = {path.name for path in SKILLS_DIR.iterdir() if path.is_dir()}
    if not expected.issubset(set(root_skills)):
        raise ValueError("OpenCode did not discover all shared toolkit-authored skills")
    passed.append("OpenCode discovers the shared .agents/skills toolkit workflows")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--static", action="store_true", help="run read-only repository checks")
    parser.add_argument("--opencode", action="store_true", help="inspect OpenCode config and discover all profiles/skills")
    args = parser.parse_args()
    if not args.static and not args.opencode:
        args.static = True
    try:
        if args.static:
            for result in static_checks():
                print("PASS static: " + result)
        if args.opencode:
            for result in opencode_checks():
                print("PASS opencode: " + result)
        return 0
    except (OSError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
