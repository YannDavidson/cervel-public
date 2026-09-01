# CERVEL

**Persistent Knowledge Infrastructure for humans, organizations, AI, and machines.**

> Intelligence changes. Knowledge persists.

This repository is the public home for CERVEL's developer-facing specifications, protocols, schemas, examples, and interoperability work.

CERVEL is designed around a simple architectural belief: durable knowledge should not be trapped inside a particular model, agent, application, or document store. Knowledge should persist independently, retain provenance and permissions, and remain usable as intelligence changes.

## Repository status

CERVEL is currently in active alpha development. This public repository is being established deliberately. Public interfaces and specifications may evolve before a stable release.

The production CERVEL implementation is maintained separately. This repository does **not** contain the complete production runtime, proprietary reasoning implementation, enterprise control plane, private infrastructure, credentials, or unreleased research.

## Public architecture

The public CERVEL surface is organized around interoperable contracts rather than a specific reasoning model:

- **Knowledge objects** — durable semantic objects that can be referenced independently of applications and models.
- **Capture** — normalized ingestion boundaries for information entering CERVEL.
- **Embodiments** — browser, desktop, mobile, agent, API, and machine interfaces to the same persistent knowledge world.
- **Provenance** — evidence describing where knowledge came from and how it moved through the system.
- **Permissions** — explicit boundaries governing what knowledge an identity may activate or access.
- **Trace** — developer-facing evidence connecting outputs back to supporting knowledge.
- **Model neutrality** — intelligence can change without requiring the underlying knowledge to disappear with it.

## What will live here

```text
docs/        Public architecture and concepts
protocols/   Interoperability contracts
schemas/     Public data schemas
sdk/         Developer-facing SDKs and clients
examples/    Minimal integration examples
```

The initial public foundation is being developed through pull requests so that disclosure boundaries can be reviewed before additional material reaches `main`.

## License

No open-source license has been granted yet. Until a license is explicitly added, all rights are reserved. The eventual licensing model for specifications, SDKs, and executable components is under review and may differ by component.

## Security

Please do not publish suspected vulnerabilities, credentials, private endpoints, or sensitive implementation details in public issues. A coordinated disclosure policy is being added in `SECURITY.md`.

## CERVEL

CERVEL is being developed as persistent, sovereign-by-design knowledge infrastructure.

**One persistent semantic world. Many embodiments. Many intelligences.**

Copyright © 2026 CSIX AI LABS LLC. All rights reserved.
