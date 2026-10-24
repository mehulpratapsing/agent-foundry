# Runtime verification report

Run date: 2026-10-24 (local date, Asia/Kolkata)

This report separates static compatibility checks from observed runtime behavior. PASS means the command or behavior was observed in this run. A vendored source snapshot or valid config file alone is not a runtime pass.

## Environment observed

- OS: Microsoft Windows 11 Pro (PowerShell 7.6.5).
- OpenCode: 1.19.3.
- Codex CLI: 0.163.0-alpha.11.
- Python: 3.15.0.
- Git: 2.55.0.windows.5.
- Installed locally: OpenCode, Codex CLI. Not found: Graphify CLI, `uv`, Strix CLI, Docker, Claude Code, Gemini CLI, Cursor, Aider, Cline, Roo, Qwen Code, Zed, Amazon Q, Continue.
- No credential values were printed or stored in this report. Optional-provider key presence was not inspected.

## Static and repository checks

| Status | Check and exact command | Evidence / limitation |
|---|---|---|
| **PASS** | `python scripts/generate_adapters.py --check` | All 15 generated instruction/config adapters match `AGENTS.md` and the logical Context7 definition. |
| **PASS** | `python scripts/verify_toolkit.py --static` | Confirmed 11 source pins have full commit IDs and license metadata; source directories match the manifest; complete protocol is 30,696 bytes and below the documented 32 KiB Codex budget; six profiles point to existing directories; Context7 alone is enabled in the OpenCode base; five local skills have valid unique names; generated files have no drift; no credential-shaped strings were detected in checked files; offline upstream manifest/profile check passed. |
| **PASS** | `python -m unittest discover -s tests -v` | 5 repository regression tests passed from the test root after adding package markers so standard recursive discovery works. |
| **PASS** | `python scripts/verify_toolkit.py --opencode` | Root config and all six profiles resolved with OpenCode 1.19.3. Each profile kept the Context7 base and exposed skill files from its configured paths; all five `.agents/skills` workflows were discovered. This validates loading and paths, not every skill's external runtime dependencies. |

The canonical full protocol is in `AGENTS.md`. A harmless prompt in each installed harness returned exactly `# 17. NON-NEGOTIABLE BEHAVIOR`, confirming that the end of the file was loaded rather than only an opening summary. This does not imply all harness-specific secondary features are active.

## Live documentation and harness checks

| Status | Workflow | Exact non-secret command / query | Observed result |
|---|---|---|---|
| **PASS** | OpenCode instruction smoke | `opencode run --format json --model opencode/glm-5.3-flash-free "According to the root AGENTS.md, return only the exact title of section 17. Do not use tools."` | Returned `# 17. NON-NEGOTIABLE BEHAVIOR`. |
| **PASS** | Codex instruction smoke | `codex exec --ephemeral -C . -s read-only --json "Read the project instruction chain. Return only the exact Markdown title of section 17 from the root AGENTS.md. Do not use tools or modify files."` | Returned `# 17. NON-NEGOTIABLE BEHAVIOR`. Codex emitted non-fatal warnings about unrelated user-installed skill icons and PowerShell shell snapshots. |
| **PASS** | OpenCode Context7 discovery | `opencode mcp list` | Listed one server, `context7`, as `connected` at `https://mcp.context7.com/mcp`. Listing alone is not treated as a docs-fetch pass. |
| **PASS with version limitation** | Live Context7 request through OpenCode | `opencode run --format json --model opencode/glm-5.3-flash-free "Use Context7 MCP only. Resolve the Python requests library at version 2.32.3, then fetch its docs for a GET request with a timeout. Return the resolved library identifier, whether that exact version is indexed, and one supported usage detail. Do not use other tools."` | Context7 resolved `/psf/requests` and returned actual docs for GET timeouts. It did **not** index requested 2.32.3; the only versioned identifier shown was `v2.32.0`. Docs state `requests.get(url, timeout=5)` applies a combined connect/read timeout and a tuple sets them separately. |
| **BLOCKED** | Graphify CLI and bounded fixture smoke | `Get-Command uv, graphify -ErrorAction SilentlyContinue` (both absent); upstream README installation reviewed. | No CLI or `uv` is installed, so no graph artifact was created. The pinned Graphify README documents Python >=3.10 and `uv tool install graphifyy`, followed by `graphify install`. Next step: install the optional runtime in an approved environment, then run it only on a small non-sensitive fixture and verify its generated graph. The source snapshot is not an installation. |
| **BLOCKED** | Strix configuration and authorized local test | `Get-Command strix, docker -ErrorAction SilentlyContinue` (both absent); pinned Strix README and skill prerequisites reviewed. | Strix and Docker are absent. No scan was run; no target was selected. Next step: install/configure Strix and Docker, provide the chosen LLM provider's key through the provider's documented environment variable, and explicitly scope an intentionally vulnerable local fixture before exercising a scan. |

The OpenCode live requests used a public library and did not send repository source. Context7's `v2.32.0` result is evidence of a completed fetch, not of the exact requested `2.32.3` version.

## Profile status

All six selectable profiles were parsed by OpenCode, and their referenced paths and discovered skills were checked. Where a harmless text-only skill exercise was possible, it was also run:

| Profile | Skill source | Status | Runtime limits |
|---|---|---|---|
| `ecc` | `upstream/ecc/skills` | **PASS: config/discovery and safe skill smoke** | Ran the `api-design` skill on a hypothetical endpoint; it returned three validation checks and `201 Created`. No files or external services used. |
| `superpowers` | `upstream/superpowers/skills`, `upstream/ponytail/skills` | **PASS: config/discovery and safe skill smoke** | Ran the `systematic-debugging` skill against the observed zero-test discovery issue; it identified package markers and recommended the fresh test-root command. No files changed by the smoke. |
| `research` | Context7 skills, Agent Reach, Firecrawl skills | **PASS: config/discovery and Context7 smoke** | Live Context7 resolve + docs request succeeded under this profile for `/psf/requests`. Agent Reach and Firecrawl runtimes were not installed or exercised. |
| `security` | `upstream/strix/skills` | **PASS: config and discovery; runtime BLOCKED** | Strix execution **BLOCKED** by missing Strix CLI and Docker; no target was scanned. |
| `gstack` | `upstream/gstack` | **PASS: config and discovery; workflow NOT RUN** | The source skills require their gstack launcher and some use write-capable review/release workflows. The expected launcher and Autoplan publication hook are absent, so running one would not be a safe representative smoke. |
| `memory` | `upstream/claude-mem/plugin/skills` | **PASS: config/discovery and documentation smoke** | Ran the `how-it-works` skill in documentation-only mode. It summarized local storage and second-session injection from source text. No memory service was installed, queried, or written. |

The base remains selective: it enables Context7 only and selects no specialist skill pack. Profile loading is not the same as installing or running the upstream tool. Use one profile at a time and follow the component's own prerequisite/security guidance.

The four safe profile exercises used these commands (all model runs used `opencode/glm-5.3-flash-free`):

```powershell
.\scripts\opencode-profile.ps1 ecc run --format json --model opencode/glm-5.3-flash-free "Use the api-design skill to review this hypothetical endpoint contract: POST /api/v1/todos accepts a title string. Give three input checks and one appropriate success status code. Text only; do not inspect files, call external services, or modify anything."
.\scripts\opencode-profile.ps1 superpowers run --format json --model opencode/glm-5.3-flash-free "Use the systematic-debugging skill to explain this observed test-discovery issue, using only the facts given: python -m unittest discover -s tests -v originally reported 0 tests because the test directories lacked package markers. I added tests/__init__.py and tests/toolkit/__init__.py, then python -m unittest discover -s tests/toolkit -v ran 5 tests and passed. State root cause and the next verification command. Do not run commands or modify files."
.\scripts\opencode-profile.ps1 research run --format json --model opencode/glm-5.3-flash-free "Use Context7 only. Resolve the Python requests library, then retrieve one documented detail about requests.get timeout behavior. Return the library identifier and detail. Do not search the web, inspect repository files, or modify anything."
.\scripts\opencode-profile.ps1 memory run --format json --model opencode/glm-5.3-flash-free "Use the how-it-works skill to answer where claude-mem stores its local observations and when memory injection begins. Treat the profile as documentation only: do not install, launch, authenticate, query, or write to any memory service. Ground the answer in the skill text."
```

The outputs and remaining checks are captured in the [sanitized evidence log](verification-evidence-2026-10-24.md).

## Cross-harness status

OpenCode and Codex were the only installed harnesses, and both instruction-loading smoke tests passed. Other rows in [harness-compatibility.md](harness-compatibility.md) are static documentation/schema compatibility checks only; their runtimes were unavailable and are marked NOT RUN. No personal client MCP configuration was modified.

## Rerun commands

From the repository root in PowerShell:

```powershell
python scripts/generate_adapters.py --check
python scripts/verify_toolkit.py --static
python scripts/verify_toolkit.py --opencode
python -m unittest discover -s tests -v
opencode mcp list
```

The two model-backed instruction smoke prompts and Context7 query are written above so they can be repeated manually. Graphify and Strix remain blocked until their dependencies are available and a safe fixture is in scope.
