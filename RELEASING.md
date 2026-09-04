# Release Process

CERVEL Public uses a deliberate release gate. Merging release-readiness changes does not publish a package, create a Git tag, or create a GitHub Release.

## Versioning

The public repository uses semantic release labels for human-facing release communication and PEP 440 versions for the Python distribution.

For the first alpha release family:

- public release label: `0.1.0-alpha`;
- Python package version: `0.1.0a0`;
- recommended first tag: `v0.1.0-alpha.0`.

If another alpha candidate is required before a stable release, increment both the tag suffix and Python alpha serial together, for example `v0.1.0-alpha.1` and `0.1.0a1`.

## Release artifact policy

The Python wheel and source distribution are public SDK artifacts, not repository mirrors. They must contain only the public SDK package, required packaging metadata and documentation, and the Apache-2.0 license. Repository test sources, schemas, conformance fixtures, workflows, private implementation material, credentials, and unrelated repository content must not be included.

Tests remain in the repository and CI because they validate the artifact boundary before release; they are intentionally excluded from the published sdist and wheel.

## Alpha release gate

Before any external publication:

1. select the exact `main` commit intended for release and record its SHA;
2. confirm the `DCO sign-off` and Public conformance checks are successful on the release-preparation PR;
3. build wheel and sdist from the exact release commit with the pinned build tooling;
4. run distribution integrity tests, offline wheel installation, installed-wheel smoke tests, all published examples, and public schema/conformance tests;
5. inspect both archives and verify the Apache-2.0 license is present and repository tests/private surfaces are absent;
6. confirm package metadata and release notes describe the same version;
7. scan the exact release diff and artifacts for secrets, private identifiers, production endpoints, customer information, or unpublished CERVEL runtime semantics;
8. create the annotated/signed release tag only after the exact commit passes the gate;
9. create a prerelease GitHub Release from that tag only after tag verification;
10. publish the Python package only as a separate explicit action after the GitHub release artifacts and metadata are verified.

No workflow in this repository currently publishes to PyPI or another package registry.

## Rollback and correction

Published package versions and Git tags are immutable identifiers. Do not silently replace an already published artifact. If a release is defective, document the issue, withdraw or mark the release appropriately where supported, increment the prerelease version, rebuild from a reviewed commit, and run the full gate again.
