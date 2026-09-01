# Contributing to CERVEL Public

Thank you for your interest in CERVEL.

This repository is the developer-facing public surface of a larger system. Contributions are welcome, but the project deliberately separates public interoperability work from non-public production implementation and unreleased research.

## Good contribution areas

We especially welcome contributions to:

- public specifications and protocol clarity;
- schema validation and compatibility tests;
- SDK ergonomics;
- examples and tutorials;
- import/export interoperability;
- documentation corrections;
- accessibility and internationalization;
- security improvements to public components.

## Before contributing code

For substantial proposals, open an issue describing the problem, intended public interface, compatibility implications, and why the capability belongs in the public layer.

Do not submit code or documentation copied from a private CERVEL repository, private communication, unreleased design document, partner deployment, or other non-public source unless the maintainers have explicitly approved that disclosure.

## Pull requests

Keep pull requests focused and explain:

1. what changes;
2. why it belongs in the public surface;
3. whether it changes a protocol or schema;
4. compatibility or migration implications;
5. security/privacy considerations;
6. how the change was tested.

## Public-boundary rule

The governing principle is:

> Open the interfaces deliberately. Do not assume the production implementation is public.

A public specification may define observable behavior without exposing proprietary implementation, internal ranking logic, private infrastructure, production credentials, unreleased research, or confidential partner information.

## Security

Do not report vulnerabilities publicly. Follow `SECURITY.md`.

## Licensing

The repository does not yet grant a general open-source license. Do not assume that publication alone grants permission to copy, modify, redistribute, or commercially use repository contents. Contribution licensing terms will be formalized before accepting external code contributions.

Until then, maintainers may decline external code contributions that create unclear ownership or licensing obligations.

## Conduct

Be constructive, technically specific, and respectful. The goal is to build infrastructure that developers and organizations can trust.
