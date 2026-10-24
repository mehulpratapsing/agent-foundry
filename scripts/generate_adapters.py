#!/usr/bin/env python3
"""Generate native instruction adapters and Context7 MCP templates from canonical sources."""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
CONTEXT7 = ROOT / "adapters" / "mcp" / "context7.json"


def read_context7() -> dict[str, object]:
    data = json.loads(CONTEXT7.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("name") != "context7":
        raise ValueError("adapters/mcp/context7.json has an unsupported schema or server name")
    if data.get("transport") != "streamable-http" or not str(data.get("url", "")).startswith("https://"):
        raise ValueError("Context7 must use a secure streamable HTTP endpoint")
    if data.get("required_environment_variables") != [] or data.get("required_scopes") != []:
        raise ValueError("the public Context7 adapter must not require credentials or scopes")
    return data


def expected_files() -> dict[Path, str]:
    protocol = AGENTS.read_text(encoding="utf-8")
    c7 = read_context7()
    name, url = str(c7["name"]), str(c7["url"])
    protocol_marker = "<!-- Canonical protocol. Generated full copies and harness-specific imports are maintained by `python scripts/generate_adapters.py`; edit this file only. -->"
    if not protocol.startswith(protocol_marker):
        raise ValueError("AGENTS.md is missing its canonical-source marker")

    continue_rule = (
        "---\n"
        "name: toolkit-master-protocol\n"
        "description: Canonical engineering protocol for repository tasks.\n"
        "alwaysApply: true\n"
        "---\n\n"
        "<!-- Generated from AGENTS.md by python scripts/generate_adapters.py; do not edit. -->\n\n"
        + protocol
    )
    claude = (
        "<!-- Native Claude Code adapter. AGENTS.md stays canonical. Claude Code de-duplicates imported AGENTS.md. -->\n"
        "@AGENTS.md\n"
    )
    gemini = (
        "<!-- Native Gemini CLI adapter. Do not also add AGENTS.md to context.fileName; this import loads it. -->\n"
        "@./AGENTS.md\n"
    )

    mcp_templates: dict[str, str] = {
        "codex.config.toml": (
            "# Optional project-scoped Codex MCP adapter. Copy into .codex/config.toml only after review.\n"
            f'[{"mcp_servers." + name}]\nurl = "{url}"\nenabled = true\n'
        ),
        "claude.mcp.json": json.dumps(
            {"mcpServers": {name: {"type": "http", "url": url}}}, indent=2
        )
        + "\n",
        "gemini.settings.json": json.dumps(
            {"mcpServers": {name: {"httpUrl": url}}}, indent=2
        )
        + "\n",
        "cursor.mcp.json": json.dumps({"mcpServers": {name: {"url": url}}}, indent=2) + "\n",
        "vscode.mcp.json": json.dumps(
            {"servers": {name: {"type": "http", "url": url}}}, indent=2
        )
        + "\n",
        "cline.mcp.json": json.dumps(
            {"mcpServers": {name: {"type": "streamableHttp", "url": url}}}, indent=2
        )
        + "\n",
        "roo.mcp.json": json.dumps(
            {"mcpServers": {name: {"type": "streamable-http", "url": url}}}, indent=2
        )
        + "\n",
        "continue.mcp.yaml": (
            "name: Context7\n"
            "version: 0.0.1\n"
            "schema: v1\n"
            "mcpServers:\n"
            "  - name: Context7\n"
            "    type: streamable-http\n"
            f"    url: {url}\n"
        ),
    }

    return {
        ROOT / "opencode.json": json.dumps(
            {
                "$schema": "https://opencode.ai/config.json",
                "mcp": {name: {"type": "remote", "url": url, "enabled": True}},
            },
            indent=2,
        )
        + "\n",
        ROOT / "CLAUDE.md": claude,
        ROOT / "GEMINI.md": gemini,
        ROOT / ".github" / "copilot-instructions.md": protocol,
        ROOT / ".continue" / "rules" / "00-toolkit.md": continue_rule,
        ROOT / ".amazonq" / "rules" / "00-toolkit.md": protocol,
        ROOT / ".aider.conf.yml": "# Generated native Aider adapter; AGENTS.md remains canonical.\nread: AGENTS.md\n",
        ROOT / "adapters" / "mcp" / "templates" / "codex.config.toml": mcp_templates["codex.config.toml"],
        ROOT / "adapters" / "mcp" / "templates" / "claude.mcp.json": mcp_templates["claude.mcp.json"],
        ROOT / "adapters" / "mcp" / "templates" / "gemini.settings.json": mcp_templates["gemini.settings.json"],
        ROOT / "adapters" / "mcp" / "templates" / "cursor.mcp.json": mcp_templates["cursor.mcp.json"],
        ROOT / "adapters" / "mcp" / "templates" / "vscode.mcp.json": mcp_templates["vscode.mcp.json"],
        ROOT / "adapters" / "mcp" / "templates" / "cline.mcp.json": mcp_templates["cline.mcp.json"],
        ROOT / "adapters" / "mcp" / "templates" / "roo.mcp.json": mcp_templates["roo.mcp.json"],
        ROOT / "adapters" / "mcp" / "templates" / "continue.mcp.yaml": mcp_templates["continue.mcp.yaml"],
    }


def validate_rendered(files: dict[Path, str]) -> None:
    for path, body in files.items():
        if path.suffix == ".json":
            json.loads(body)
        elif path.suffix == ".toml":
            tomllib.loads(body)
    continue_mcp = files[ROOT / "adapters" / "mcp" / "templates" / "continue.mcp.yaml"]
    for required in ("name: Context7", "version: 0.0.1", "schema: v1", "type: streamable-http", "url: https://mcp.context7.com/mcp"):
        if required not in continue_mcp:
            raise ValueError(f"Continue MCP template is missing {required!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated files without writing")
    args = parser.parse_args()
    try:
        files = expected_files()
        validate_rendered(files)
        mismatches: list[str] = []
        for path, expected in files.items():
            if args.check:
                if not path.is_file() or path.read_text(encoding="utf-8") != expected:
                    mismatches.append(path.relative_to(ROOT).as_posix())
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(expected, encoding="utf-8", newline="\n")
        if args.check and mismatches:
            print("Generated adapter drift: " + ", ".join(mismatches), file=sys.stderr)
            return 1
        if args.check:
            print(f"Generated adapters match canonical sources: {len(files)} files")
        else:
            print(f"Generated native instruction and MCP adapters: {len(files)} files")
        return 0
    except (OSError, json.JSONDecodeError, tomllib.TOMLDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
