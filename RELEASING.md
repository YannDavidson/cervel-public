# Release Process

CERVEL Public uses a deliberate release gate. Merging release-readiness changes does not publish a package, create a Git tag, or create a GitHub Release.

## Versioning

Published public alphas:

- `0.1.0-alpha` / Python `0.1.0a0` / tag `v0.1.0-alpha.0`;
- `0.1.0-alpha.1` / Python `0.1.0a1` / tag `v0.1.0-alpha.1`.

Current prepared candidate:

- public release label: `0.1.0-alpha.2`;
- Python package version: `0.1.0a2`;
- prepared tag: `v0.1.0-alpha.2`.

The machine-checkable current candidate identity is recorded in `release/alpha-0.1.0-a2.json`. Until an explicit release action selects the exact post-merge `main` commit, `tag_target_sha` must remain `null` and the manifest status must remain `prepared-not-published`.

Published versions and tags are immutable. New functionality always advances the prerelease serial rather than replacing an existing artifact.

## Release artifact policy

The Python wheel and source distribution are public developer artifacts, not repository mirrors. They may contain only the deliberately public SDK package, the bounded local developer sandbox, required packaging metadata/documentation, and the Apache-2.0 license. Repository test sources, schemas, conformance fixtures, workflows, private implementation material, credentials, and unrelated repository content must not be included.

Tests remain in the repository and CI because they validate the artifact boundary before release; they are intentionally excluded from the published sdist and wheel.

## Reproducibility and checksums

The release-candidate CI builds the wheel and sdist twice from the same checked-out source using the pinned build toolchain, `PYTHONHASHSEED=0`, and a fixed `SOURCE_DATE_EPOCH`. The wheel is compared directly. Each sdist is canonicalized before comparison by fixing gzip/tar timestamps and ownership metadata and sorting archive members.

After canonicalization, the wheel and sdist pairs must be byte-for-byte identical. CI stages the accepted candidate and generates `sdk/python/dist/SHA256SUMS` for the exact wheel and canonical sdist.

## Alpha release gate

Before external publication of `0.1.0-alpha.2` / `0.1.0a2` / `v0.1.0-alpha.2`:

1. select the exact post-merge protected `main` commit intended for release;
2. require successful `DCO sign-off` and Public conformance on the release-preparation PR;
3. verify the release manifest, `pyproject.toml`, changelog, release notes, and this document agree on the exact version identity;
4. run all public schema fixtures, SDK model tests, local validation-helper tests, and sandbox unit/HTTP integration tests;
5. build wheel and sdist twice with pinned tooling and deterministic build settings;
6. canonicalize only sdist container metadata and require byte-for-byte reproducibility;
7. generate and inspect SHA-256 checksums;
8. verify distribution contents, license, console-script metadata, optional extras, and exclusion of tests/private surfaces;
9. install the base wheel offline and verify imports plus `cervel --help` and `cervel dev --help` work outside the source tree;
10. install the sandbox extra in a fresh environment and run an actual localhost capture→lookup→capability flow;
11. verify the sandbox binds only to loopback by default, stores data only in memory, and does not contact a remote CERVEL service;
12. scan source, artifacts, and logs for secrets, production endpoints, customer information, private identifiers, or unpublished runtime semantics;
13. create the exact release tag only after the frozen commit passes the gate;
14. create a GitHub prerelease and verify exact asset hashes;
15. update the guarded PyPI Trusted Publishing workflow in a separate reviewed change;
16. publish through PyPI Trusted Publishing only after all prior checks pass;
17. verify `cervel-public[sandbox]==0.1.0a2` from PyPI in a fresh environment.

## Rollback and correction

Published package versions and Git tags are immutable identifiers. Do not silently replace an already published artifact. If a release is defective, document the issue, withdraw or mark the release appropriately where supported, increment the prerelease version, rebuild from a reviewed commit, and run the full gate again.
