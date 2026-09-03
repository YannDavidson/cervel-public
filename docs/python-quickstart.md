# CERVEL Public Python SDK — 5-Minute Quickstart

This quickstart demonstrates the experimental public `0.1-draft` SDK as a local, typed representation of the published CERVEL interoperability contracts.

> The public JSON Schemas remain authoritative. These examples do not connect to a CERVEL service and do not describe production capture, retrieval, authorization, ranking, persistence, provenance, or other private runtime behavior.

## 1. Install the local SDK

From a clone of this repository:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install ./sdk/python
```

The package has no runtime dependencies.

## 2. Represent a capture envelope

```python
from cervel_public import CaptureEnvelope

capture = CaptureEnvelope(
    content="The design review is scheduled for Friday.",
    content_type="text/plain",
    title="Synthetic project note",
)

print(capture.to_dict())
```

This creates JSON-compatible data matching the published Capture Envelope draft. It does not submit or persist anything.

Run the repository example:

```bash
python examples/python/01_capture.py
```

## 3. Represent a lookup request

```python
from cervel_public import LookupRequest

request = LookupRequest(
    query="When is the design review?",
    limit=3,
    scope="public-example",
)

print(request.to_dict())
```

This represents a public Lookup Request payload only. No retrieval operation is performed.

```bash
python examples/python/02_lookup_request.py
```

## 4. Handle a synthetic lookup result

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

for item in result.items:
    print(item.reference.id, item.text)
```

The result above is deliberately synthetic. It illustrates how an application can consume the public SDK type without implying a public CERVEL endpoint or retrieval implementation.

```bash
python examples/python/03_synthetic_lookup_result.py
```

## 5. Run the complete local flow

The combined example constructs a Capture Envelope, a Lookup Request, and a synthetic Lookup Result in one script:

```bash
python examples/python/04_quickstart_flow.py
```

The flow is intentionally local:

```text
Capture Envelope
      ↓
application-controlled handoff (not implemented here)
      ↓
Lookup Request
      ↓
synthetic example result (not a service response)
      ↓
Lookup Result → Knowledge Reference
```

## Contract and execution boundary

The examples exercise only the public SDK objects already defined by the repository schemas. They contain no HTTP requests, credentials, endpoint URLs, service discovery, authentication, authorization, persistence, ranking, knowledge compilation, provenance engine, agent runtime, synchronization, model routing, or production compatibility claims.

CI executes every Python file published under `examples/python/` against the built and installed wheel so examples cannot silently drift from the installable SDK.