# CERVEL

**Persistent Knowledge Infrastructure for humans, organizations, AI, and machines.**

> Intelligence changes. Knowledge persists.

This repository is the deliberately reviewed public home for CERVEL developer-facing material.

CERVEL is built around a simple idea: durable knowledge should remain useful even as models, applications, and interfaces change.

## Start here

- `docs/python-quickstart.md` — five-minute Python quickstart using only the experimental public SDK and synthetic local examples.
- `docs/CONCEPTS.md` — public vocabulary for persistent knowledge, identity, source context, access, embodiments, capture, provenance, and traceability.
- `docs/ARCHITECTURE.md` — deliberately high-level public architecture.
- `docs/TRUST_PRINCIPLES.md` — security and trust expectations for public interfaces.
- `docs/SPECIFICATION_MODEL.md` — how concepts, draft specifications, and stable public contracts are separated.
- `docs/PUBLIC_PRIVATE_BOUNDARY.md` — the publication and disclosure boundary.
- `CONTRIBUTING.md` — contribution workflow, sign-off, licensing, and disclosure requirements.
- `GOVERNANCE.md` — maintainer decision boundary and public-repository governance.
- `CODE_OF_CONDUCT.md` — participation expectations.
- `RELEASING.md` — controlled alpha release gate and artifact policy.
- `CHANGELOG.md` — public change history and release family status.

## Repository status

CERVEL is in active development. Public material may evolve before stable releases.

The current Python SDK package metadata is `0.1.0a0`, corresponding to the first `0.1.0-alpha` release family. No package registry publication or GitHub Release is implied by the repository version alone; releases follow the explicit gate in `RELEASING.md`.

This repository is **not** a mirror of non-public CERVEL source or infrastructure. Only material explicitly published here should be treated as part of the public CERVEL surface.

## Public repository

```text
docs/        Public concepts, release notes, and documentation
protocols/   Approved interoperability contracts
schemas/     Approved public schemas
sdk/         Developer tooling for published interfaces
examples/    Public-safe examples
governance/  Public contribution-governance validation tooling
```

Every new public contract or implementation should pass disclosure, security, privacy, and intellectual-property review before publication.

## Specifications

Public concepts are informative. Normative interoperability behavior exists only when a versioned specification explicitly defines it.

`protocols/SPECIFICATION_TEMPLATE.md` provides the minimum structure expected for future public contracts. The presence of a concept or placeholder does not commit CERVEL to publish a corresponding internal component.

## License

Material published in this repository is licensed under the Apache License, Version 2.0 unless a more specific notice states otherwise. See `LICENSE` and `LICENSING.md`.

The Python wheel and source distribution also carry the Apache-2.0 license as part of the release artifact. The license applies only to material actually distributed in this public repository or package; it does not imply publication or licensing of non-public CERVEL technology.

## Security

Please do not publish suspected vulnerabilities or sensitive information in public issues. Follow `SECURITY.md` for coordinated disclosure.

## CERVEL

CERVEL is being developed as persistent, sovereign-by-design knowledge infrastructure.

**One persistent semantic world. Many embodiments. Many intelligences.**

Copyright © 2026 CSIX AI LABS LLC.
