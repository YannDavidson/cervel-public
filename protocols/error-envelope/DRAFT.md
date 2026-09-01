# CERVEL Error Envelope — Draft

**Status:** Draft  
**Version:** 0.1-draft

## Purpose

This draft defines a minimal public envelope for reporting that a compatible public interaction did not complete successfully.

It is intentionally implementation-neutral. It does not define CERVEL production exceptions, internal failure states, security decisions, retry policy, service topology, or operational diagnostics.

## Contract

An error envelope contains:

- `version` — the version of this public draft;
- `code` — a non-empty, implementation-defined string suitable for programmatic comparison.

An error envelope may also contain:

- `message` — optional human-readable text intended for display or diagnostics at the public interface boundary.

A conforming consumer MUST treat `code`, `message`, and any unknown fields as untrusted data.

A consumer MUST NOT interpret an error envelope as proof of authentication state, authorization state, resource existence, internal topology, retry safety, or the cause of a private implementation failure beyond what the public interface explicitly documents.

The `code` value is intentionally not standardized by this draft. Implementations MAY define public error codes for their own interfaces.

## Example

```json
{
  "version": "0.1-draft",
  "code": "example_error",
  "message": "Synthetic example error."
}
```

All values are synthetic. They do not identify a production CERVEL error code, service, endpoint, resource, authorization decision, or operational condition.

## Validation

A conforming consumer MUST reject an error envelope when `version` is absent or unsupported, or when `code` is absent, not a string, or empty.

If present, `message` MUST be a string.

Unknown fields SHOULD be ignored unless a later specification states otherwise.

## Security and privacy considerations

Error responses can accidentally reveal sensitive implementation details. Producers SHOULD minimize `message` content and other optional metadata to what is necessary at the public interface boundary.

Producers MUST NOT intentionally include credentials, secrets, private configuration, authentication material, stack traces, private filesystem paths, internal service addresses, or unrelated personal or operational metadata.

An error envelope MUST NOT itself grant authority, permission, access, or permission to retry an operation.

## Compatibility

This is an experimental draft and may change incompatibly before a stable specification is published.

## Disclosure boundary

This document exposes only a minimal public failure envelope. It does not disclose production error taxonomies, exception hierarchies, security controls, authorization logic, retry mechanisms, service topology, observability systems, internal identifiers, storage, synchronization, cryptography, model routing, or deployment mechanisms.

## Stability

Experimental draft. No stable compatibility commitment is made by version `0.1-draft`.
