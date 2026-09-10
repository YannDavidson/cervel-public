# PyPI Trusted Publishing

CERVEL Public publishes Python distributions to PyPI only through a dedicated GitHub Actions Trusted Publisher using OpenID Connect (OIDC). Long-lived PyPI API tokens are not part of the publication path.

## Trusted Publisher identity

Configure PyPI to trust exactly this GitHub Actions identity:

- owner: `YannDavidson`
- repository: `cervel-public`
- workflow: `publish-pypi.yml`
- environment: `pypi`
- PyPI project: `cervel-public`

For the first publication, a pending Trusted Publisher may be configured before the project exists. The pending publisher does not reserve the project name until the first successful publication.

## First alpha publication boundary

The first publishing workflow is intentionally release-specific. It can publish only the already-published GitHub prerelease `v0.1.0-alpha.0` / Python version `0.1.0a0`.

The workflow:

1. requires an explicit manual `workflow_dispatch` confirmation value;
2. runs inside the dedicated `pypi` GitHub environment;
3. grants `id-token: write` only to the publishing job;
4. checks out the immutable release tag and verifies the exact approved release commit;
5. downloads the wheel, canonical sdist, and `SHA256SUMS` from the existing GitHub prerelease;
6. requires the checksum file to match the frozen release checksums exactly;
7. verifies the downloaded wheel and sdist against those checksums;
8. reruns the repository distribution-boundary tests against the exact downloaded artifacts;
9. publishes only the wheel and sdist, never the checksum file;
10. uses an immutable commit pin for the PyPA publishing action;
11. enables PyPI attestations;
12. does not use `skip-existing`, so an accidental attempt to republish the same version fails instead of silently succeeding.

## Governance

Publication is an explicit release action, separate from merging this workflow. Merging this document and workflow must not publish anything by itself.

Before manually dispatching a publication, verify that the GitHub release, tag target, release asset digests, and PyPI Trusted Publisher configuration all match the approved release identity.

Published versions are immutable. Any correction must use a new prerelease serial and repeat the full review and release gate.
