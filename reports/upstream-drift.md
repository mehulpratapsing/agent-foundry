# Upstream drift report

Checked: 2026-10-26 15:18 UTC

This report identifies upstream commits newer than the reviewed pins in `sources.json`. It does **not** change pins, enable tools, or install code. Review upstream changes, licenses, compatibility, and security before updating the manifest.

| Source | Status | Reviewed pin | Current default-branch head |
|---|---|---|---|
| [Everything Claude Code](https://github.com/affaan-m/ECC) | workflow-pack | `90606c8315ee09cafc303515c5f33024db6b9882` | [`25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b`](https://github.com/affaan-m/ECC/commit/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b) |
| [Context7](https://github.com/upstash/context7) | mcp | `b5e81de845092694ba1bfc5af15400f319c89b6d` | [`d9561600ad502cd72ab8bae4f9172f434aadf4d1`](https://github.com/upstash/context7/commit/d9561600ad502cd72ab8bae4f9172f434aadf4d1) |
| [Agent Reach](https://github.com/Panniantong/Agent-Reach) | research-tool | `beabda7486e9a666360b18cdb5c0e759c2c4d20f` | [`14c213405669414492bda0f8d52cc6531d062c45`](https://github.com/Panniantong/Agent-Reach/commit/14c213405669414492bda0f8d52cc6531d062c45) |
| [Strix](https://github.com/usestrix/strix) | security-tool | `14cc948c36e90517a774cf32bdfe5d8cd3605b62` | [`200a501f15a24a4152f92897a6b72af238ee69ef`](https://github.com/usestrix/strix/commit/200a501f15a24a4152f92897a6b72af238ee69ef) |
| [gstack](https://github.com/garrytan/gstack) | workflow-pack | `6f7488a70f23bc71745bde704eda98033cc33bfa` | [`5755601dac5d35ebd7dde181fdefe52a023c73d9`](https://github.com/garrytan/gstack/commit/5755601dac5d35ebd7dde181fdefe52a023c73d9) |
| [Firecrawl](https://github.com/firecrawl/firecrawl) | research-tool | `5228ce8ac720c321374a7ad4f6eebb9eba2d3072` | [`4c1e0d2aa15dd52ecc877630e58cf4d842701147`](https://github.com/firecrawl/firecrawl/commit/4c1e0d2aa15dd52ecc877630e58cf4d842701147) |
| [claude-mem](https://github.com/thedotmack/claude-mem) | memory-tool | `73d86abd2617d3f5057f79cacf2aed562f52cf2b` | [`7325fb7818ff7426665d85922db642ec0931bdcd`](https://github.com/thedotmack/claude-mem/commit/7325fb7818ff7426665d85922db642ec0931bdcd) |

## Review checklist

- Read upstream release notes and the commit range.
- Confirm the current license and any compatibility changes.
- Decide explicitly whether to update the reviewed pin or enabled status.
- Update `last_reviewed` only after human review.
