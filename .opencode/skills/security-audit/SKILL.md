---
name: security-audit
description: Plan or perform a scoped security review; use Strix only when explicitly requested and the target is authorized.
license: MIT
compatibility: OpenCode; Strix source is vendored under upstream/strix, but runtime dependencies are not installed by this toolkit.
---

# Security audit

Use for a security review of code, an API, or an application. Begin with a read-only scope and threat review.

1. Identify the target, environment, authentication boundary, and allowed testing scope. Do not test third-party or production systems without explicit authorization.
2. Review source and configuration for relevant trust boundaries, access controls, input handling, secrets, and unsafe defaults.
3. Run Strix only when the user explicitly requests active testing, the target is authorized, and scope is clear. Follow the current upstream setup and avoid destructive actions.
4. Report findings with evidence, impact, reproduction conditions, and practical remediation. Distinguish confirmed findings from hypotheses.
5. Do not expose secrets or include sensitive data unnecessarily in reports.

Upstream reference: [Strix](https://github.com/usestrix/strix), vendored at `upstream/strix`. This toolkit neither installs runtime dependencies nor starts scans automatically.
