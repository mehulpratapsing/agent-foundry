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
5. Keep the plan concise and ordered. If the user requested planning only, do not modify files. If the user asked for execution, planning does not prevent implementation; do not create planning-only delay.

## Expected output

For a substantial task, provide a reviewable plan with these headings (omit a heading when it truly does not apply):

- **Outcome and users** — the behavior or deliverable and who needs it.
- **Acceptance checks** — observable conditions that define completion.
- **Scope and assumptions** — included work and reversible defaults.
- **Approach** — ordered changes, interfaces/data flow, and meaningful alternatives.
- **Risks and dependencies** — failure modes, compatibility, access, and unresolved blockers.

Do not turn a small edit into a planning document. If the request already authorizes execution, treat the plan as an implementation guide and continue.

## Completion check

The plan is decision-complete enough to implement without inventing requirements. Open questions are limited to decisions that materially change the outcome and cannot be resolved from the repository or request.

Upstream reference: [Superpowers](https://github.com/obra/superpowers) and [ECC](https://github.com/affaan-m/ECC). This local workflow does not install or copy either project.
