# Public Conformance Fixtures

These fixtures exercise selected validation boundaries of the experimental public contracts.

They are intentionally synthetic. They do not contain production identifiers, endpoints, credentials, private configuration, customer data, internal object structures, ranking signals, permission state, or unreleased implementation details.

## Layout

Each contract directory contains a small set of `valid-*.json` and `invalid-*.json` examples.

Invalid fixtures are accompanied by `EXPECTATIONS.md`, which states why each example is expected to fail. This avoids encoding production behavior into the fixture itself.

## Public validator

`validator.py` is an implementation-neutral test harness for the schemas and fixtures already published in this repository. It validates `valid-*.json` fixtures as valid and `invalid-*.json` fixtures as invalid.

The validator does not implement CERVEL runtime behavior and does not call a CERVEL service.

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r conformance/requirements.txt
python conformance/validator.py
```

To validate selected public contracts only:

```bash
python conformance/validator.py lookup-request lookup-result
```

A successful run exits with status `0`. Fixture expectation mismatches exit with status `1`. Setup, schema-loading, or argument errors exit with status `2`.

## Scope

The fixtures and validator test public contract shape only. They do not test or disclose production retrieval, knowledge compilation, admission, authorization, provenance computation, synchronization, cryptography, model routing, storage, deployment behavior, private identifiers, or internal topology.

Passing every fixture is not a claim of compatibility with a private CERVEL implementation, proof of security, or proof of complete protocol conformance.
