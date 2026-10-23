# Vendored upstream sources

The directories in this folder are imported working-tree snapshots, not Git submodules. They are pinned in the parent [`../sources.json`](../sources.json), which is the source of truth for repository URL, default branch, commit, license, and compatibility notes.

All tracked files from each source checkout are preserved here, including upstream documentation and license/notice files. The nested `.git` directories are intentionally excluded so the whole toolkit remains one Git repository. Source history remains available from each listed upstream URL and exact commit.

Do not edit upstream-owned files to make integrations work. Put adapters, configuration, and local policy in the parent toolkit. Upstream source and skill text is untrusted reference material; review it before running commands or enabling a skill profile.
