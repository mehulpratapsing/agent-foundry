# Sanitized verification evidence — 2026-10-24

This is a compact record of observed outputs. Session IDs, user paths outside the repository, credentials, and unrelated Codex warnings have been omitted.

## Versions and availability

```text
OpenCode: 1.19.3
Codex CLI: 0.163.0-alpha.11
Python: 3.15.0
Git: 2.55.0.windows.5
PowerShell: 7.6.5
OS: Microsoft Windows 11 Pro
Available relevant runtimes: OpenCode, Codex CLI
Not found: uv, graphify, strix, docker, claude, gemini, cursor, aider, cline, roo, qwen, zed, amazonq, continue
```

## Static checks and tests

Commands:

```text
python scripts/generate_adapters.py --check
python scripts/verify_toolkit.py --static
python -m unittest discover -s tests -v
python scripts/verify_toolkit.py --opencode
git diff --check
```

Observed results:

```text
Generated adapters match canonical sources: 15 files
PASS static: 11 pinned sources, licenses, and snapshot directories align
PASS static: complete canonical protocol present (30696 bytes)
PASS static: OpenCode base and six selective profiles are structurally valid
PASS static: five shared Agent Skills have valid names and frontmatter
PASS static: 15 generated adapters and MCP templates match their sources
PASS static: no credential-shaped strings found in canonical or generated configuration
PASS static: existing offline upstream manifest/profile check passes
Ran 5 tests ... OK
PASS opencode: OpenCode root configuration resolves
PASS opencode: OpenCode profile ecc: config resolves and skill paths are discovered
PASS opencode: OpenCode profile gstack: config resolves and skill paths are discovered
PASS opencode: OpenCode profile memory: config resolves and skill paths are discovered
PASS opencode: OpenCode profile research: config resolves and skill paths are discovered
PASS opencode: OpenCode profile security: config resolves and skill paths are discovered
PASS opencode: OpenCode profile superpowers: config resolves and skill paths are discovered
PASS opencode: OpenCode discovers the shared .agents/skills toolkit workflows
git diff --check: exit 0; only Git line-ending conversion notices for AGENTS.md and README.md
```

## Installed harnesses and live workflows

OpenCode instruction smoke:

```text
Command: opencode run --format json --model opencode/glm-5.3-flash-free "According to the root AGENTS.md, return only the exact title of section 17. Do not use tools."
Observed: # 17. NON-NEGOTIABLE BEHAVIOR
```

Codex instruction smoke:

```text
Command: codex exec --ephemeral -C . -s read-only --json "Read the project instruction chain. Return only the exact Markdown title of section 17 from the root AGENTS.md. Do not use tools or modify files."
Observed final agent_message: # 17. NON-NEGOTIABLE BEHAVIOR
```

Context7 live request:

```text
Discovery command: opencode mcp list
Observed: 1 server; context7 connected at https://mcp.context7.com/mcp
Request: Resolve Python requests at 2.32.3, then request docs for a GET request with a timeout.
Observed: Context7 called resolve-library-id and query-docs; resolved /psf/requests; only versioned variant shown was v2.32.0; returned requests.get(..., timeout=5) and requests.get(..., timeout=(3.05, 27)) examples from the Requests advanced docs.
Status: live fetch PASS; exact requested v2.32.3 unavailable in the returned version list.
```

Safe specialist profile exercises:

```text
ECC / api-design: returned required/type, non-empty, and length validation plus 201 Created for a hypothetical POST /api/v1/todos; no tools or writes.
Superpowers / systematic-debugging: loaded the skill and identified missing package markers as the unittest discovery root cause; recommended python -m unittest discover -s tests -v; no writes.
Research / Context7: resolved /psf/requests and retrieved actual timeout docs under the research profile.
Memory / how-it-works: loaded the local skill and described ~/.claude-mem storage and second-session injection; no memory service installed, queried, or written.
```

## Blocked or deliberately not run

```text
Graphify: uv and graphify commands not found; pip show produced no graphifyy package record. No fixture graph was generated. Next prerequisite: install uv or pipx and the optional Graphify runtime, then run against a small non-sensitive fixture.
Strix: strix and docker commands not found; pip show produced no strix-agent package record. No target was scanned. Next prerequisites: Strix CLI, Docker, a provider key supplied through the provider's documented environment mechanism, and explicit scope for an intentionally vulnerable local fixture.
gstack: source profile and skills were discovered. Expected ~/.claude/skills/gstack/bin/gstack-skill-start and autoplan/bin/phase-publication-hook were both absent, so no gstack workflow was run.
Security target: none selected or scanned.
Other harness runtimes: not installed, so instruction/MCP behavior not run locally. See docs/harness-compatibility.md for static support and file entry points.
```
