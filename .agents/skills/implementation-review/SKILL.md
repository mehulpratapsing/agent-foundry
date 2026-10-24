---
name: implementation-review
description: Implement a scoped change in small steps, then review the diff and report validation evidence.
license: MIT
compatibility: Agent Skills format; Codex, Gemini CLI, OpenCode, Cursor, and GitHub Copilot. Toolkit-authored workflow informed by ECC and Superpowers.
---

# Implementation and review

1. Restate the behavior and acceptance criteria; inspect repository conventions and the current diff.
2. Implement the smallest complete change. Avoid speculative features and parallel mechanisms.
3. Add or update a regression check when needed to prove changed behavior or prevent a reproduced defect. Do not add unrelated tests. Run the checks required by the acceptance criteria and report any that could not run.
4. Review the final diff for correctness, edge cases, error handling, security, maintainability, and scope.
5. Report changed behavior, checks actually run, results, and remaining limitations. Never imply unrun checks passed.

## Expected output

For implementation, summarize changed behavior and affected files, then list each validation command with its observed result. For review-only work, report findings first in severity order using: **severity**, **file and location**, **evidence**, **impact/preconditions**, and **recommended fix**. Label unconfirmed concerns separately. End with remaining limitations or state that none were found within the reviewed scope.

## Completion check

The diff matches the request; each material bug found during review is fixed or explicitly reported; relevant tests/checks ran; and documentation describes the delivered behavior rather than a planned future state.

Upstream references: [ECC](https://github.com/affaan-m/ECC) and [Superpowers](https://github.com/obra/superpowers). Their upstream skill packs are not copied or automatically activated here; this skill is the single local implementation/review workflow.
