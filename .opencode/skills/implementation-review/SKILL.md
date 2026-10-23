---
name: implementation-review
description: Implement a scoped change in small steps, then review the diff and report validation evidence.
license: MIT
compatibility: OpenCode; toolkit-authored workflow informed by ECC and Superpowers.
---

# Implementation and review

1. Restate the behavior and acceptance criteria; inspect repository conventions and the current diff.
2. Implement the smallest complete change. Avoid speculative features and parallel mechanisms.
3. Add or update checks only when requested or necessary to establish the stated acceptance criteria.
4. Review the final diff for correctness, edge cases, error handling, security, maintainability, and scope.
5. Report changed behavior, checks actually run, results, and remaining limitations. Never imply unrun checks passed.

Upstream references: [ECC](https://github.com/affaan-m/ECC) and [Superpowers](https://github.com/obra/superpowers). Their upstream skill packs are not copied or automatically activated here; this skill is the single local implementation/review workflow.
