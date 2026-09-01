# Public / Private Boundary

CERVEL Public is intentionally **not** a mirror of the production repository.

The purpose of this repository is to make CERVEL understandable, interoperable, and useful to developers while preserving security-sensitive implementation, unreleased research, confidential information, and proprietary production systems.

## Intended public surface

Subject to review and versioning, this repository may contain:

- architecture overviews;
- terminology and conceptual specifications;
- interoperability protocols;
- public schemas;
- SDK interfaces;
- reference clients and examples;
- import/export formats;
- conformance tests;
- selected connectors and integrations;
- selected local interoperability components.

## Not automatically public

The following categories require explicit review before publication and may remain private:

- production reasoning and ranking internals;
- knowledge-compilation algorithms and heuristics;
- enterprise permission and authority enforcement internals;
- synchronization cryptographic implementation and service internals;
- private deployment infrastructure;
- credentials, tokens, keys, endpoints, telemetry, or operational configuration;
- confidential customer, partner, user, or tenant information;
- unreleased research and experimental architecture;
- security-sensitive implementation details;
- material whose intellectual-property disclosure status has not been reviewed.

## Disclosure classification

Before moving material from a non-public source into this repository, maintainers should classify it:

- **GREEN** — deliberately approved for public disclosure.
- **YELLOW** — requires security, IP, product, or privacy review.
- **RED** — must remain non-public.

Absence from the RED list is not approval to publish. Publication requires an affirmative GREEN decision.

## Clean-room publication rule

Prefer writing public specifications and examples specifically for this repository rather than copying production source files wholesale. Public artifacts should describe the contract developers need without unintentionally importing internal comments, configuration, commit history, private dependencies, or implementation details.

## History boundary

The public repository should maintain its own commit history. Private repository history should not be pushed here merely to preserve ancestry.

## Secrets

No production secret belongs in this repository, including in examples, fixtures, test snapshots, commit messages, deleted files, or Git history.
