# CERVEL Public Python SDK — API Reference

This document describes the deliberately public Python API shipped in `cervel-public==0.1.0a0`.

Install the current public alpha from PyPI:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install cervel-public==0.1.0a0
```

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

## Public/private boundary

The Python package is a convenience layer over the published experimental CERVEL contracts. It provides immutable typed objects and JSON-compatible serialization helpers.

It does **not** implement or expose CERVEL networking, service endpoints, authentication, authorization, permission-aware activation, retrieval, ranking, persistence, provenance processing, knowledge compilation, synchronization, model routing, agent orchestration, private storage, or production runtime behavior.

The public JSON Schemas remain the authoritative contract surface. The Python classes are developer conveniences that mirror the deliberately published example schemas.

## Version constant

### `PUBLIC_DRAFT_VERSION`

```python
PUBLIC_DRAFT_VERSION == "0.1-draft"
```

The convenience models use this value as their default public contract version unless a field explicitly requires another value.

---

## `CaptureEnvelope`

Represents a public capture-envelope payload. Constructing this object does not submit, store, synchronize, or persist anything.

```python
CaptureEnvelope(
    content: str,
    version: str = PUBLIC_DRAFT_VERSION,
    content_type: str | None = None,
    source: str | None = None,
    title: str | None = None,
)
```

Fields:

- `content` — required text content represented by the envelope.
- `version` — public contract version; defaults to `"0.1-draft"`.
- `content_type` — optional content-type label, such as `"text/plain"`.
- `source` — optional caller-supplied source label.
- `title` — optional caller-supplied title.

Example:

```python
from cervel_public import CaptureEnvelope

capture = CaptureEnvelope(
    content="The design review is scheduled for Friday.",
    content_type="text/plain",
    title="Synthetic project note",
)

payload = capture.to_dict()
```

`to_dict()` returns a JSON-compatible dictionary and omits optional fields whose value is `None`.

---

## `LookupRequest`

Represents the shape of a public lookup-request payload. Constructing it does not execute retrieval.

```python
LookupRequest(
    query: str,
    version: str = PUBLIC_DRAFT_VERSION,
    limit: int | None = None,
    scope: str | None = None,
)
```

Fields:

- `query` — required lookup text.
- `version` — public contract version; defaults to `"0.1-draft"`.
- `limit` — optional caller-supplied result limit.
- `scope` — optional public scope label.

Example:

```python
from cervel_public import LookupRequest

request = LookupRequest(
    query="When is the design review?",
    limit=3,
    scope="public-example",
)

payload = request.to_dict()
```

`to_dict()` omits optional fields whose value is `None`.

---

## `KnowledgeReference`

Represents a reference object used by the public lookup-result contract.

```python
KnowledgeReference(
    id: str,
    version: str = PUBLIC_DRAFT_VERSION,
    kind: str | None = None,
    source: str | None = None,
)
```

Fields:

- `id` — required reference identifier.
- `version` — public contract version; defaults to `"0.1-draft"`.
- `kind` — optional public type label.
- `source` — optional caller-supplied source label.

Example:

```python
from cervel_public import KnowledgeReference

reference = KnowledgeReference(
    id="example-knowledge-1",
    kind="note",
)
```

A `KnowledgeReference` is a public data structure only. It does not expose internal identifiers, resolution services, provenance engines, permission checks, storage locations, or private CKURI behavior.

---

## `LookupResultItem`

Represents one item in a synthetic or externally obtained public lookup-result payload.

```python
LookupResultItem(
    reference: KnowledgeReference,
    text: str | None = None,
)
```

Fields:

- `reference` — required `KnowledgeReference`.
- `text` — optional public text associated with the item.

Example:

```python
from cervel_public import KnowledgeReference, LookupResultItem

item = LookupResultItem(
    reference=KnowledgeReference(id="example-knowledge-1", kind="note"),
    text="The design review is scheduled for Friday.",
)
```

`to_dict()` serializes the nested reference and omits `text` when it is `None`.

---

## `LookupResult`

Represents a public lookup-result payload as an immutable tuple of `LookupResultItem` objects.

```python
LookupResult(
    items: tuple[LookupResultItem, ...],
    version: str = PUBLIC_DRAFT_VERSION,
)
```

Fields:

- `items` — required tuple of public result items.
- `version` — public contract version; defaults to `"0.1-draft"`.

Example:

```python
from cervel_public import KnowledgeReference, LookupResult, LookupResultItem

result = LookupResult(
    items=(
        LookupResultItem(
            reference=KnowledgeReference(id="example-knowledge-1", kind="note"),
            text="The design review is scheduled for Friday.",
        ),
    )
)

payload = result.to_dict()
```

The SDK does not retrieve, rank, authorize, score, enrich, or generate these items. The class only represents the published result shape.

---

## `ErrorEnvelope`

Represents the public experimental error-envelope shape.

```python
ErrorEnvelope(
    code: str,
    version: str = PUBLIC_DRAFT_VERSION,
    message: str | None = None,
)
```

Fields:

- `code` — required public error code.
- `version` — public contract version; defaults to `"0.1-draft"`.
- `message` — optional human-readable message.

Example:

```python
from cervel_public import ErrorEnvelope

error = ErrorEnvelope(
    code="example_error",
    message="Synthetic public example.",
)

payload = error.to_dict()
```

This object does not define transport semantics, HTTP status mapping, retry behavior, internal exceptions, or production error handling.

---

## Capability discovery

Capability discovery is represented by two public data classes: `CapabilityContract` and `CapabilityDiscovery`.

### `CapabilityContract`

Represents one advertised public contract name/version pair.

```python
CapabilityContract(
    name: str,
    version: str,
)
```

Example:

```python
from cervel_public import CapabilityContract

contract = CapabilityContract(
    name="capture-envelope",
    version="0.1-draft",
)
```

`to_dict()` returns:

```python
{
    "name": "capture-envelope",
    "version": "0.1-draft",
}
```

### `CapabilityDiscovery`

Represents a public capability-discovery document containing a tuple of `CapabilityContract` values.

```python
CapabilityDiscovery(
    contracts: tuple[CapabilityContract, ...],
    version: str = PUBLIC_DRAFT_VERSION,
)
```

Example:

```python
from cervel_public import CapabilityContract, CapabilityDiscovery

discovery = CapabilityDiscovery(
    contracts=(
        CapabilityContract(name="capture-envelope", version="0.1-draft"),
        CapabilityContract(name="lookup-request", version="0.1-draft"),
    )
)

payload = discovery.to_dict()
```

Capability discovery describes advertised public contract identifiers only. It does not perform service discovery, endpoint negotiation, authentication, feature authorization, runtime routing, or private implementation introspection.

---

## Immutability and serialization

All public SDK models are frozen Python dataclasses. After construction, their fields are not intended to be mutated.

Each model exposes `to_dict()` to produce JSON-compatible public data. For models with optional scalar fields, values set to `None` are omitted. Collection-bearing models serialize nested public objects recursively.

Example:

```python
from cervel_public import CaptureEnvelope

capture = CaptureEnvelope(content="Example")

assert capture.to_dict() == {
    "version": "0.1-draft",
    "content": "Example",
}
```

## Contract authority

When Python convenience behavior and a published JSON Schema are compared, the versioned public schema is the normative interoperability artifact. The SDK exists to make those published shapes easier to use from Python.

See also:

- `docs/python-quickstart.md` — end-to-end synthetic Python examples.
- `schemas/` — published JSON Schemas.
- `docs/PUBLIC_PRIVATE_BOUNDARY.md` — disclosure boundary.
- `docs/SPECIFICATION_MODEL.md` — distinction between concepts, drafts, and stable contracts.
