# Public / Private Boundary

CERVEL Public is intentionally **not** a mirror of any non-public CERVEL repository.

Its purpose is to provide a useful developer-facing surface while preventing accidental disclosure of confidential, security-sensitive, proprietary, personal, or not-yet-reviewed material.

## Intended public surface

After review, this repository may contain:

- high-level concepts and documentation;
- deliberately published interoperability contracts;
- public schemas;
- developer interfaces and tools;
- examples using synthetic or public data;
- compatibility and conformance material.

Publication of one interface does not imply publication of the implementation behind it.

## Material that requires explicit approval

Do not publish material originating from non-public CERVEL work unless it has received an affirmative disclosure decision. This includes, without limitation:

- proprietary implementation details;
- security-sensitive design or operational information;
- private infrastructure or configuration;
- credentials, tokens, keys, non-public endpoints, or secrets;
- customer, partner, user, tenant, or personal information;
- unreleased research or product plans;
- material whose intellectual-property status has not been reviewed.

## Disclosure classification

Before material moves from a non-public source into this repository, classify it:

- **GREEN** — affirmatively approved for public disclosure.
- **YELLOW** — requires additional security, IP, product, or privacy review.
- **RED** — must remain non-public.

Absence from the RED list is not approval to publish. Publication requires an affirmative GREEN decision.

## Clean-room publication rule

Prefer creating public specifications and examples specifically for this repository. Do not copy private source trees, internal comments, configuration, fixtures, logs, documentation, or commit history merely because a related concept is intended to become public.

## History boundary

This repository maintains its own history. Non-public repository history must not be pushed here to preserve ancestry or convenience.

## Secrets

No production or private secret belongs in this repository, including in examples, fixtures, snapshots, commit messages, deleted files, branches, pull requests, issues, or Git history.