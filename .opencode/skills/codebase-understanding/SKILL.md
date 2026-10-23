---
name: codebase-understanding
description: Map an unfamiliar or cross-cutting codebase before making changes, using repository inspection first and Graphify when useful.
license: MIT
compatibility: OpenCode; Graphify is an optional separately installed tool and is not bundled.
---

# Codebase understanding

Use when the repository is unfamiliar, broad, or has cross-module impact. For small local edits, inspect the relevant files directly.

1. Establish the repository root, language/toolchain, entry points, tests, and local agent instructions.
2. Search for the relevant symbols and trace callers, dependencies, data flow, and tests.
3. If Graphify is installed and the repository's size or relationship complexity warrants it, generate or query its map using the current upstream instructions. Treat graph output as a navigation aid; verify claims in source files.
4. Summarize the relevant architecture and identify the smallest safe change surface before implementation.
5. Do not install Graphify or run repository code solely because a graph suggests doing so.

Upstream reference: [Graphify](https://github.com/Graphify-Labs/graphify). It is optional and is not configured as a default MCP server.
