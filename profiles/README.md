# OpenCode profiles

Profiles are opt-in OpenCode configurations. The launcher sets `OPENCODE_CONFIG` only for the OpenCode process it starts, so switching profiles does not rewrite the root configuration.

```powershell
.\scripts\opencode-profile.ps1 superpowers
```

Available profiles: `superpowers`, `ecc`, `gstack`, `research`, `security`, and `memory`. Start OpenCode normally to use the base `opencode.json` configuration.

| Profile | Adds | Notes |
|---|---|---|
| `superpowers` | Superpowers and ponytail skills | Review both instruction sets for task-specific fit |
| `ecc` | ECC | Broad optional practices and tools |
| `gstack` | gstack | Some workflows may require setup hooks or additional tools |
| `research` | Agent Reach / Firecrawl integrations | Review service setup and Firecrawl's AGPL-3.0 license |
| `security` | Strix | Use only when explicitly requested and on an authorized target |
| `memory` | claude-mem | Requires separately configured services; it is not started automatically |

Profiles do not install dependencies, start services, authenticate accounts, or execute a skill automatically. Read the profile JSON and relevant upstream instructions before enabling a profile in another project.
