# Fieldnote skill trial and operations log

**Run date:** 2026-10-24  
**Purpose:** Exercise Agent Foundry's local workflows on a non-trivial codebase, record what they helped with, and use observed gaps to improve the workflows.  
**Result:** A synthetic API test project was created outside this repository at `C:\AgentFoundry-Complex-Test`. It is not a product, upstream fork, or committed fixture in Agent Foundry.

## Executive assessment

The five original local skills were a useful starting set and OpenCode discovered them. They supported planning, version-aware dependency research, source inspection, implementation/review, and a read-only security review. The trial exposed three prompt-quality gaps: outputs were not standardized, implementation checks could be interpreted too weakly, and tool discovery was mixed into library-documentation research.

The toolkit changes from this trial retain all five workflows, clarify their expected deliverables and completion conditions, and add a sixth `tool-discovery` skill for the separate task of evaluating new projects. No skill was removed: each original workflow was exercised and remains a distinct capability. The result is an exploratory single-project evaluation, not a controlled benchmark or proof of equal behavior across every listed harness.

## Test project

Fieldnote is a deliberately broad local project-management API used to exercise cross-cutting work:

- FastAPI with Pydantic v2, async SQLAlchemy, Alembic, and SQLite.
- Organizations, memberships, tenant isolation, role-based access, and demo authentication.
- Project/task CRUD, optimistic concurrency, and cursor pagination.
- Idempotency keys with response replay and conflict handling.
- Transactional audit records and a webhook outbox with retries, dead-letter state, and HMAC signing.
- Liveness/readiness endpoints, including database migration-head and worker-heartbeat checks.

The optional browser UI was not built; the plan's feasibility gate called for cutting it if it expanded the test beyond a dependency-light API exercise.

## Operations performed

1. Created the Fieldnote project outside Agent Foundry and copied in the canonical `AGENTS.md`, root OpenCode configuration, and five local skill directories. Kept upstream repositories separate and did not modify their snapshots.
2. Used OpenCode's skill-discovery diagnostics to confirm it recognized the local workflows. The base configuration exposed Context7; specialist upstream profiles were not enabled for the application build.
3. Used project planning to define milestones and acceptance checks. Used Context7 for version-specific async SQLAlchemy and Alembic guidance, and inspected the project files and dependency versions directly.
4. Implemented the API in milestones: scaffold/data/migrations; auth, tenancy, and RBAC; CRUD, concurrency, and pagination; idempotency and audit; webhook outbox and delivery worker; readiness and documentation.
5. Ran the growing test suite and static checks during implementation, reviewed failures, and fixed reproduced defects before final validation.
6. Performed a read-only security review of the local source and configuration. No Strix scan or active exploit test was run. Graphify was not installed; codebase understanding used direct repository/file/symbol inspection.
7. Started Uvicorn locally and exercised readiness, token issuance, current-user lookup, project creation, and task creation/replay over loopback HTTP. Stopped the server and removed the temporary live-validation database afterward.

## Findings that changed the implementation

| Observed issue | Correction made | Evidence after correction |
|---|---|---|
| Two concurrent requests with the same idempotency key could return different task IDs. A losing transaction rolled back database writes but still returned its in-memory task. | Use the database uniqueness constraint as the arbiter across workers; roll back the losing transaction and return the winner's stored response. Avoid relying on an in-process lock. | Concurrent same-key test passed; live repeated request returned the same task ID. |
| Organization/member/webhook authorization dependencies return a membership object, not the authenticated user. Using that value as the audit actor could record the wrong ID. | Keep the role dependency for authorization and obtain the actor independently through `get_current_user`. | Added webhook audit assertion comparing recorded actor ID with `/auth/me`. |
| Webhook creation serialized the whole model into the audit event, including its signing secret. | Emit an explicit secret-free audit representation. | Regression assertion verifies the returned creation secret is absent from audit JSON. |
| A webhook URL could target a private or local destination. Redirects and ambient proxy configuration could also undermine destination checks. | Require HTTPS and public DNS/IP results before sending; disable redirect following and ambient proxy settings. Document network-level egress filtering as an additional production control. | URL, webhook, and outbox tests passed. DNS could still change between validation and connection; see limitations. |
| SQLite returned a naive worker heartbeat timestamp, which failed comparison with an aware UTC timestamp and caused live readiness to say the worker was stale. | Normalize the loaded timestamp to UTC before checking freshness. | Live `/readyz` reported database healthy, migrations current, and worker alive. |
| The original test environment's Python 3.15 could not build a dependency's native core, and `passlib==1.7.4` was incompatible with bcrypt 5. | Use a project-local Python 3.13 virtual environment and direct bcrypt calls. | Dependencies installed in the project environment; application tests and type checks ran there. |

## Validation observed

Final Fieldnote checks:

```text
python -m pytest tests -q                         100 passed, 1 skipped
ruff check .                                      passed
mypy app                                          passed (37 source files)
alembic upgrade head                              passed
alembic downgrade base                            passed
alembic upgrade head                              passed
```

The single skipped test, `test_outbox_per_delivery_exception_isolation`, requires at least two webhook subscriptions; the test fixture supplied fewer. It is not counted as passing and should be made self-contained in a future Fieldnote test-fixture change.

Live loopback smoke:

```text
/readyz: ready (database=healthy, migrations=current, worker=alive)
/auth/token: successful
/auth/me: successful
project creation: successful
same-key task create + replay: successful; both responses had the same task ID
```

The application test suite and its code are local-only and are not included in this toolkit repository. The recorded checks establish behavior on this one Windows/OpenCode run; they are not a load benchmark, a production deployment test, a full pentest, or cross-harness verification.

## Skill-by-skill evaluation

| Skill | Trial result | Improvement made |
|---|---|---|
| `project-planning` | Produced useful milestone/acceptance framing. | Added a concise expected plan structure and clarified that planning should not pause already-authorized execution. |
| `current-library-research` | Context7 was useful for exact library API guidance. | Added a version/source/fallback output contract and separated discovery of new projects into its own skill. |
| `codebase-understanding` | Direct source inspection was sufficient; optional Graphify was unavailable. | Requires a reproducible map with paths, symbols, flows, tests, change surface, and explicit distinction between source facts and graph/inference. |
| `implementation-review` | Found real transaction, audit, webhook, and readiness defects through iterative verification. | Requires regression coverage for reproduced issues and a consistent validation/findings format. |
| `security-audit` | Read-only source review found data-handling and outbound-request risks. | Adds severity calibration, scope/method disclosure, structured evidence, and an explicit no-active-test statement when applicable. |
| `tool-discovery` | Added in response to the research/discovery responsibilities being blended. | Defines primary-source checks for maintenance, license, setup, permissions, and data exposure; never installs/enables by default. |

## Limits and next evaluation

- Only OpenCode skill discovery was exercised for this test project. Compatibility declarations for other harnesses are not equivalent to runtime proof.
- The new `tool-discovery` skill was added after the Fieldnote implementation and has not yet been exercised on a real candidate-selection request. Its frontmatter/workflow contract passed repository checks, and OpenCode discovered it.
- The codebase workflow was tested without Graphify. The security workflow was source-only; Strix and other active testing were not run.
- One exploratory project cannot establish repeatability or prove the skills outperform an unassisted baseline. A better next evaluation is to repeat the same rubric on a second repository, record tool calls and outputs, and compare completeness, defect detection, and unnecessary work.
- Webhook DNS validation is subject to a DNS time-of-check/time-of-use window. Production deployments should enforce private/metadata IP blocking through an egress proxy or network policy.
