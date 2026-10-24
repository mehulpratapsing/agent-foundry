---
name: current-library-research
description: Check current, version-specific library and framework documentation before choosing or implementing APIs; discover candidate projects when asked.
license: MIT
compatibility: Agent Skills format; Codex, Gemini CLI, OpenCode, Cursor, and GitHub Copilot. Context7 MCP is configured in the OpenCode base config; other harnesses can use the native templates under adapters/mcp/templates.
---

# Current library research

Use for unfamiliar, recently changed, or version-sensitive libraries, frameworks, and APIs. For discovering candidate tools or libraries, use `tool-discovery` instead.

1. Identify the exact library and version in the project manifests or ask only if it cannot be established.
2. Use Context7 to resolve the library and retrieve documentation for the relevant task. Prefer the exact version when available; report if the requested version is missing.
3. Verify material recommendations against official documentation or source repositories and link the sources.
4. Separate documented facts from inference. Do not claim Context7 indexes every library or automatically discovers new packages.

## Expected output

Report the package and version inspected, the documentation source(s), the relevant supported API/configuration details, any version mismatch or unavailable docs, and recommendations. Link primary documentation near the claims it supports. Label inference and uncertainty; never imply a Context7 lookup succeeded unless its result was observed.

## Completion check

The recommendation is traceable to documentation for the actual dependency version, or clearly states the nearest version checked and what remains unverified. If Context7 is unavailable, use official project docs/source and say so; do not block unrelated implementation.

Upstream reference: [Context7](https://github.com/upstash/context7). Context7 docs are refreshed for requested libraries; this is documentation freshness, not automatic ecosystem discovery.
