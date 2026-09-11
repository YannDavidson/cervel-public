# CERVEL Public Python SDK — API Reference

This document describes the deliberately public Python SDK surface. The currently published PyPI release is `cervel-public==0.1.0a0`; the repository is preparing `0.1.0a1`, which adds the optional local validation helpers documented below.

Install the current published alpha from PyPI:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install cervel-public==0.1.0a0
```

The prepared validation helpers will require the optional extra when `0.1.0a1` is explicitly published:

```bash
python -m pip install 'cervel-public[validation]==0.1.0a1'
```

## Public/private boundary

The Python package is a convenience layer over the published experimental CERVEL contracts. It provides immutable typed objects, JSON-compatible serialization helpers, and—starting with the prepared `0.1.0a1` candidate—optional local JSON Schema validation.

It does **not** implement or expose CERVEL networking, service endpoints, authentication, authorization, permission-aware activation, retrieval, ranking, persistence, provenance processing, knowledge compilation, synchronization, model routing, agent orchestration, private storage, or production runtime behavior.

The public JSON Schemas remain the authoritative contract surface. The Python classes and validators are developer conveniences that mirror the deliberately published example schemas.

## Public models

The model API remains unchanged from `0.1.0a0`:

```python
from cervel_public import (
    PUBLIC_DRAFT_VERSION,
    CapabilityContract,
    CapabilityDiscovery,
    CaptureEnvelope,
    ErrorEnvelope,
    KnowledgeReference,
    LookupRequest,
    LookupResult,
    LookupResultItem,
)
```

### `PUBLIC_DRAFT_VERSION`

```python
PUBLIC_DRAFT_VERSION == "0.1-draft"
```

The convenience models use this value as their default public contract version unless a field explicitly requires another value.

### `CaptureEnvelope`

```python
CaptureEnvelope(
    content: str,
    version: str = PUBLIC_DRAFT_VERSION,
    content_type: str | None = None,
    source: str | None = None,
    title: str | None = None,
)
```

Represents a public capture-envelope payload. Constructing it does not submit, store, synchronize, or persist anything. `to_dict()` returns a JSON-compatible dictionary and omits optional fields whose value is `None`.

### `LookupRequest`

```python
LookupRequest(
    query: str,
    version: str = PUBLIC_DRAFT_VERSION,
    limit: int | None = None,
    scope: str | None = None,
)
```

Represents the shape of a public lookup-request payload. Constructing it does not execute retrieval. `to_dict()` omits optional fields whose value is `None`.

### `KnowledgeReference`

```python
KnowledgeReference(
    id: str,
    version: str = PUBLIC_DRAFT_VERSION,
    kind: str | None = None,
    source: str | None = None,
)
```

Represents the public reference object used by lookup results. It does not expose internal identifiers, resolution services, provenance engines, permission checks, storage locations, or private CKURI behavior.

### `LookupResultItem`

```python
LookupResultItem(
    reference: KnowledgeReference,
    text: str | None = None,
)
```

Represents one item in a synthetic or externally obtained public lookup-result payload. `to_dict()` serializes the nested reference and omits `text` when it is `None`.

### `LookupResult`

```python
LookupResult(
    items: tuple[LookupResultItem, ...],
    version: str = PUBLIC_DRAFT_VERSION,
)
```

Represents a public lookup-result payload as an immutable tuple of `LookupResultItem` objects. The SDK does not retrieve, rank, authorize, score, enrich, or generate these items.

### `ErrorEnvelope`

```python
ErrorEnvelope(
    code: str,
    version: str = PUBLIC_DRAFT_VERSION,
    message: str | None = None,
)
```

Represents the public experimental error-envelope shape. It does not define transport semantics, HTTP status mapping, retry behavior, internal exceptions, or production error handling.

### `CapabilityContract`

```python
CapabilityContract(
    name: str,
    version: str,
)
```

Represents one advertised public contract name/version pair.

### `CapabilityDiscovery`

```python
CapabilityDiscovery(
    contracts: tuple[CapabilityContract, ...],
    version: str = PUBLIC_DRAFT_VERSION,
)
```

Represents a public capability-discovery document. It does not perform service discovery, endpoint negotiation, authentication, feature authorization, runtime routing, or private implementation introspection.

## Local contract validation — prepared for `0.1.0a1`

Validation is entirely local and operates only on the six schemas already published in `schemas/`. The base SDK remains dependency-free; validation uses the optional `validation` extra.

### `SUPPORTED_CONTRACTS`

The exact generic-validator contract names are:

```python
(
    "capture-envelope",
    "lookup-request",
    "knowledge-reference",
    "lookup-result",
    "error-envelope",
    "capability-discovery",
)
```

### `get_public_schema(contract)`

Returns a defensive copy of the embedded public schema for a supported contract. An unsupported contract raises `UnsupportedContractError`.

```python
from cervel_public import get_public_schema

schema = get_public_schema("lookup-request")
```

The embedded representations are not a second source of authority: repository tests require them to remain exactly equal to the corresponding published JSON files.

### `validate_payload(contract, value)`

Validates either a mapping or an SDK object exposing `to_dict()`.

```python
from cervel_public import LookupRequest, validate_payload

request = LookupRequest(query="When is the design review?", limit=3)
validate_payload("lookup-request", request)
```

The function returns `None` on success and raises `ContractValidationError` on schema failure.

### Specialized helpers

```python
validate_capture_envelope(value)
validate_lookup_request(value)
validate_knowledge_reference(value)
validate_lookup_result(value)
validate_error_envelope(value)
validate_capability_discovery(value)
```

Each is a thin local wrapper over `validate_payload()` using the corresponding published contract.

Example:

```python
from cervel_public import CaptureEnvelope, validate_capture_envelope

capture = CaptureEnvelope(
    content="The design review is scheduled for Friday.",
    content_type="text/plain",
)
validate_capture_envelope(capture)
```

### `validation_errors(contract, value)`

Returns a tuple of stable human-readable schema-error strings without raising for ordinary schema failures.

```python
from cervel_public import validation_errors

issues = validation_errors(
    "lookup-request",
    {"version": "0.1-draft", "query": "example", "limit": -1},
)
```

### Validation exceptions

- `ContractValidationError` — payload does not satisfy the selected public schema. Exposes `.contract` and `.errors`.
- `UnsupportedContractError` — caller requested a contract outside the deliberately supported public schema set.
- `ValidationDependencyError` — validation was invoked without the optional validation dependency installed.

## Immutability and serialization

All public SDK models are frozen Python dataclasses. After construction, their fields are not intended to be mutated.

Each model exposes `to_dict()` to produce JSON-compatible public data. For models with optional scalar fields, values set to `None` are omitted. Collection-bearing models serialize nested public objects recursively.

## Contract authority

When Python convenience behavior and a published JSON Schema are compared, the versioned public schema is the normative interoperability artifact. The SDK exists to make those published shapes easier to use from Python.

Validation helpers do not grant authority, access, permission, provenance status, or production compatibility. A payload passing a public schema means only that its public shape conforms to that experimental contract.

See also:

- `docs/python-quickstart.md` — end-to-end synthetic Python examples.
- `schemas/` — authoritative published JSON Schemas.
- `docs/PUBLIC_PRIVATE_BOUNDARY.md` — disclosure boundary.
- `docs/SPECIFICATION_MODEL.md` — distinction between concepts, drafts, and stable contracts.
