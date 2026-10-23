# Curated AI Engineering Toolkit

A small control plane for a GLM-5.3 + OpenCode workflow. This repository keeps local policy and focused skills; upstream projects remain separate and are tracked by commit in [`sources.json`](sources.json).

## Contents

- `AGENTS.md` — shared engineering and safety rules.
- `opencode.json` — project-local Context7 MCP configuration. OpenCode discovers the skills below automatically.
- `.opencode/skills/` — on-demand workflows for planning, current library research, codebase mapping, implementation/review, and security audits.
- `sources.json` — upstream URLs, pinned revisions, licenses, status, and review metadata. `enabled` means that upstream integration itself is active by default; ECC and Superpowers are referenced by local workflows but are not installed as upstream packs.
- `.github/workflows/upstream-drift.yml` — weekly check that proposes a report PR without changing pins.
- `scripts/check_upstreams.py` — standard-library-only drift checker.

## Start here

1. Open this directory as an OpenCode project. Set your preferred GLM provider/model in your existing user or project configuration; this toolkit intentionally does not guess the provider identifier.
2. OpenCode will discover `.opencode/skills/*/SKILL.md` on demand.
3. Context7 is configured as a remote MCP endpoint. Authenticate with OpenCode if prompted. Keep any API key in an environment variable, never in this repository.
4. Install Agent Reach, Graphify, or Strix separately only when a project needs them. Follow each upstream project's current setup and inspect its permissions before use.

## How sources are managed

The `sources.json` commit is the reviewed pin. The weekly workflow compares it with each repository's current default-branch head and creates a PR containing a dated report. It does not update pins, copy upstream code, install tools, or enable optional sources. Review upstream release notes, license changes, compatibility, and security implications before changing a pin or status.

Only Context7's remote MCP integration is enabled by default. ECC and Superpowers are core workflow references, not installed upstream packs; the local skills are independently authored. Optional and deferred projects are tracked for visibility but are not enabled. In particular, `awesome-opencode` and GitHub Trending support discovery; Context7 supplies current documentation for requested libraries and does not guarantee discovery of every new package.

## Validation

Run `python scripts/check_upstreams.py --offline` to validate manifest shape and generate a local report without network access. Run it without `--offline` to query GitHub's API; set `GITHUB_TOKEN` to avoid low unauthenticated rate limits.

For the scheduled workflow to open PRs, enable **Allow GitHub Actions to create and approve pull requests** in the repository's Actions settings. The workflow does not need any project secrets.

## License

Toolkit-authored material is MIT-licensed; upstream projects retain their own licenses. See [`LICENSE`](LICENSE).
