# Main Branch Protection Policy

Status: required repository administration policy for `main` before the first public alpha tag.

## Purpose

The `main` branch is the authoritative public source for CERVEL release candidates and published releases. Changes to `main` must pass reviewable pull-request and automated conformance gates before merge.

## Required protections

Repository administration for `main` must enforce all of the following:

1. Require a pull request before merging.
2. Require these status checks before merging:
   - `DCO sign-off`
   - `Validate public schemas, SDK, examples, governance, and release candidate`
3. Require branches to be up to date before merging when GitHub supports that setting for the selected protection mode.
4. Prevent force pushes to `main`.
5. Prevent deletion of `main`.
6. Apply protections to repository administrators as well as ordinary contributors, except for a narrowly scoped emergency bypass defined below.

## Review policy

For the current single-maintainer alpha phase, branch protection does not require an additional approving reviewer beyond the repository owner. The pull-request requirement remains mandatory so that every change has a durable diff, CI record, DCO result, and merge event.

If additional maintainers gain merge authority, this policy should be revisited before granting them unrestricted bypass capability.

## Bypass policy

Routine owner/admin bypass is not permitted.

If GitHub Rulesets are used, the preferred configuration is no standing bypass actor. If operational constraints require an owner bypass, it should be configured as pull-request-only or emergency-only where GitHub supports that distinction, and must not be used for normal development or release preparation.

Any emergency bypass that changes `main` must be followed by a pull request or issue documenting:

- why bypass was necessary;
- the exact resulting commit SHA;
- which required checks were unavailable or intentionally bypassed;
- the validation performed immediately afterward.

## Release requirement

No first public alpha tag may be created until repository administration confirms that the protections in this document are active on `main` and the exact release commit has passed the required checks.

For `v0.1.0-alpha.0`, the release process remains governed by `RELEASING.md` and `release/alpha-0.1.0.json`.

## Verification

Before a release, verify repository administration state directly through GitHub and confirm:

- `main` is protected by branch protection or an active ruleset targeting `main`;
- pull requests are required;
- both required status checks are configured by their exact names;
- force pushes are blocked;
- branch deletion is blocked;
- bypass settings match this policy.

A policy file in the repository does not itself enable GitHub protection. Repository administration must be configured separately and verified after configuration.
