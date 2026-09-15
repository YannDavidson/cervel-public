# Changelog

All notable changes to the deliberately public CERVEL developer surface are recorded here.

The repository is pre-stable. Until a stable release is declared, public contracts and SDK surfaces may evolve between alpha releases. Versioned schemas and published compatibility statements remain authoritative for their stated versions.

## Unreleased

### Added

- Dependency-free Python `LocalClient` for the bounded localhost developer sandbox.
- `capabilities()`, `capture()`, and `lookup()` client methods returning existing public typed models.
- Loopback-only target enforcement and stable client failure types.
- Client success/failure tests, installed-wheel coverage, distribution checks, executable example, and API documentation.

### Changed

- Prepared the next Python prerelease candidate as `0.1.0a3` / `0.1.0-alpha.3` without modifying the published `0.1.0a2` release.

## 0.1.0-alpha.2

Published as Python package version `0.1.0a2` with tag `v0.1.0-alpha.2`. Added the CERVEL Local Developer Sandbox, `cervel dev`, loopback-only public capture/lookup/capability routes, ephemeral in-memory records, deterministic development-only lookup behavior, sandbox validation, and installed-wheel runtime verification.

## 0.1.0-alpha.1

Published as Python package version `0.1.0a1` with tag `v0.1.0-alpha.1`. Added optional purely local JSON Schema validation helpers for the six deliberately published experimental contracts, structured validation errors, local schema access, and the `validation` extra.

## 0.1.0-alpha

First externally consumable public SDK and interoperability draft release family. Python package version: `0.1.0a0`. Published tag: `v0.1.0-alpha.0`. The published package and tag are immutable; later corrections or additions use a new prerelease serial.
