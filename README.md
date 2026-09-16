# CERVEL

**Persistent Knowledge Infrastructure for humans, organizations, AI, and machines.**

> Intelligence changes. Knowledge persists.

This repository is the deliberately reviewed public home for CERVEL developer-facing material.

CERVEL is built around a simple idea: durable knowledge should remain useful even as models, applications, and interfaces change.

## Install it. Run it. Restart it. Switch models.

The latest published Python SDK release is `cervel-public==0.1.0a3`. The current `main` branch moves beyond that published prerelease with developer-owned model adapters, observable model-replacement continuity, and bounded SQLite-backed local sandbox persistence.

To use the latest published package from PyPI:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install 'cervel-public[sandbox]==0.1.0a3'
```

To exercise the newest capabilities currently on `main`, including restart persistence and the latest model-switching work, install from a repository clone:

```bash
git clone https://github.com/YannDavidson/cervel-public.git
cd cervel-public
python -m venv .venv
source .venv/bin/activate
python -m pip install -e './sdk/python[sandbox]'
```

Start the bounded local sandbox:

```bash
cervel dev
```

It binds only to `127.0.0.1`, defaults to port `8765`, and on current `main` stores public sandbox records in:

```text
~/.cervel-public/sandbox.sqlite3
```

Use `cervel dev --db PATH` to select another local SQLite database.

Check the public capabilities:

```bash
curl http://127.0.0.1:8765/capabilities
```

Capture a synthetic local record:

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

The sandbox exposes the experimental public interoperability surface:

```text
GET  /capabilities
POST /capture
POST /lookup
```

On current `main`, records survive a complete sandbox process restart when the same local SQLite database is reused. Their synthetic `local-*` references remain stable, and new captures continue the durable local sequence. Lookup remains deliberately simple and deterministic for developer compatibility testing; it is not CERVEL's production retrieval or ranking behavior.

See `docs/local-developer-sandbox.md` for the complete sandbox guide.

## Replace the reasoning model, not the knowledge

Current `main` includes a public model-adapter surface for developer-selected reasoning models. A developer can keep knowledge in the local sandbox, ask with Ollama, and explicitly switch to a configured OpenAI-compatible cloud model without recapturing or migrating that knowledge.

Ask using a local Ollama model:

```bash
cervel ask "What do we know about Project Atlas?" --model ollama:llama3
```

Cloud model use is deliberately explicit. The developer supplies the provider credential at execution time and must explicitly consent to sending retrieved context to the cloud. CERVEL does not persist provider API keys.

The repository also includes an opt-in continuity demonstration:

```bash
python examples/python/model_replacement_continuity.py --run --ollama-model llama3
```

See `docs/model-adapters.md` for the model-adapter and continuity guide.

## Restart continuity

Current `main` includes bounded local SQLite persistence for the public sandbox. The observable developer flow is:

```text
capture knowledge
      ↓
stop cervel dev
      ↓
restart cervel dev
      ↓
retrieve the same local reference and content
      ↓
ask with Ollama
      ↓
switch reasoning model
      ↓
knowledge remains in the sandbox
```

The automated tests exercise restart continuity using two distinct server instances against the same temporary SQLite database and verify that the same public reference and content survive without recapture.

This is deliberately a **public developer persistence mechanism**, not the proprietary CERVEL Vault or production persistence architecture.

## Choose your developer mode

### Base SDK

Typed convenience models for the published public experimental contracts, with no runtime dependencies:

```bash
python -m pip install cervel-public==0.1.0a3
```

### Local contract validation

Add local JSON Schema validation helpers:

```bash
python -m pip install 'cervel-public[validation]==0.1.0a3'
```

Example:

```python
from cervel_public import CaptureEnvelope, validate_capture_envelope

capture = CaptureEnvelope(
    content="The design review is scheduled for Friday.",
    content_type="text/plain",
    title="Synthetic project note",
)
validate_capture_envelope(capture)
print(capture.to_dict())
```

### Local developer sandbox

For the published Alpha.3 sandbox:

```bash
python -m pip install 'cervel-public[sandbox]==0.1.0a3'
cervel dev
```

For the newest sandbox behavior on `main`, including durable local restart persistence, install from the repository clone as shown above.

## Deliberate public/private boundary

The local developer sandbox is a compatibility and development surface. It is **not** the proprietary CERVEL engine and does not establish compatibility with a production CERVEL deployment.

Current `main` implements bounded SQLite persistence only for public sandbox records. The public package does not expose or reproduce CERVEL's non-public authorization or permission-aware activation/MSAKS, production Vault persistence, CKO/CKURI internals, provenance processing, Knowledge Compiler, CCP/context compilation, production retrieval or ranking, Intelligence Gateway, production model routing, agent orchestration, synchronization, authentication, production identifiers, private storage semantics, or service topology.

Public sandbox `scope` values are accepted only as public request data and are not interpreted as production authorization or permission semantics.

Only contracts and behavior explicitly published in this repository should be treated as part of the public CERVEL surface.

## Start here

- `docs/python-quickstart.md` — five-minute Python quickstart.
- `docs/python-sdk-api-reference.md` — complete public Python API reference.
- `docs/local-developer-sandbox.md` — install, run, restart, and build against the bounded localhost sandbox.
- `docs/model-adapters.md` — developer-selected model adapters and continuity demonstrations.
- `docs/CONCEPTS.md` — public vocabulary for persistent knowledge and traceability.
- `docs/ARCHITECTURE.md` — deliberately high-level public architecture.
- `docs/TRUST_PRINCIPLES.md` — security and trust expectations for public interfaces.
- `docs/SPECIFICATION_MODEL.md` — separation of concepts, drafts, and stable public contracts.
- `docs/PUBLIC_PRIVATE_BOUNDARY.md` — publication and disclosure boundary.
- `CONTRIBUTING.md` — contribution workflow, sign-off, licensing, and disclosure requirements.
- `GOVERNANCE.md` — maintainer decision boundary and public-repository governance.
- `RELEASING.md` — controlled alpha release gate and artifact policy.
- `CHANGELOG.md` — public change history and release family status.

## Repository status

CERVEL is in active development. Public material may evolve before stable releases.

The latest published Python SDK release is `cervel-public==0.1.0a3`. Current `main` contains additional reviewed developer capabilities that have not yet been represented as a newer PyPI prerelease, including model switching and bounded local restart persistence.

This repository is **not** a mirror of non-public CERVEL source or infrastructure. Only material explicitly published here should be treated as part of the public CERVEL surface.

## Public repository

```text
docs/        Public concepts, release notes, and documentation
protocols/   Approved interoperability contracts
schemas/     Approved public schemas
sdk/         Developer tooling and bounded public sandbox
examples/    Public-safe examples
governance/  Public contribution-governance validation tooling
```

Every new public contract or implementation should pass disclosure, security, privacy, and intellectual-property review before publication.

## Specifications

Public concepts are informative. Normative interoperability behavior exists only when a versioned specification explicitly defines it.

`protocols/SPECIFICATION_TEMPLATE.md` provides the minimum structure expected for future public contracts. The presence of a concept or placeholder does not commit CERVEL to publish a corresponding internal component.

## License

Material published in this repository is licensed under the Apache License, Version 2.0 unless a more specific notice states otherwise. See `LICENSE` and `LICENSING.md`.

The Python wheel and source distribution also carry the Apache-2.0 license. The license applies only to material actually distributed in this public repository or package; it does not imply publication or licensing of non-public CERVEL technology.

## Security

Please do not publish suspected vulnerabilities or sensitive information in public issues. Follow `SECURITY.md` for coordinated disclosure.

## CERVEL

CERVEL is being developed as persistent, sovereign-by-design knowledge infrastructure.

**One persistent semantic world. Many embodiments. Many intelligences.**

Copyright © 2026 CSIX AI LABS LLC.
