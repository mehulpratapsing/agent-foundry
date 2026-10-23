#!/usr/bin/env python3
"""Compare reviewed GitHub commit pins with current default-branch heads."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "sources.json"
DEFAULT_REPORT = ROOT / "reports" / "upstream-drift.md"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def load_manifest() -> list[dict[str, object]]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("sources"), list):
        raise ValueError("sources.json must have schema_version 1 and a sources array")
    sources = data["sources"]
    seen: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("each source must be an object")
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id or source_id in seen:
            raise ValueError(f"invalid or duplicate source id: {source_id!r}")
        seen.add(source_id)
        for field in ("name", "url", "default_branch", "license", "compatibility", "status"):
            if not isinstance(source.get(field), str) or not source[field]:
                raise ValueError(f"{source_id}: {field} must be a non-empty string")
        pinned = source.get("pinned_commit", "")
        if pinned and (not isinstance(pinned, str) or not SHA_RE.fullmatch(pinned)):
            raise ValueError(f"{source_id}: pinned_commit must be a full 40-character SHA or empty")
        if not isinstance(source.get("enabled"), bool):
            raise ValueError(f"{source_id}: enabled must be boolean")
    return sources


def github_repo(url: str) -> str:
    match = re.fullmatch(r"https://github\.com/([^/]+/[^/#?]+?)/?", url)
    if not match:
        raise ValueError(f"not a canonical GitHub repository URL: {url}")
    return match.group(1).removesuffix(".git")


def latest_commit(repo: str, branch: str, token: str | None) -> str:
    endpoint = f"https://api.github.com/repos/{repo}/commits/{branch}"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "curated-ai-engineering-toolkit"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(endpoint, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    sha = payload.get("sha")
    if not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
        raise ValueError(f"GitHub returned an invalid commit SHA for {repo}@{branch}")
    return sha


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="validate only; do not query GitHub")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT, help="Markdown report path")
    args = parser.parse_args()

    sources = load_manifest()
    print(f"Manifest valid: {len(sources)} sources")
    if args.offline:
        return 0

    token = os.environ.get("GITHUB_TOKEN")
    drift: list[tuple[dict[str, object], str]] = []
    failures: list[str] = []
    for source in sources:
        pinned = str(source.get("pinned_commit", ""))
        if not pinned:
            print(f"SKIP {source['id']}: no reviewed pin")
            continue
        try:
            repo = github_repo(str(source["url"]))
            current = latest_commit(repo, str(source["default_branch"]), token)
            if current != pinned:
                drift.append((source, current))
                print(f"DRIFT {source['id']}: {pinned[:12]} -> {current[:12]}")
            else:
                print(f"OK {source['id']}: {pinned[:12]}")
        except (ValueError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            failures.append(f"{source['id']}: {exc}")
            print(f"ERROR {source['id']}: {exc}", file=sys.stderr)

    if failures:
        return 2

    if not drift:
        args.report.unlink(missing_ok=True)
        print("No upstream drift detected.")
        return 0

    checked = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Upstream drift report",
        "",
        f"Checked: {checked}",
        "",
        "This report identifies upstream commits newer than the reviewed pins in `sources.json`. It does **not** change pins, enable tools, or install code. Review upstream changes, licenses, compatibility, and security before updating the manifest.",
        "",
        "| Source | Status | Reviewed pin | Current default-branch head |",
        "|---|---|---|---|",
    ]
    for source, current in drift:
        repo = github_repo(str(source["url"]))
        pinned = str(source["pinned_commit"])
        lines.append(
            f"| [{source['name']}]({source['url']}) | {source['status']} | `{pinned}` | [`{current}`](https://github.com/{repo}/commit/{current}) |"
        )
    lines.extend(["", "## Review checklist", "", "- Read upstream release notes and the commit range.", "- Confirm the current license and any compatibility changes.", "- Decide explicitly whether to update the reviewed pin or enabled status.", "- Update `last_reviewed` only after human review.", ""])
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote drift report: {args.report}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
