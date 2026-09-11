# CERVEL Public Python SDK — Experimental

This directory contains a deliberately small Python convenience layer for the public CERVEL `0.1-draft` interoperability contracts.

The SDK mirrors the fields already published in the repository's example JSON Schemas. The schemas remain authoritative for the public drafts; these Python classes and validation helpers are convenience representations only.

## Scope

Included models:

- `KnowledgeReference`
- `CaptureEnvelope`
- `LookupRequest`
- `LookupResult` and `LookupResultItem`
- `ErrorEnvelope`
- `CapabilityDiscovery` and `CapabilityContract`

Each model exposes `to_dict()` for JSON-compatible serialization.

The prepared `0.1.0a1` candidate also includes optional, purely local contract-validation helpers:

- `validate_payload(contract, value)`
- `validate_capture_envelope()`
- `validate_lookup_request()`
- `validate_knowledge_reference()`
- `validate_lookup_result()`
- `validate_error_envelope()`
- `validate_capability_discovery()`
- `validation_errors()`
- `get_public_schema()`

The base SDK remains dependency-free. Once `0.1.0a1` is explicitly published, validation will be installed with the optional extra:

```bash
python -m pip install 'cervel-public[validation]==0.1.0a1'
```

Until then, the published PyPI release remains `0.1.0a0` and does not contain these helpers.

The validation extra uses the same public JSON Schema engine used by repository conformance. Validation is local only; it performs no network requests.

## Deliberate boundary

This SDK does **not** provide a CERVEL network client and does not implement authentication, authorization, capture processing, retrieval, ranking, knowledge compilation, provenance, persistence, synchronization, cryptography, model routing, agent behavior, storage, service topology, or any private CERVEL runtime mechanism.

It does not establish compatibility with a production CERVEL implementation. Compatibility claims are limited to the explicitly published experimental draft contracts and their conformance fixtures.

## Example

```python
from cervel_public import (
    KnowledgeReference,
    LookupResult,
    LookupResultItem,
    validate_lookup_result,
)

reference = KnowledgeReference(id="example-knowledge-1")
result = LookupResult(items=(LookupResultItem(reference=reference, text="Example"),))

payload = result.to_dict()
validate_lookup_result(payload)
```

The resulting payload is validated against the published Lookup Result schema, including its `$ref` to the public Knowledge Reference schema.

## Development and packaging verification

From the repository root, install the pinned validation and build dependencies:

```bash
python -m pip install -r conformance/requirements.txt -r sdk/python/requirements-build.txt
```

Then run the source contract checks and build both distribution formats:

```bash
python conformance/validator.py
python sdk/python/tests/test_conformance.py
python sdk/python/tests/test_validation.py
python -m build --no-isolation --sdist --wheel --outdir sdk/python/dist sdk/python
python sdk/python/tests/test_distribution.py
```

CI additionally installs the built base wheel into a fresh virtual environment with `--no-index --no-deps` and smoke-tests it from outside the repository source tree. This proves that the base artifact remains importable without the optional validation dependency and without accidentally resolving `cervel_public` from the checkout.

The base package declares no runtime dependencies. The `validation` extra directly pins `jsonschema==4.25.1`; its transitive dependencies are resolved by pip. Build tooling is directly pinned, but this experimental rollout does not claim a fully hash-locked or hermetic transitive Python dependency graph.

No package publication, artifact upload, external CERVEL service access, or production compatibility claim is performed by these checks.
