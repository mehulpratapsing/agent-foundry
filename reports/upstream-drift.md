# Upstream drift report

Checked: 2026-11-09 18:56 UTC

This report identifies upstream commits newer than the reviewed pins in `sources.json`. It does **not** change pins, enable tools, or install code. Review upstream changes, licenses, compatibility, and security before updating the manifest.

| Source | Status | Reviewed pin | Current default-branch head |
|---|---|---|---|
| [Everything Claude Code](https://github.com/affaan-m/ECC) | workflow-pack | `90606c8315ee09cafc303515c5f33024db6b9882` | [`d2ef2680594f9a17526a6e1a2e18b3d242c5d17b`](https://github.com/affaan-m/ECC/commit/d2ef2680594f9a17526a6e1a2e18b3d242c5d17b) |
| [Superpowers](https://github.com/obra/superpowers) | workflow-pack | `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b` | [`22f0b463e7a5e579904dd6211a520321035526f7`](https://github.com/obra/superpowers/commit/22f0b463e7a5e579904dd6211a520321035526f7) |
| [Context7](https://github.com/upstash/context7) | mcp | `b5e81de845092694ba1bfc5af15400f319c89b6d` | [`6e68ffcbad0e23cf4fa8c11795ce9e551aeef19b`](https://github.com/upstash/context7/commit/6e68ffcbad0e23cf4fa8c11795ce9e551aeef19b) |
| [Agent Reach](https://github.com/Panniantong/Agent-Reach) | research-tool | `beabda7486e9a666360b18cdb5c0e759c2c4d20f` | [`c70ae6da5d39bc90e09ad2ae0575ccc89f31e284`](https://github.com/Panniantong/Agent-Reach/commit/c70ae6da5d39bc90e09ad2ae0575ccc89f31e284) |
| [Graphify](https://github.com/Graphify-Labs/graphify) | codebase-tool | `92741d162b2094ffc2fed58cfbd8ee823e9da62c` | [`5eedffa87476a063a05bed96f17275ed63f05c1a`](https://github.com/Graphify-Labs/graphify/commit/5eedffa87476a063a05bed96f17275ed63f05c1a) |
| [Strix](https://github.com/usestrix/strix) | security-tool | `14cc948c36e90517a774cf32bdfe5d8cd3605b62` | [`215482eb2204cd30ac6b87520e3f5c6511e2e2e8`](https://github.com/usestrix/strix/commit/215482eb2204cd30ac6b87520e3f5c6511e2e2e8) |
| [ponytail](https://github.com/DietrichGebert/ponytail) | workflow-pack | `09c434ab73ca43761c5d8b0c5d341926c2fba710` | [`96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`](https://github.com/DietrichGebert/ponytail/commit/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846) |
| [gstack](https://github.com/garrytan/gstack) | workflow-pack | `6f7488a70f23bc71745bde704eda98033cc33bfa` | [`f75ce6fdcc14e6398b00645c1608e834d766a922`](https://github.com/garrytan/gstack/commit/f75ce6fdcc14e6398b00645c1608e834d766a922) |
| [Firecrawl](https://github.com/firecrawl/firecrawl) | research-tool | `5228ce8ac720c321374a7ad4f6eebb9eba2d3072` | [`474524586521df68d58940a4eed3ecbb1d256670`](https://github.com/firecrawl/firecrawl/commit/474524586521df68d58940a4eed3ecbb1d256670) |
| [claude-mem](https://github.com/thedotmack/claude-mem) | memory-tool | `73d86abd2617d3f5057f79cacf2aed562f52cf2b` | [`a926f57d18ee0040d6b0e5107f847ad6dacc8cb9`](https://github.com/thedotmack/claude-mem/commit/a926f57d18ee0040d6b0e5107f847ad6dacc8cb9) |
| [awesome-opencode](https://github.com/awesome-opencode/awesome-opencode) | discovery-catalog | `bcc5c03cec19789b45ef9af4a969e3fe3fd7431b` | [`a23b18eda5d062288cc3ba8f775cc6756dd77df7`](https://github.com/awesome-opencode/awesome-opencode/commit/a23b18eda5d062288cc3ba8f775cc6756dd77df7) |

## Review checklist

- Read upstream release notes and the commit range.
- Confirm the current license and any compatibility changes.
- Decide explicitly whether to update the reviewed pin or enabled status.
- Update `last_reviewed` only after human review.
