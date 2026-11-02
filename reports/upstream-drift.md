# Upstream drift report

Checked: 2026-11-02 18:32 UTC

This report identifies upstream commits newer than the reviewed pins in `sources.json`. It does **not** change pins, enable tools, or install code. Review upstream changes, licenses, compatibility, and security before updating the manifest.

| Source | Status | Reviewed pin | Current default-branch head |
|---|---|---|---|
| [Everything Claude Code](https://github.com/affaan-m/ECC) | workflow-pack | `90606c8315ee09cafc303515c5f33024db6b9882` | [`b38be6a7f6350964d59328b52f0624e1d1d552d1`](https://github.com/affaan-m/ECC/commit/b38be6a7f6350964d59328b52f0624e1d1d552d1) |
| [Context7](https://github.com/upstash/context7) | mcp | `b5e81de845092694ba1bfc5af15400f319c89b6d` | [`ceaf5f91f48949eaa6e4da5e66f3f59d1b44556d`](https://github.com/upstash/context7/commit/ceaf5f91f48949eaa6e4da5e66f3f59d1b44556d) |
| [Agent Reach](https://github.com/Panniantong/Agent-Reach) | research-tool | `beabda7486e9a666360b18cdb5c0e759c2c4d20f` | [`7a38047acf26a729cbb27851e3cb81639da86b29`](https://github.com/Panniantong/Agent-Reach/commit/7a38047acf26a729cbb27851e3cb81639da86b29) |
| [Graphify](https://github.com/Graphify-Labs/graphify) | codebase-tool | `92741d162b2094ffc2fed58cfbd8ee823e9da62c` | [`32e5efe935e6844ef39a5e33409e4efe848f2172`](https://github.com/Graphify-Labs/graphify/commit/32e5efe935e6844ef39a5e33409e4efe848f2172) |
| [Strix](https://github.com/usestrix/strix) | security-tool | `14cc948c36e90517a774cf32bdfe5d8cd3605b62` | [`6b7ae2ebe4d47037a927aade23265ff4e4f27e84`](https://github.com/usestrix/strix/commit/6b7ae2ebe4d47037a927aade23265ff4e4f27e84) |
| [ponytail](https://github.com/DietrichGebert/ponytail) | workflow-pack | `09c434ab73ca43761c5d8b0c5d341926c2fba710` | [`96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`](https://github.com/DietrichGebert/ponytail/commit/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846) |
| [gstack](https://github.com/garrytan/gstack) | workflow-pack | `6f7488a70f23bc71745bde704eda98033cc33bfa` | [`8f08cb76ac63ec9393e382568e30e511e8d70069`](https://github.com/garrytan/gstack/commit/8f08cb76ac63ec9393e382568e30e511e8d70069) |
| [Firecrawl](https://github.com/firecrawl/firecrawl) | research-tool | `5228ce8ac720c321374a7ad4f6eebb9eba2d3072` | [`8ffe58599538ed0e36b5ad2530a64cdcb285ceca`](https://github.com/firecrawl/firecrawl/commit/8ffe58599538ed0e36b5ad2530a64cdcb285ceca) |
| [claude-mem](https://github.com/thedotmack/claude-mem) | memory-tool | `73d86abd2617d3f5057f79cacf2aed562f52cf2b` | [`63efe315b4bb85b21dad871cf7e6a9dbd1867864`](https://github.com/thedotmack/claude-mem/commit/63efe315b4bb85b21dad871cf7e6a9dbd1867864) |
| [awesome-opencode](https://github.com/awesome-opencode/awesome-opencode) | discovery-catalog | `bcc5c03cec19789b45ef9af4a969e3fe3fd7431b` | [`37e8c941cbae9dc663aaed8841f83a0f054997b7`](https://github.com/awesome-opencode/awesome-opencode/commit/37e8c941cbae9dc663aaed8841f83a0f054997b7) |

## Review checklist

- Read upstream release notes and the commit range.
- Confirm the current license and any compatibility changes.
- Decide explicitly whether to update the reviewed pin or enabled status.
- Update `last_reviewed` only after human review.
