# CERVEL Public Python SDK — Experimental

The `cervel-public` package is the deliberately bounded Python developer layer for CERVEL's public `0.1-draft` interoperability contracts.

The public JSON Schemas remain authoritative. The Python models, local validation helpers, and localhost developer sandbox are convenience surfaces for building against the contracts that CERVEL has explicitly published.

Current published prerelease: `cervel-public==0.1.0a2`.

## Install it. Run it. Build against it.

For the quickest executable developer experience, install the sandbox extra in a fresh virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install 'cervel-public[sandbox]==0.1.0a2'
```

Start the bounded local sandbox:

```bash
cervel dev
```

The sandbox binds only to `127.0.0.1` and uses port `8765` by default.

In another terminal, inspect the published capabilities:

```bash
curl http://127.0.0.1:8765/capabilities
```

Capture a local in-memory record:

```bash
curl -X POST http://127.0.0.1:8765/capture \
  -H 'Content-Type: application/json' \
  -d '{
    "version":"0.1-draft",
    "content":"CERVEL knowledge should persist independently of the reasoning model.",
    "source":"developer-quickstart"
  }'
```

Look it up:

```bash
curl -X POST http://127.0.0.1:8765/lookup \
  -H 'Content-Type: application/json' \
  -d '{
    "version":"0.1-draft",
    "query":"knowledge persist",
    "limit":3
  }'
```

The sandbox exposes only:

- `GET /capabilities`
- `POST /capture`
- `POST /lookup`

Records live only in process memory and disappear when the sandbox stops. Identifiers are synthetic and local. Lookup is deliberately simple and deterministic; it is not CERVEL's production retrieval or ranking behavior.

## Installation modes

### Base SDK

```bash
python -m pip install cervel-public==0.1.0a2
```

The base SDK has no runtime dependencies. It provides public convenience models for the published experimental contracts.

### Local validation

```bash
python -m pip install 'cervel-public[validation]==0.1.0a2'
```

The validation extra provides purely local JSON Schema validation helpers. It performs no network requests.

### Local developer sandbox

```bash
python -m pip install 'cervel-public[sandbox]==0.1.0a2'
cervel dev
```

The sandbox extra enables the bounded localhost compatibility runtime described above.

## Public SDK surface

Included models:

- `KnowledgeReference`
- `CaptureEnvelope`
- `LookupRequest`
- `LookupResult` and `LookupResultItem`
- `ErrorEnvelope`
- `CapabilityDiscovery` and `CapabilityContract`

Each model exposes `to_dict()` for JSON-compatible serialization.

Optional local validation helpers include:

- `validate_payload(contract, value)`
- `validate_capture_envelope()`
- `validate_lookup_request()`
- `validate_knowledge_reference()`
- `validate_lookup_result()`
- `validate_error_envelope()`
- `validate_capability_discovery()`
- `validation_errors()`
- `get_public_schema()`

## Python example

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

## Deliberate public/private boundary

The local sandbox is a compatibility and developer surface. It is **not** the proprietary CERVEL engine and does not establish compatibility with a production CERVEL implementation.

The public package does not expose or implement CERVEL's non-public authorization or permission-aware activation behavior, persistence mechanisms, provenance processing, Knowledge Compiler, context compilation, production retrieval or ranking, Intelligence Gateway, model routing, agent orchestration, private Vault internals, production identifiers, private storage, service topology, or other unpublished runtime mechanisms.

The public sandbox may accept `scope` as public request data where the published schema permits it, but it does not interpret or enforce `scope` as production authorization or permission semantics.

Only contracts and behavior explicitly published in this repository are part of the public surface.

## Development and packaging verification

From the repository root, install the pinned validation and build dependencies:

```bash
python -m pip install -r conformance/requirements.txt -r sdk/python/requirements-build.txt
```

Then run the source contract checks, sandbox tests, and distribution verification:

```bash
python conformance/validator.py
python sdk/python/tests/test_conformance.py
python sdk/python/tests/test_validation.py
python sdk/python/tests/test_sandbox.py
python -m build --no-isolation --sdist --wheel --outdir sdk/python/dist sdk/python
python sdk/python/tests/test_distribution.py
```

CI additionally builds the release candidate reproducibly, verifies distribution contents, installs the built base wheel without network access, exercises the CLI, runs every published Python example, and exercises the installed sandbox wheel in a fresh environment.

The base package declares no runtime dependencies. The `validation` and `sandbox` extras directly pin `jsonschema==4.25.1`; its transitive dependencies are resolved by pip. Build tooling is directly pinned, but this experimental rollout does not claim a fully hash-locked or hermetic transitive Python dependency graph.

These checks do not expose private CERVEL services or turn the public compatibility surface into the proprietary production runtime.
