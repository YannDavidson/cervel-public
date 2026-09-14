# CERVEL Public Python SDK — API Reference

This document describes the deliberately public Python SDK surface in the repository. The currently published PyPI prerelease is `cervel-public==0.1.0a2`. The `LocalClient` described below is part of the repository development surface for the next prerelease; it is not yet present in the published alpha.2 package.

## Public/private boundary

The Python package is a convenience layer over the published experimental CERVEL contracts. It provides immutable typed objects, JSON-compatible serialization helpers, optional local JSON Schema validation, the bounded localhost sandbox, and a loopback-only client for that sandbox.

It does **not** expose or implement production authentication, authorization, permission-aware activation, persistence, provenance processing, Knowledge Compiler behavior, context compilation, production retrieval or ranking, Intelligence Gateway behavior, model routing, agent orchestration, private Vault internals, production identifiers, private storage, service topology, or other unpublished CERVEL runtime mechanisms.

The public JSON Schemas remain authoritative. The Python classes, validators, sandbox, and client are developer conveniences for the deliberately published public surface.

## Installation

Current published base SDK:

```bash
python -m pip install cervel-public==0.1.0a2
```

Current published validation and sandbox extras:

```bash
python -m pip install 'cervel-public[validation]==0.1.0a2'
python -m pip install 'cervel-public[sandbox]==0.1.0a2'
```

The base package remains dependency-free.

## Public models

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

All public models are frozen dataclasses and expose `to_dict()` for JSON-compatible serialization.

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

### `LookupRequest`

```python
LookupRequest(
    query: str,
    version: str = PUBLIC_DRAFT_VERSION,
    limit: int | None = None,
    scope: str | None = None,
)
```

`scope` is an opaque public field. The SDK and sandbox do not interpret it as production authorization or permission semantics.

### `KnowledgeReference`

```python
KnowledgeReference(
    id: str,
    version: str = PUBLIC_DRAFT_VERSION,
    kind: str | None = None,
    source: str | None = None,
)
```

### `LookupResultItem` and `LookupResult`

```python
LookupResultItem(reference: KnowledgeReference, text: str | None = None)
LookupResult(items: tuple[LookupResultItem, ...], version: str = PUBLIC_DRAFT_VERSION)
```

### `ErrorEnvelope`

```python
ErrorEnvelope(
    code: str,
    version: str = PUBLIC_DRAFT_VERSION,
    message: str | None = None,
)
```

### `CapabilityContract` and `CapabilityDiscovery`

```python
CapabilityContract(name: str, version: str)
CapabilityDiscovery(
    contracts: tuple[CapabilityContract, ...],
    version: str = PUBLIC_DRAFT_VERSION,
)
```

## Local contract validation

Validation operates only on the six published public schemas and requires the optional `validation` dependency.

Public helpers:

```python
SUPPORTED_CONTRACTS
get_public_schema(contract)
validate_payload(contract, value)
validate_capture_envelope(value)
validate_lookup_request(value)
validate_knowledge_reference(value)
validate_lookup_result(value)
validate_error_envelope(value)
validate_capability_discovery(value)
validation_errors(contract, value)
```

Exceptions:

- `ContractValidationError` — payload does not satisfy the selected public schema.
- `UnsupportedContractError` — contract is outside the deliberately supported public set.
- `ValidationDependencyError` — validation was invoked without the optional validation dependency installed.

## `LocalClient` — repository development surface

`LocalClient` is a dependency-free stdlib HTTP client for the existing public developer sandbox. It is intentionally restricted to loopback HTTP targets and defaults to `http://127.0.0.1:8765`.

```python
from cervel_public import LocalClient

client = LocalClient()

reference = client.capture(
    "CERVEL knowledge should persist independently of the reasoning model."
)

results = client.lookup("knowledge persist")
```

Start the sandbox separately with:

```bash
cervel dev
```

### Constructor

```python
LocalClient(
    base_url: str = "http://127.0.0.1:8765",
    *,
    timeout: float = 5.0,
)
```

Accepted hosts are limited to loopback names/addresses: `127.0.0.1`, `localhost`, and `::1`. Non-loopback targets are rejected. The client does not provide production service discovery or routing.

### `capabilities()`

```python
client.capabilities() -> CapabilityDiscovery
```

Calls only `GET /capabilities` and parses the published capability-discovery shape.

### `capture()`

```python
client.capture(
    content: str,
    *,
    content_type: str | None = None,
    source: str | None = None,
    title: str | None = None,
) -> KnowledgeReference
```

Calls only `POST /capture` using the public `CaptureEnvelope` shape and returns a public `KnowledgeReference`.

### `lookup()`

```python
client.lookup(
    query: str,
    *,
    limit: int | None = None,
    scope: str | None = None,
) -> LookupResult
```

Calls only `POST /lookup` using the public `LookupRequest` shape and returns a public `LookupResult`.

### Local client exceptions

- `LocalClientError` — base client exception.
- `LocalClientConfigurationError` — target or timeout violates the bounded local-client configuration.
- `LocalClientConnectionError` — loopback sandbox could not be reached.
- `LocalClientMalformedResponseError` — response is not valid UTF-8 JSON or does not match the expected public response shape.
- `LocalClientResponseError` — sandbox returned an HTTP error. Exposes `.status` and, when parseable, `.error` as an `ErrorEnvelope`.

A sandbox schema failure, such as `lookup(..., limit=-1)`, remains a public sandbox validation error and is surfaced through `LocalClientResponseError`; the client does not silently reinterpret or expand the published contract.

## Dependency boundary

`LocalClient` uses only Python's standard-library `urllib`, `json`, and URL parsing modules. Adding the client does not add a runtime dependency to the base SDK.

The client contains no credentials, authentication logic, authorization policy, permission-aware activation semantics, production endpoint knowledge, private CKO/CKURI behavior, persistence mechanism, model routing, or hidden production transport.

## Contract authority

When Python convenience behavior and a published JSON Schema are compared, the versioned public schema is the normative interoperability artifact. Passing a public schema means only that a payload conforms to that experimental public shape; it does not grant access, authority, provenance status, or production compatibility.

See also:

- `docs/python-quickstart.md`
- `docs/local-developer-sandbox.md`
- `schemas/`
- `docs/PUBLIC_PRIVATE_BOUNDARY.md`
- `docs/SPECIFICATION_MODEL.md`
