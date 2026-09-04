# Release Process

CERVEL Public uses a deliberate release gate. Merging release-readiness changes does not publish a package, create a Git tag, or create a GitHub Release.

## Versioning

The public repository uses semantic release labels for human-facing release communication and PEP 440 versions for the Python distribution.

For the first alpha release family:

- public release label: `0.1.0-alpha`;
- Python package version: `0.1.0a0`;
- prepared first tag: `v0.1.0-alpha.0`.

The machine-checkable candidate identity is recorded in `release/alpha-0.1.0.json`. Until an explicit release action selects the exact post-merge `main` commit, `tag_target_sha` must remain `null` and the manifest status must remain `prepared-not-published`.

If another alpha candidate is required before a stable release, increment both the tag suffix and Python alpha serial together, for example `v0.1.0-alpha.1` and `0.1.0a1`.

## Release artifact policy

The Python wheel and source distribution are public SDK artifacts, not repository mirrors. They must contain only the public SDK package, required packaging metadata and documentation, and the Apache-2.0 license. Repository test sources, schemas, conformance fixtures, workflows, private implementation material, credentials, and unrelated repository content must not be included.

Tests remain in the repository and CI because they validate the artifact boundary before release; they are intentionally excluded from the published sdist and wheel.

## Reproducibility and checksums

The release-candidate CI builds the wheel and sdist twice from the same checked-out source using the pinned build toolchain, `PYTHONHASHSEED=0`, and a fixed `SOURCE_DATE_EPOCH`. The wheel is compared directly. Because setuptools' gzip/tar container metadata is not itself stable across otherwise identical sdist builds, each sdist is canonicalized before comparison by fixing gzip/tar timestamps and ownership metadata and sorting archive members. File contents, names, modes, links, and release payload remain subject to exact comparison.

After canonicalization, the wheel and sdist pairs must be byte-for-byte identical before they are accepted as a candidate. The accepted candidate is then staged and CI generates `sdk/python/dist/SHA256SUMS` containing SHA-256 digests for the exact wheel and canonical sdist.

Checksums are evidence for the candidate produced by that exact run; they are not a substitute for selecting and recording the final release commit SHA.

## Alpha release gate

Before any external publication:

1. select the exact post-merge `main` commit intended for release and record its SHA;
2. confirm the `DCO sign-off` and Public conformance checks are successful on the release-preparation PR;
3. verify `release/alpha-0.1.0.json`, `pyproject.toml`, `CHANGELOG.md`, release notes, and this document agree on `0.1.0-alpha`, `0.1.0a0`, and `v0.1.0-alpha.0`;
4. build wheel and sdist twice from the exact release source with the pinned build tooling and deterministic build environment;
5. canonicalize only the sdist container metadata and require both candidate pairs to be byte-for-byte identical;
6. generate and inspect SHA-256 checksums for the accepted wheel and canonical sdist;
7. run distribution integrity tests, offline wheel installation, installed-wheel smoke tests, all published examples, and public schema/conformance tests;
8. inspect both archives and verify the Apache-2.0 license is present and repository tests/private surfaces are absent;
9. scan the exact release diff and artifacts for secrets, private identifiers, production endpoints, customer information, or unpublished CERVEL runtime semantics;
10. update the release record with the exact selected `main` SHA only as part of the explicit release action;
11. create the annotated/signed `v0.1.0-alpha.0` tag only after the exact commit passes the gate;
12. create a prerelease GitHub Release from that tag only after tag verification;
13. publish the Python package only as a separate explicit action after the GitHub release artifacts, checksums, and metadata are verified.

No workflow in this repository currently publishes to PyPI or another package registry, and PR #21 does not create the prepared tag.

## Rollback and correction

Published package versions and Git tags are immutable identifiers. Do not silently replace an already published artifact. If a release is defective, document the issue, withdraw or mark the release appropriately where supported, increment the prerelease version, rebuild from a reviewed commit, and run the full gate again.
