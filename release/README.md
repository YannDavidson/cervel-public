# Release Candidate Controls

This directory contains machine-checkable controls for preparing public CERVEL releases without publishing them.

For the first alpha candidate, `alpha-0.1.0.json` freezes the human release label, Python package version, and prepared tag name. Its `tag_target_sha` remains `null` until an explicit release action selects the exact post-merge `main` commit that passed the full release gate.

`verify_candidate.py` enforces metadata consistency, compares two independently built wheel/sdist pairs byte-for-byte, stages the accepted pair, and generates SHA-256 checksums. It does not create tags, GitHub Releases, registry publications, deployments, or production interfaces.
