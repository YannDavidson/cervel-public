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

## Development

From the repository root, after installing `conformance/requirements.txt`, run:

```bash
python -m unittest discover -s sdk/python/tests -v
python conformance/validator.py
```

No package publication or external service access is performed by these tests.
