# CERVEL Public Python SDK — Experimental

This directory contains a deliberately small Python convenience layer for the public CERVEL `0.1-draft` interoperability contracts.

The SDK mirrors the fields already published in the repository's example JSON Schemas. The schemas remain authoritative for the public drafts; these Python classes are convenience representations only.

## Scope

Included models:

- `KnowledgeReference`
- `CaptureEnvelope`
- `LookupRequest`
- `LookupResult` and `LookupResultItem`
- `ErrorEnvelope`
- `CapabilityDiscovery` and `CapabilityContract`

Each model exposes `to_dict()` for JSON-compatible serialization.

## Deliberate boundary

This SDK does **not** provide a CERVEL network client and does not implement authentication, authorization, capture processing, retrieval, ranking, knowledge compilation, provenance, persistence, synchronization, cryptography, model routing, agent behavior, storage, service topology, or any private CERVEL runtime mechanism.

It does not establish compatibility with a production CERVEL implementation. Compatibility claims are limited to the explicitly published experimental draft contracts and their conformance fixtures.

## Example

```python
from cervel_public import KnowledgeReference, LookupResult, LookupResultItem

reference = KnowledgeReference(id="example-knowledge-1")
result = LookupResult(items=(LookupResultItem(reference=reference, text="Example"),))

payload = result.to_dict()
```

The resulting payload is expected to validate against the published Lookup Result schema, including its `$ref` to the public Knowledge Reference schema.

## Development and packaging verification

From the repository root, install the pinned validation and build dependencies:

```bash
python -m pip install -r conformance/requirements.txt -r sdk/python/requirements-build.txt
```

Then run the source contract checks and build both distribution formats:

```bash
python conformance/validator.py
python sdk/python/tests/test_conformance.py
python -m build --no-isolation --sdist --wheel --outdir sdk/python/dist sdk/python
python sdk/python/tests/test_distribution.py
```

CI additionally installs the built wheel into a fresh virtual environment with `--no-index --no-deps` and smoke-tests it from outside the repository source tree. This proves that the artifact itself is importable without accidentally resolving `cervel_public` from the checkout.

The package declares no runtime dependencies. Build tooling is directly pinned, but this experimental rollout does not claim a fully hash-locked or hermetic transitive Python dependency graph.

No package publication, artifact upload, external CERVEL service access, or production compatibility claim is performed by these checks.
