# Contributing to CERVEL Public

Thank you for your interest in CERVEL.

This repository is a deliberately reviewed public developer surface. Contributions should improve material that is already public or propose new public-facing work without importing non-public CERVEL information.

Before contributing, read `GOVERNANCE.md`, `DCO.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and the repository licensing terms.

## Good contribution areas

We welcome improvements to public documentation, specifications, schemas, examples, compatibility tooling, accessibility, internationalization, and security of components that are explicitly published here.

## Before contributing

For substantial proposals, open an issue describing the public problem, intended interface, compatibility implications, validation approach, and any intellectual-property considerations that may affect publication.

Do not submit material copied or derived from private repositories, private communications, unreleased documents, confidential deployments, customer data, credentials, embargoed research, or other non-public sources unless the maintainers have explicitly approved that disclosure before it is pushed to a public branch.

If you are unsure whether information is public-safe, do not push it. Ask maintainers privately first.

## Pull requests

Keep pull requests focused and explain:

1. what changes;
2. why it belongs in the public surface;
3. compatibility implications;
4. security and privacy considerations;
5. licensing, provenance, and disclosure considerations;
6. how the change was validated.

Changes to published schemas, conformance tooling, SDK material, executable examples, or governance checks are expected to pass the applicable public CI gates before merge.

## DCO sign-off

External contributions must carry a Developer Certificate of Origin style sign-off on each contributed commit. Create signed-off commits with:

```bash
git commit -s -m "Describe the change"
```

The commit message must contain a trailer such as:

```text
Signed-off-by: Contributor Name <contributor@example.com>
```

The repository's `DCO sign-off` status check verifies every pull-request commit. If any commit is missing a valid trailer, update or recreate that commit with `git commit --amend -s` or an equivalent signed-off history edit, then push the corrected branch.

See `DCO.md` for what this certification means and how the automated gate is isolated from contributor code. A cryptographic Git signature does not replace the DCO trailer.

## Publication and IP boundary

> Publication is affirmative, not inferred.

Only material deliberately released in this repository should be treated as public CERVEL material. A public contract does not imply that related non-public implementation is open.

Because this repository is public, disclosure and IP review must happen before potentially sensitive material is pushed to a branch, not merely before merge. Maintainers may decline technically valid changes when publication could expose non-public implementation details, restricted information, patent-sensitive material, security-sensitive behavior, or commitments beyond the intended public contract.

External contribution does not create a right to merge, roadmap control, access to private systems, or disclosure of non-public technology. See `GOVERNANCE.md`.

## Security

Do not report vulnerabilities publicly. Follow `SECURITY.md`.

## Licensing and contributions

Material published in this repository is licensed under the Apache License, Version 2.0 unless a more specific notice states otherwise. See `LICENSE` and `LICENSING.md`.

Unless explicitly stated otherwise, a contribution intentionally submitted for inclusion in this repository is governed by Section 5 of Apache-2.0. Do not submit code, documentation, specifications, or other material unless you have the right to contribute it under those terms.

DCO sign-off supplements these license terms by recording the contributor's certification that they have the right to submit the material. It is not a Contributor License Agreement and does not transfer ownership of unrelated intellectual property.

## Conduct

Participation is governed by `CODE_OF_CONDUCT.md`. Be constructive, technically specific, and respectful.
