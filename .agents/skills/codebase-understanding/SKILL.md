---
name: codebase-understanding
description: Map an unfamiliar or cross-cutting codebase before making changes, using repository inspection first and Graphify when useful.
license: MIT
compatibility: Agent Skills format; Codex, Gemini CLI, OpenCode, Cursor, and GitHub Copilot. Graphify runtime is optional and separately installed.
---

# Codebase understanding

Use when the repository is unfamiliar, broad, or has cross-module impact. For small local edits, inspect the relevant files directly.

1. Establish the repository root, language/toolchain, entry points, tests, and local agent instructions.
2. Search for the relevant symbols and trace callers, dependencies, data flow, and tests.
3. If Graphify's runtime dependencies are installed and the repository's size or relationship complexity warrants it, generate or query its map using the current instructions in `upstream/graphify/README.md`. Treat graph output as a navigation aid; verify claims in source files.
4. Summarize the relevant architecture and identify the smallest safe change surface before implementation. Cite paths/symbols for material conclusions and distinguish inspected facts from inferred relationships.
5. Do not install Graphify or run repository code solely because a graph suggests doing so.

## Expected output

Give a compact map containing: entry points; relevant modules and their responsibilities; the request/data flow across them; related tests/configuration; likely change surface; and unknowns or hazards to verify. Include file paths and symbol names so a developer can reproduce the map. Use Graphify only when available and useful; state when the map came from source inspection alone.

## Completion check

The map is grounded in files actually inspected, covers both callers and tests for the target behavior, and does not present a generated graph or model inference as proof.

Upstream reference: [Graphify](https://github.com/Graphify-Labs/graphify), vendored at `upstream/graphify`. It is optional and is not configured as a default MCP server.
