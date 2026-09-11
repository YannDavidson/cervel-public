# CERVEL Local Developer Sandbox

The local developer sandbox is a deliberately bounded compatibility surface for the public CERVEL experimental contracts. It is designed so developers can run a working local target, exercise capture and lookup flows, and build integrations without receiving or executing the proprietary CERVEL runtime.

## Install from a clone

Until `0.1.0a2` is explicitly published, install the prepared sandbox candidate from a repository checkout:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e './sdk/python[sandbox]'
cervel dev
```

The server binds only to `127.0.0.1` and defaults to port `8765`.

```text
http://127.0.0.1:8765
```

A different loopback port can be selected with `cervel dev --port 9000`. The alpha CLI intentionally does not provide a non-loopback host option.

## Public routes

### `GET /capabilities`

Returns a `CapabilityDiscovery` document declaring the six published experimental contracts understood by the sandbox.

### `POST /capture`

Accepts a public `CaptureEnvelope`, validates it locally, stores its `content` in ephemeral process memory, and returns a public `KnowledgeReference` with an opaque sandbox identifier such as `local-000001`.

```bash
curl -s http://127.0.0.1:8765/capture \
  -H 'Content-Type: application/json' \
  -d '{"version":"0.1-draft","content":"The design review is Friday."}'
```

### `POST /lookup`

Accepts a public `LookupRequest`, validates it locally, performs a deterministic case-insensitive token-overlap scan over the sandbox's in-memory records, and returns a public `LookupResult`.

```bash
curl -s http://127.0.0.1:8765/lookup \
  -H 'Content-Type: application/json' \
  -d '{"version":"0.1-draft","query":"Friday","limit":3}'
```

The matching rule exists only to make the public sandbox useful and predictable. It is not CERVEL retrieval, ranking, semantic activation, permission logic, knowledge compilation, or a representation of how the proprietary runtime works.

## Validation and errors

Every accepted request and generated public response is validated against the deliberately published JSON Schemas. Invalid requests fail closed with the public `ErrorEnvelope` shape.

The sandbox extra currently installs the same pinned `jsonschema==4.25.1` dependency used by the public validation helpers. The base `cervel-public` install remains dependency-free. If a developer runs `cervel dev` without sandbox validation support, the CLI exits and prints the exact `cervel-public[sandbox]` installation command.

## Ephemeral by design

All captured records live only in process memory. Stopping the server deletes them. There is no database, vault, cloud synchronization, filesystem persistence, account, tenant, credential, or hidden remote service behind the sandbox.

## Public/private boundary

The sandbox does **not** expose or implement CERVEL's non-public runtime, including permission-aware activation, production retrieval/ranking, persistence, provenance processing, knowledge compilation, synchronization, model routing, agent orchestration, service topology, production identifiers, or private storage.

Its purpose is narrower: give developers a real localhost target for the public interoperability contracts.

**Clone it. Run it. Build against it. Contribute.**
