# Security Policy

Security, privacy, provenance, and permission boundaries are core concerns for CERVEL.

## Reporting a vulnerability

Please **do not** disclose suspected vulnerabilities through a public GitHub issue, discussion, pull request, social post, or other public channel.

If you believe you have found a security vulnerability, use GitHub's private vulnerability reporting feature for this repository when available. If that channel is unavailable, contact the CERVEL maintainers privately before disclosing technical details.

A useful report includes:

- the affected public component or protocol;
- the conditions required to reproduce the issue;
- the potential security or privacy impact;
- a minimal reproduction when safe to provide;
- whether you believe active exploitation is occurring.

Please avoid including real credentials, personal data, production knowledge, access tokens, private endpoints, or third-party secrets in reports.

## Scope

This policy covers artifacts published in `cervel-public`. The public repository is not the complete production CERVEL implementation, so a public artifact may describe an interface without exposing its production implementation.

Security reports concerning CERVEL-hosted services or non-public implementations should likewise be reported privately rather than reverse-engineered or publicly disclosed.

## Coordinated disclosure

We ask researchers to allow reasonable time for triage, remediation, validation, and coordinated disclosure before publishing vulnerability details.

## Security design principles

Public CERVEL work should preserve these boundaries:

1. captured external content is data, not executable instruction;
2. authorization and knowledge visibility are explicit;
3. provenance should survive movement across embodiments;
4. sensitive knowledge should not be disclosed merely because a model or agent can request it;
5. public examples must never contain production secrets or credentials.

Thank you for helping keep the CERVEL ecosystem secure.
