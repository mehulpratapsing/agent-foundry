---
name: security-audit
description: Plan or perform a scoped security review; use Strix only when explicitly requested and the target is authorized.
license: MIT
compatibility: Agent Skills format; Codex, Gemini CLI, OpenCode, Cursor, and GitHub Copilot. Strix runtime is optional and separately installed.
---

# Security audit

Use for a security review of code, an API, or an application. Begin with a read-only scope and threat review.

1. Identify the target, environment, authentication boundary, and allowed testing scope. Do not test third-party or production systems without explicit authorization.
2. Review source and configuration for relevant trust boundaries, access controls, input handling, secrets, and unsafe defaults.
3. Default to source/configuration review. Run active probes or Strix only when the user clearly requested active security testing, the target is authorized, and the allowed scope is explicit. A request for a read-only review is not authorization to probe. Never scan an unrelated or third-party target.
4. Report findings with severity, affected asset and file/location, evidence, impact, preconditions/reproduction, and practical remediation. Distinguish confirmed findings from hypotheses; group duplicates and avoid claiming a clean bill of health from a bounded review.
5. Do not expose secrets or include sensitive data unnecessarily in reports.

Use Critical / High / Medium / Low / Informational consistently: Critical means likely catastrophic compromise or broad exposure; High means serious compromise of an important asset; Medium means material but constrained impact; Low means limited impact or difficult preconditions; Informational means a hardening note without a demonstrated vulnerability. Base severity on realistic impact and preconditions, not only a tool's score; state when the score is provisional.

## Expected output

Start with **scope and method** (target, environment, authorization, and what was not tested). Then list findings from highest to lowest severity using the fields above. Close with **positive controls observed**, **limitations**, and **recommended next checks**. For a source-only review, explicitly say no active exploit validation was performed.

## Completion check

Every reported issue has evidence and a practical fix; every relevant trust boundary in the agreed scope was considered; and runtime/active-test claims match observed tool output. If the scope is too broad, report what was covered instead of implying full coverage.

Upstream reference: [Strix](https://github.com/usestrix/strix), vendored at `upstream/strix`. This toolkit neither installs runtime dependencies nor starts scans automatically.
