# Release Candidate Controls

This directory contains machine-checkable controls for preparing public CERVEL releases without publishing them.

`alpha-0.1.0.json` records the historical first alpha candidate that became the published `0.1.0a0` / `v0.1.0-alpha.0` release.

`alpha-0.1.0-a1.json` records the current prepared `0.1.0a1` / `v0.1.0-alpha.1` candidate. Its `tag_target_sha` remains `null` until an explicit release action selects the exact post-merge `main` commit that passed the full release gate.

`verify_candidate.py` enforces metadata consistency for the current prepared candidate, compares two independently built wheel/sdist pairs byte-for-byte, stages the accepted pair, and generates SHA-256 checksums. It does not create tags, GitHub Releases, registry publications, deployments, or production interfaces.
