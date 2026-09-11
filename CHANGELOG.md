# Changelog

All notable changes to the deliberately public CERVEL developer surface are recorded here.

The repository is pre-stable. Until a stable release is declared, public contracts and SDK surfaces may evolve between alpha releases. Versioned schemas and published compatibility statements remain authoritative for their stated versions.

## Unreleased

### Added

- CERVEL Local Developer Sandbox with a `cervel dev` CLI.
- Loopback-only `GET /capabilities`, `POST /capture`, and `POST /lookup` endpoints.
- Ephemeral in-memory capture records and deterministic public token-overlap lookup behavior.
- Contract validation for sandbox requests and generated public responses.
- HTTP integration tests, installed-wheel CLI checks, and local sandbox documentation.
- Optional `sandbox` dependency extra.

### Changed

- Prepared the next Python prerelease candidate as `0.1.0a2` / `0.1.0-alpha.2` without modifying the published `0.1.0a1` release.

## 0.1.0-alpha.1

Published as Python package version `0.1.0a1` with tag `v0.1.0-alpha.1`. Added optional purely local JSON Schema validation helpers for the six deliberately published experimental contracts, structured validation errors, local schema access, and the `validation` extra.

## 0.1.0-alpha

First externally consumable public SDK and interoperability draft release family. Python package version: `0.1.0a0`. Published tag: `v0.1.0-alpha.0`. The published package and tag are immutable; later corrections or additions use a new prerelease serial.
