# Changelog

All notable changes to the deliberately public CERVEL developer surface are recorded here.

The repository is pre-stable. Until a stable release is declared, public contracts and SDK surfaces may evolve between alpha releases. Versioned schemas and published compatibility statements remain authoritative for their stated versions.

## Unreleased

### Added

- Optional local JSON Schema validation helpers for the six deliberately published experimental contracts.
- Generic `validate_payload()` and non-throwing `validation_errors()` helpers.
- Specialized validators for Capture Envelope, Lookup Request, Knowledge Reference, Lookup Result, Error Envelope, and Capability Discovery.
- Local schema access through `get_public_schema()` and `SUPPORTED_CONTRACTS`.
- Structured validation exceptions and the optional `validation` dependency extra.

### Changed

- Prepared the next Python prerelease candidate as `0.1.0a1` / `0.1.0-alpha.1` without modifying the published `0.1.0a0` release.

## 0.1.0-alpha.1

Prepared next-alpha candidate for local public-contract validation helpers. Python package version: `0.1.0a1`. Prepared tag: `v0.1.0-alpha.1`. The candidate is not published merely by merging repository changes; publication remains a separate explicit release action.

## 0.1.0-alpha

First externally consumable public SDK and interoperability draft release family. Python package version: `0.1.0a0`. Published tag: `v0.1.0-alpha.0`. The published package and tag are immutable; later corrections or additions use a new prerelease serial.
