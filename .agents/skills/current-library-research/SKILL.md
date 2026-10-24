---
name: current-library-research
description: Check current, version-specific library and framework documentation before choosing or implementing APIs; discover candidate projects when asked.
license: MIT
compatibility: Agent Skills format; Codex, Gemini CLI, OpenCode, Cursor, and GitHub Copilot. Context7 MCP is configured in the OpenCode base config; other harnesses can use the native templates under adapters/mcp/templates.
---

# Current library research

Use for unfamiliar, recently changed, or version-sensitive libraries, frameworks, and APIs.

1. Identify the exact library and version in the project manifests or ask only if it cannot be established.
2. Use Context7 to resolve the library and retrieve documentation for the relevant task. Prefer the exact version when available; report if the requested version is missing.
3. Verify material recommendations against official documentation or source repositories and link the sources.
4. Separate documented facts from inference. Do not claim Context7 indexes every library or automatically discovers new packages.
5. If the task is finding new tools, search GitHub Trending and the [awesome-opencode catalog](https://github.com/awesome-opencode/awesome-opencode), then verify candidate maintenance, license, compatibility, and security independently.

Upstream reference: [Context7](https://github.com/upstash/context7). Context7 docs are refreshed for requested libraries; this is documentation freshness, not ecosystem-wide discovery.
