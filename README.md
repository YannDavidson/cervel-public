# CERVEL

**Persistent Knowledge Infrastructure for humans, organizations, AI, and machines.**

> Intelligence changes. Knowledge persists.

This repository is the deliberately reviewed public home for CERVEL developer-facing material.

CERVEL is built around a simple idea: durable knowledge should remain useful even as models, applications, and interfaces change.

## Install it. Run it. Build against it.

The current published public alpha includes a bounded localhost developer sandbox. Install it from PyPI:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install 'cervel-public[sandbox]==0.1.0a2'
```

Start the sandbox:

```bash
cervel dev
```

It binds only to `127.0.0.1` and defaults to port `8765`.

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

Records exist only in process memory and disappear when the sandbox stops. Identifiers are synthetic local identifiers. Lookup behavior is deliberately simple and deterministic for developer compatibility testing; it is not CERVEL's production retrieval or ranking behavior.

See `docs/local-developer-sandbox.md` for the complete sandbox guide.

## Choose your developer mode

### Base SDK

Typed convenience models for the public experimental contracts, with no runtime dependencies:

```bash
python -m pip install cervel-public==0.1.0a2
```

### Local contract validation

Add local JSON Schema validation helpers:

```bash
python -m pip install 'cervel-public[validation]==0.1.0a2'
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

Install the runnable localhost compatibility target:

```bash
python -m pip install 'cervel-public[sandbox]==0.1.0a2'
cervel dev
```

## Deliberate public/private boundary

The local developer sandbox is a compatibility and development surface. It is **not** the proprietary CERVEL engine and does not establish compatibility with a production CERVEL deployment.

The public package deliberately does not expose or implement CERVEL's non-public authorization or permission-aware activation, persistence systems, provenance processing, Knowledge Compiler, context compilation, production retrieval or ranking, Intelligence Gateway, model routing, agent orchestration, private Vault internals, production identifiers, private storage, or service topology.

Public sandbox `scope` values are accepted only as public request data and are not interpreted as production authorization or permission semantics.

Only contracts and behavior explicitly published in this repository should be treated as part of the public CERVEL surface.

## Start here

- `docs/python-quickstart.md` — five-minute Python quickstart.
- `docs/python-sdk-api-reference.md` — complete public Python API reference.
- `docs/local-developer-sandbox.md` — install, run, and build against the bounded localhost sandbox.
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

The current published Python SDK release is `cervel-public==0.1.0a2`. Alpha.2 includes the bounded local developer sandbox described above.

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
