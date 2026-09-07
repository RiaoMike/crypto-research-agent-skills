# Validation Record

## 0.2.0 — 2026-09-07 (Linux, Python 3.14.7)

Added `crypto-venue-paper-writing`, `ccs-writing-style`, and `usenixsec-writing-style` (16 canonical skills total). Results on this machine:

| Check | Result |
|---|---:|
| Canonical top-level skills | 16 |
| Standard-library unit tests | 19 passed, 0 failed |
| Repository validator | 16 passed, 0 failed |
| Dry-run install plan | 16 skills, no writes |
| Skills tree files | 68 |
| Public Markdown files checked | 80 |
| Broken local Markdown links | 0 |
| Exact author-machine path or private-key hits | 0 |
| ZIP files in source tree | 0 |

## 0.1.0 — 2026-08-31 (Windows)

Date: 2026-08-31
Release candidate: `v0.1.0`
Local platform: Windows
Local Python: 3.14.6
Local Git: 2.54.0.windows.1

### Results

| Check | Result |
|---|---:|
| Canonical top-level skills | 13 |
| Canonical skill files installed in smoke test | 58 |
| Standard-library unit tests | 18 passed, 0 failed |
| Repository validator | 13 passed, 0 failed |
| Meta-skill validator | 13 passed, 0 failed |
| Dry-run install plan | 13 skills, no writes |
| Real isolated install | 58 files, 0 hash mismatches |
| Public Markdown files checked | 68 |
| Broken local Markdown links | 0 |
| Exact author-machine path or private-key hits | 0 |
| GitHub token-pattern hits | 0 |
| ZIP files in source tree | 0 |
| Python cache files eligible for commit | 0 |

Commands:

```bash
python -m unittest discover -s tests -v
python scripts/validate.py skills
python scripts/install.py --target custom --dest .install-smoke --dry-run
```

The real-install check copied all skills into a newly created temporary directory, compared every source/destination file with SHA-256, and then removed that verified temporary directory.

## Continuous Integration

GitHub Actions is configured to run the unit tests, corpus validator, and installer dry-run on Ubuntu and Windows with Python 3.10 and 3.12. The first remote workflow run necessarily occurs after the initial push; local results above do not claim that remote matrix has already completed.

## Limits of This Evidence

- The evaluation-scenario files are test specifications, not completed blinded trials on every model/harness combination.
- Structural and unit validation cannot prove that an agent will discover all prior art, catch every proof gap, reproduce an artifact on every platform, or follow instructions under all prompts.
- The release has not independently certified any paper, construction, implementation, parameter set, or security claim.
- Venue and harness policies change. Users must refresh official requirements and retest the exact deployed model, tools, permissions, and context limits.
- “Top-venue rigor” names the workflow target; it is not an acceptance, novelty, correctness, or security guarantee.
