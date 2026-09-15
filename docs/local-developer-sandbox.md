# CERVEL Local Developer Sandbox

The local developer sandbox is a deliberately bounded compatibility surface for the public CERVEL experimental contracts. It is designed so developers can run a working local target, exercise capture and lookup flows, verify restart continuity, and build integrations without receiving or executing the proprietary CERVEL runtime.

## Install from a clone

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

## Local persistence

By default, the sandbox stores its public development records in:

```text
~/.cervel-public/sandbox.sqlite3
```

Use `cervel dev --db PATH` to select another SQLite database. The database contains only the bounded public sandbox record fields required for this compatibility surface. It is not the CERVEL Vault and does not reproduce CKO storage, provenance, permissions, synchronization, production topology, or private runtime semantics.

A record's `local-*` reference is derived from its durable local database sequence. If the sandbox process stops and later starts against the same database, the record keeps the same reference and content. New captures continue the sequence instead of reusing identifiers.

## Public routes

### `GET /capabilities`

Returns a `CapabilityDiscovery` document declaring the six published experimental contracts understood by the sandbox.

### `POST /capture`

Accepts a public `CaptureEnvelope`, validates it locally, stores its `content` in the selected local sandbox database, and returns a public `KnowledgeReference` with an opaque sandbox identifier such as `local-000001`.

```bash
curl -s http://127.0.0.1:8765/capture \
  -H 'Content-Type: application/json' \
  -d '{"version":"0.1-draft","content":"The design review is Friday."}'
```

### `POST /lookup`

Accepts a public `LookupRequest`, validates it locally, performs a deterministic case-insensitive token-overlap scan over the sandbox's local records, and returns a public `LookupResult`.

```bash
curl -s http://127.0.0.1:8765/lookup \
  -H 'Content-Type: application/json' \
  -d '{"version":"0.1-draft","query":"Friday","limit":3}'
```

The matching rule exists only to make the public sandbox useful and predictable. It is not CERVEL retrieval, ranking, semantic activation, permission logic, knowledge compilation, or a representation of how the proprietary runtime works.

## Restart proof

To verify persistence, capture a record and note its returned reference. Stop `cervel dev` completely, start it again against the same database, and repeat the lookup. The same reference and content should be returned without recapture.

The automated test suite performs the stronger form of this proof: it creates a first HTTP server, captures a record, shuts that server down, creates a distinct second server against the same temporary SQLite database, and verifies the same public reference and content are returned.

## Validation and errors

Every accepted request and generated public response is validated against the deliberately published JSON Schemas. Invalid requests fail closed with the public `ErrorEnvelope` shape.

The sandbox extra installs the same pinned `jsonschema==4.25.1` dependency used by the public validation helpers. The base `cervel-public` install remains dependency-free. If a developer runs `cervel dev` without sandbox validation support, the CLI exits and prints the exact `cervel-public[sandbox]` installation command.

## Public/private boundary

The sandbox implements only bounded local SQLite persistence for its public compatibility records. It does **not** expose or implement CERVEL's non-public runtime, including permission-aware activation, production retrieval/ranking, production Vault persistence, CKO/CKURI internals, provenance processing, knowledge compilation, synchronization, model routing, agent orchestration, service topology, production identifiers, authentication, or private storage semantics.

Its purpose remains narrow: give developers a real localhost target for the public interoperability contracts and an observable restart-continuity proof.

**Clone it. Run it. Restart it. Build against it. Contribute.**
