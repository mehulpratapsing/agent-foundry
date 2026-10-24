---
name: project-planning
description: Turn a feature or substantial change into a decision-complete, reviewable plan before implementation.
license: MIT
compatibility: Agent Skills format; Codex, Gemini CLI, OpenCode, Cursor, and GitHub Copilot. Toolkit-authored workflow informed by Superpowers.
---

# Project planning

Use for multi-step features, architecture changes, or work with material tradeoffs. For small, clear edits, act directly.

1. Inspect the repository, current behavior, conventions, and constraints before asking questions.
2. State the goal, users, success criteria, scope, assumptions, and dependencies. Ask only about decisions that cannot be discovered and materially affect the outcome.
3. Compare viable approaches where a real tradeoff exists, then recommend one.
4. Specify affected interfaces, data flow, failure cases, compatibility, and acceptance checks at the level needed to implement without guesswork.
5. Keep the final plan concise and ordered. Do not modify files while planning unless the user requests execution and the active mode permits it.

Upstream reference: [Superpowers](https://github.com/obra/superpowers) and [ECC](https://github.com/affaan-m/ECC). This local workflow does not install or copy either project.
