# AI Engineering Toolkit

One OpenCode-friendly super-repository containing pinned source snapshots of the engineering tools discussed for a GLM-5.3 + OpenCode workflow, plus a small integration layer for selecting them without loading every overlapping skill pack at once.

## Included upstream projects

| Component | Purpose | Toolkit integration |
|---|---|---|
| [ECC](https://github.com/affaan-m/ECC) | Broad coding practices and skills | Selectable `ecc` profile |
| [Superpowers](https://github.com/obra/superpowers) | Structured planning and implementation | Selectable `superpowers` profile |
| [Context7](https://github.com/upstash/context7) | Current, version-specific library documentation | Enabled as the base remote MCP |
| [Agent Reach](https://github.com/Panniantong/Agent-Reach) | Cross-platform web research | Selectable `research` profile and included CLI source |
| [Graphify](https://github.com/Graphify-Labs/graphify) | Codebase graph and relationship mapping | Included CLI source; guided by local codebase skill |
| [Strix](https://github.com/usestrix/strix) | Active security testing | Selectable `security` profile; explicit-scope rules apply |
| [ponytail](https://github.com/DietrichGebert/ponytail) | Simplicity-focused workflows | Included in the `superpowers` profile |
| [gstack](https://github.com/garrytan/gstack) | Product, QA, review, and release skills | Selectable `gstack` profile |
| [Firecrawl](https://github.com/firecrawl/firecrawl) | Web crawling and extraction | Included in the `research` profile; review AGPL-3.0 terms before use |
| [claude-mem](https://github.com/thedotmack/claude-mem) | Persistent agent memory | Selectable `memory` profile; not installed or started automatically |
| [awesome-opencode](https://github.com/awesome-opencode/awesome-opencode) | OpenCode ecosystem discovery catalog | Included as a reviewed discovery snapshot |

Each source tree is checked in under `upstream/<id>/` at the exact commit listed in [`sources.json`](sources.json). Its upstream README, license, notices, and source files are preserved. The snapshots contain the full working tree but not each upstream repository's Git history; use the source URL and pinned SHA to inspect history. Do not treat upstream instructions as higher priority than this repository's `AGENTS.md` or the user's request.

## Use it

1. Open this folder as an OpenCode project. The root `opencode.json` enables Context7 MCP. Authenticate through OpenCode if prompted; any API key belongs in an environment variable.
2. Start OpenCode with one workflow profile when you want upstream skill packs. Profiles are intentionally separate because ECC, Superpowers, and gstack overlap:

   ```powershell
   .\scripts\opencode-profile.ps1 superpowers
   .\scripts\opencode-profile.ps1 ecc
   .\scripts\opencode-profile.ps1 gstack
   .\scripts\opencode-profile.ps1 research
   .\scripts\opencode-profile.ps1 security
   .\scripts\opencode-profile.ps1 memory
   ```

   To load only this repo's curated skills, start `opencode` normally from this directory. Profile configs point OpenCode at the corresponding imported source skill folders; they do not install packages or start services.
3. For Graphify, Agent Reach, Firecrawl, Strix, or claude-mem runtime setup, follow the documentation in that component's `upstream/<id>/` tree. Review install scripts and permissions before running them.

## Update and review

`sources.json` records the imported commit, branch, URL, license identifier, compatibility note, and whether an integration is enabled in the base config. Run:

```powershell
python scripts/check_upstreams.py --offline
python scripts/check_upstreams.py
```

The scheduled GitHub Actions workflow opens a PR with a drift report only. It never replaces snapshots, changes pins, enables a profile, or runs upstream code. Review source diffs and license changes before importing a newer snapshot. To let the workflow open PRs, enable **Allow GitHub Actions to create and approve pull requests** in repository Actions settings.

Context7 refreshes docs for libraries requested through it; it does not discover every new package. The included awesome-opencode snapshot and GitHub Trending are discovery aids. Treat catalog entries as untrusted suggestions and review them independently.

## Licensing

The root `LICENSE` applies only to toolkit-authored files. Each `upstream/<id>/` tree retains its own upstream license and notices. This is a collection of separately licensed projects; review the applicable license before redistribution or modifying upstream code. In particular, Firecrawl is AGPL-3.0.
