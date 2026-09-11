# CERVEL

**Persistent Knowledge Infrastructure for humans, organizations, AI, and machines.**

> Intelligence changes. Knowledge persists.

This repository is the deliberately reviewed public home for CERVEL developer-facing material.

CERVEL is built around a simple idea: durable knowledge should remain useful even as models, applications, and interfaces change.

## Python SDK quickstart

Install the current published public alpha from PyPI:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install 'cervel-public[validation]==0.1.0a1'
```

Then use the typed public SDK and local contract validation:

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

## Local developer sandbox

The next prepared candidate adds a real localhost-only compatibility target without exposing the proprietary CERVEL engine. From a repository checkout:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e './sdk/python[sandbox]'
cervel dev
```

The sandbox starts at `http://127.0.0.1:8765` and exposes:

```text
GET  /capabilities
POST /capture
POST /lookup
```

It validates public-contract traffic, stores records only in process memory, and uses deliberately simple public lookup behavior that is unrelated to CERVEL's private retrieval/ranking systems. See `docs/local-developer-sandbox.md`.

The package and sandbox do not expose CERVEL's non-public authorization, permission-aware activation, persistence, provenance processing, knowledge compilation, production retrieval/ranking, routing, orchestration, or private storage systems.

## Start here

- `docs/python-quickstart.md` — five-minute Python quickstart.
- `docs/python-sdk-api-reference.md` — complete public Python API reference.
- `docs/local-developer-sandbox.md` — clone, run, and build against the bounded localhost sandbox.
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

The current published Python SDK release is `cervel-public==0.1.0a1`. The repository is preparing `0.1.0a2`, which adds the bounded local developer sandbox; it is not published merely by merging source changes.

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
