# Harness compatibility

Last reviewed: 2026-10-24. Documentation links below were checked on that date. “Supports” describes documented file or feature support; “tested” is limited to the local runtimes actually exercised and is listed separately.

## Canonical rules, local skills, and profile boundaries

- `AGENTS.md` is the single complete protocol and source of truth. `python scripts/generate_adapters.py` renders its native imports and any required full copies. `python scripts/generate_adapters.py --check` detects drift.
- The six toolkit-authored skills in `.agents/skills/` follow the Agent Skills `SKILL.md` format. They are shared where a harness explicitly supports that location and format; they are not copied into duplicate directories for harnesses that lack documented discovery.
- The six named specialist skill packs are OpenCode profiles only. In OpenCode, set `OPENCODE_CONFIG` to one file in `profiles/` using `scripts/opencode-profile.ps1 <profile> run ...`. Do not load ECC, Superpowers, and gstack together: they overlap. Other harnesses can use the local skills one task at a time, but the repository does not claim equivalent named profile support there.
- `adapters/mcp/context7.json` is the logical server record. Only the OpenCode root config currently activates Context7. Files under `adapters/mcp/templates/` are native configuration fragments for manual review and setup; their presence does not mean the corresponding harness is configured, connected, or tested. Credentials are not stored here.
- Copilot has a generated full `AGENTS.md` copy because some code-review surfaces accept `.github/copilot-instructions.md` but not `AGENTS.md`. A surface that loads both may see duplicated instructions; no universal deduplication behavior is claimed.

## Matrix

| Harness or surface | Instruction entry point | Shared `.agents/skills` | MCP entry | Local verification on 2026-10-24 |
|---|---|---|---|---|
| **OpenCode** | Root `AGENTS.md`; root wins if another instruction filename is also present. | Documented; six local skills discovered. | Active root `opencode.json`; Context7 only. | **PASS** OpenCode 1.19.3: root and six profile configs resolved; each profile's paths and skills discovered; section-17 instruction smoke and live Context7 fetch passed. |
| **Codex CLI** | Root `AGENTS.md`. | Documented shared skill format/path; runtime skill discovery not separately exercised. | Optional project-scoped fragment: `adapters/mcp/templates/codex.config.toml`; Codex project trust applies. | **PASS** Codex CLI 0.163.0-alpha.11: harmless section-17 instruction smoke returned the exact title. MCP was not configured or tested in Codex. |
| **Claude Code** | `CLAUDE.md` imports `@AGENTS.md`; `AGENTS.md` remains canonical. | Not advertised: Claude's documented native location is `.claude/skills/`, and duplicating these names would risk discovery conflicts with OpenCode. | Optional JSON fragment: `adapters/mcp/templates/claude.mcp.json`. | **NOT RUN** Claude Code was not installed. Import and MCP schemas were checked against official docs only. |
| **Gemini CLI** | `GEMINI.md` imports `@./AGENTS.md`; do not add the same file separately to `context.fileName`. | Documented shared path/format. | Optional settings fragment: `adapters/mcp/templates/gemini.settings.json`. | **NOT RUN** Gemini CLI was not installed. |
| **Cursor** | Root `AGENTS.md` is a native project instruction file. | Documented shared path/format. | Optional project fragment: `adapters/mcp/templates/cursor.mcp.json`. | **NOT RUN** Cursor was not installed. |
| **GitHub Copilot — VS Code Chat** | Root `AGENTS.md` and/or `.github/copilot-instructions.md`, depending on surface and VS Code version. | Documented shared path/format. | VS Code MCP fragment: `adapters/mcp/templates/vscode.mcp.json`. | **NOT RUN** No Copilot extension was found in the available VS Code CLI inventory. |
| **GitHub Copilot — VS Code code review** | Generated full `.github/copilot-instructions.md` copy. | Not assumed for code review. | The VS Code MCP file is not evidence the review service uses MCP. | **NOT RUN** No local review surface available. |
| **GitHub Copilot — CLI, cloud agent, GitHub.com** | Follow each surface's current support matrix; generated Copilot copy is provided, but do not infer identical AGENTS discovery across surfaces. | Cloud agent documents shared skills; other surfaces vary. | No active MCP config in this repository for these surfaces. | **NOT RUN** These surfaces were not available in this environment. |
| **Cline** | Generated common rules are available through `AGENTS.md` conventions; Cline-specific `.clinerules` is not duplicated. | Not advertised as an automatically discovered skill location. | Optional user-level template: `adapters/mcp/templates/cline.mcp.json`. | **NOT RUN** Cline was not installed. MCP fragment requires user-level placement per Cline docs. |
| **Roo Code** | Root `AGENTS.md` is supported; `.roo/rules/` is another native option. | Documented shared path/format. | Optional project fragment: `adapters/mcp/templates/roo.mcp.json`. | **NOT RUN** Roo was not installed. |
| **Continue** | Generated `.continue/rules/00-toolkit.md` with `alwaysApply: true`. | No shared Agent Skills discovery claimed. | Optional native YAML fragment: `adapters/mcp/templates/continue.mcp.yaml`. | **NOT RUN** Continue was not installed. |
| **Aider** | Generated `.aider.conf.yml` reads root `AGENTS.md`. | No shared skill or MCP support claimed. | No native MCP template claimed. | **NOT RUN** Aider was not installed. |
| **Amazon Q Developer** | Generated full `.amazonq/rules/00-toolkit.md` copy. | No shared skill support claimed. | No MCP integration claimed. | **NOT RUN** Amazon Q was not installed. |
| **Qwen Code** | Current docs describe root `AGENTS.md` support. | Only `.qwen/skills/` was verified; no duplicate skills generated. | No native fragment claimed. | **NOT RUN** Qwen Code was not installed. |
| **Zed** | Root `AGENTS.md` is supported as project instructions. | No shared Agent Skills support claimed. | No native fragment claimed. | **NOT RUN** Zed was not installed. |
| **Windsurf / legacy Cascade** | Compatibility is uncertain: the reviewed official legacy documentation redirects to Devin Desktop docs, which describe Devin Local. No Windsurf-specific rule file is generated. | Not claimed. | Not claimed. | **NOT RUN** Windsurf was not installed; legacy behavior could not be established from current official docs. |

## Harness-specific references

All links below are vendor documentation, not runtime test evidence.

- OpenCode: [rules](https://docs.opencode.ai/docs/rules/), [skills](https://docs.opencode.ai/docs/skills/), [configuration](https://docs.opencode.ai/docs/config/), [MCP servers](https://docs.opencode.ai/docs/mcp-servers/).
- Codex: [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).
- Claude Code: [memory and imports](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills), [MCP](https://code.claude.com/docs/en/mcp).
- Gemini CLI: [GEMINI.md](https://geminicli.com/docs/cli/gemini-md/), [skills](https://geminicli.com/docs/cli/skills/), [MCP](https://geminicli.com/docs/tools/mcp-server/).
- Cursor: [rules](https://cursor.com/docs/rules), [skills](https://cursor.com/docs/skills), [MCP](https://docs.cursor.com/context/model-context-protocol).
- GitHub Copilot: [custom instructions support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support), [cloud agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills); [VS Code MCP](https://developers.openai.com/learn/docs-mcp).
- Cline: [rules](https://docs.cline.bot/customization/cline-rules), [MCP](https://docs.cline.bot/mcp/mcp-overview).
- Roo Code: [custom instructions](https://roocodeinc.github.io/Roo-Code/features/custom-instructions/), [skills](https://roocodeinc.github.io/Roo-Code/features/skills/), [MCP](https://roocodeinc.github.io/Roo-Code/features/mcp/using-mcp-in-roo/).
- Continue: [rules](https://docs.continue.dev/customize/rules), [deep-dive rules](https://docs.continue.dev/customize/deep-dives/rules), [MCP](https://docs.continue.dev/customize/deep-dives/mcp).
- Aider: [conventions and read-only instruction files](https://aider.chat/docs/usage/conventions.html).
- Amazon Q: [project rules](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/context-project-rules.html).
- Qwen Code: [memory and AGENTS support](https://qwenlm.github.io/qwen-code-docs/en/users/features/memory/), [skills](https://qwenlm.github.io/qwen-code-docs/en/users/features/skills/).
- Zed: [AI instructions](https://zed.dev/docs/ai/instructions).
- Windsurf legacy documentation currently redirects to [Devin Desktop Cascade memories](https://docs.devin.ai/desktop/cascade/memories); that page is not treated as proof of legacy Windsurf compatibility.

## Manual MCP setup

Review a harness-specific fragment before copying it to that harness's documented configuration location. Do not copy these into a personal configuration without considering project trust, remote server policy, and whether the harness duplicates Context7 already. If a harness needs a key for increased quotas, pass it through its documented environment-variable mechanism; never write the value into the repository. Confirm connection in that harness before describing it as active.
