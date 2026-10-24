# Security policy

## Scope and safe use

This repository contains toolkit-authored rules and separately licensed upstream snapshots. Security tools such as Strix are opt-in. Only test systems and source code that you own or have explicit authorization to assess; define and document the scope before running a test.

Do not include secrets in issues, pull requests, logs, screenshots, or reports. Use environment variables or a local secret manager for credentials.

## Reporting a vulnerability

For a vulnerability in toolkit-authored files, use GitHub's private vulnerability reporting if it is enabled for this repository. If private reporting is unavailable, contact the repository maintainer privately before public disclosure. Include affected paths and revisions, reproduction steps, and impact, while avoiding real credentials or data belonging to others.

For an issue in a vendored upstream project, report it to the upstream maintainers using their preferred security channel. Do not assume a snapshot here is maintained by the upstream project.

## Response

The maintainer will acknowledge reports as soon as practical, validate the finding, coordinate a fix or mitigation, and credit the reporter when appropriate and with their consent. This project does not promise a formal response-time SLA.
