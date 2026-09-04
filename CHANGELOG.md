# Changelog

All notable changes to the deliberately public CERVEL developer surface are recorded here.

The repository is pre-stable. Until a stable release is declared, public contracts and SDK surfaces may evolve between alpha releases. Versioned schemas and published compatibility statements remain authoritative for their stated versions.

## Unreleased

### Added

- Public contribution governance and automated DCO enforcement.
- Python developer quickstart and executable public SDK examples.
- Release-readiness policy and alpha release documentation.
- Machine-checkable `0.1.0-alpha` release-candidate identity.
- Deterministic double-build verification and SHA-256 candidate checksums.

### Changed

- Python release artifacts now explicitly include the Apache-2.0 license.
- Python source distributions are intentionally minimal and exclude repository test sources.

## 0.1.0-alpha

Frozen release-candidate family for the first externally consumable public SDK and interoperability draft surface. Python package version: `0.1.0a0`. Prepared tag: `v0.1.0-alpha.0`. The exact tag target remains unset until the post-merge `main` SHA passes the full release gate. No package, Git tag, or GitHub Release is created merely by this changelog entry; publication requires the explicit process in `RELEASING.md`.
