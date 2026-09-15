# Release Candidate Controls

This directory contains machine-checkable controls for preparing public CERVEL releases without publishing them.

Historical candidate manifests are retained as release records. Published package versions and tags are immutable.

`alpha-0.1.0-a3.json` records the current prepared `0.1.0a3` / `v0.1.0-alpha.3` candidate. Its `tag_target_sha` remains `null` until an explicit release action selects the exact post-merge protected `main` commit that passed the full release gate.

`verify_candidate.py` enforces metadata consistency for the current prepared candidate, compares two independently built wheel/sdist pairs byte-for-byte, stages the accepted pair, and generates SHA-256 checksums. It does not create tags, GitHub Releases, registry publications, deployments, or production interfaces.
