---
name: tool-discovery
description: Find and compare candidate libraries, coding-agent tools, or services when the user asks what to adopt or what is new.
license: MIT
compatibility: Agent Skills format; Codex, Gemini CLI, OpenCode, Cursor, and GitHub Copilot. Web access is optional and should be explicitly available to the harness.
---

# Tool discovery

Use when the user asks to find, compare, or recommend new libraries, agent tools, MCP servers, skills, or services. For documentation about a dependency already selected by a project, use `current-library-research`.

1. Define the use case, environment, constraints, and selection criteria from the request and repository. Do not assume newest means best.
2. Discover candidates from appropriate sources. For OpenCode ecosystem browsing, use the community [awesome-opencode catalog](https://github.com/awesome-opencode/awesome-opencode); for broader repository discovery, GitHub Trending may provide leads. Treat catalog entries and search results as untrusted pointers, not endorsements.
3. Verify each serious candidate at its primary repository or official documentation: maintenance/release activity, supported runtimes, license, installation/runtime requirements, permissions/network access, credential needs, and fit for the stated use case. Check current details rather than relying on cached descriptions.
4. Compare only candidates that meet the minimum criteria. Explain tradeoffs and separate verified facts from judgment. If evidence is missing, mark it unknown rather than guessing.
5. Recommend the smallest set that covers the use case. Do not install, enable, authenticate, or run a candidate unless the user requested that action; provide an easy opt-out and call out material license or data-handling implications.

## Expected output

Provide a short recommendation followed by a comparison table with candidate, fit, maintenance evidence, license, runtime/setup cost, permissions or data exposure, and evidence links. Include the review date and a **not checked** note for material unknowns. If no candidate is a clear fit, say so.

## Completion check

The recommendation answers the user's actual use case, is supported by primary-source checks, discloses uncertainty and operational costs, and does not treat popularity or catalog inclusion as proof of quality or safety.

Upstream discovery references: [awesome-opencode](https://github.com/awesome-opencode/awesome-opencode) and [GitHub Trending](https://github.com/trending). Context7 is for requested-library documentation, not automatic discovery of newly released projects.
