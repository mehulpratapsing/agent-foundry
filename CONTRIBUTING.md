# Contributing

Thanks for helping make Agent Foundry clearer and safer to use.

## Before opening a change

- Keep the toolkit curated: explain the specific gap a new tool or instruction solves.
- Keep upstream projects attributed and separately licensed. Do not move or rewrite their notices.
- Never add credentials, private data, or generated scan evidence containing sensitive material.
- For security testing, use only an explicitly authorized target and scope.

## Source of truth and upstream pins

- Edit `AGENTS.md` for canonical shared rules, then run `python scripts/generate_adapters.py`.
- Keep generated adapter files in sync; verify with `python scripts/generate_adapters.py --check`.
- For an upstream update, change `sources.json` and the corresponding snapshot together. Record the exact upstream commit and review license, notices, and relevant changes before proposing it.
- A drift report is evidence for review, not automatic approval to update or activate a source.

## Verify your changes

```powershell
python scripts/generate_adapters.py --check
python scripts/verify_toolkit.py --static
python scripts/verify_toolkit.py --opencode
python -m unittest discover -s tests -v
```

In your pull request, summarize the user-visible effect, list the checks you ran, and call out any tool activation, license, or security-scope change.
