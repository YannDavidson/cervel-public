# Public Conformance Fixtures

These fixtures exercise selected validation boundaries of the experimental public contracts.

They are intentionally synthetic. They do not contain production identifiers, endpoints, credentials, private configuration, customer data, internal object structures, ranking signals, permission state, or unreleased implementation details.

## Layout

Each contract directory contains a small set of `valid-*.json` and `invalid-*.json` examples.

Invalid fixtures are accompanied by `EXPECTATIONS.md`, which states why each example is expected to fail. This avoids encoding production behavior into the fixture itself.

## Scope

The fixtures test public contract shape only. They do not test or disclose production retrieval, knowledge compilation, admission, authorization, provenance computation, synchronization, cryptography, model routing, storage, or deployment behavior.

Passing every fixture is not a claim of compatibility with a private CERVEL implementation.
