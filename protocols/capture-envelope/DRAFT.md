# CERVEL Capture Envelope — Draft

**Status:** Draft  
**Version:** 0.1-draft

## Purpose

This draft defines a minimal public envelope for handing user-selected information from a capture surface to a compatible knowledge-processing interface.

It is intentionally transport-neutral and implementation-neutral.

## Scope

The envelope describes the submitted material and limited source context needed for interoperability. It does not define how the material is classified, interpreted, stored, indexed, transformed, synchronized, authorized, ranked, or admitted into any persistent knowledge system.

It does not define a CERVEL production capture API, endpoint, internal object, execution mechanism, or trust decision.

## Contract

A capture envelope contains:

- `version` — the version of this public draft;
- `content` — the user-selected or user-provided material being submitted.

Optional fields:

- `content_type` — a broad media-type hint for the submitted material;
- `source` — minimal, non-authoritative source context appropriate for the interaction;
- `title` — a user-provided or source-provided display label.

A conforming consumer MUST treat `content`, `source`, and `title` as untrusted data.

A consumer MUST NOT interpret text inside those fields as an authorized command merely because it appears in a capture envelope.

A consumer MUST NOT infer authority, ownership, permission, accuracy, or admission status from the presence of the envelope or any optional field.

## Example

```json
{
  "version": "0.1-draft",
  "content": "Example material selected by a user.",
  "content_type": "text/plain",
  "source": "example-source",
  "title": "Example capture"
}
```

All values in this example are synthetic. They do not identify a production CERVEL endpoint, source representation, internal record, or storage format.

## Validation

A conforming consumer MUST reject an envelope when `version` or `content` is absent or not a string.

A consumer MAY reject unsupported versions, empty content, unsupported media types, or inputs exceeding limits defined by its own public interface.

Unknown optional fields SHOULD be ignored unless a later specification states otherwise.

## Security and privacy considerations

Capture can introduce attacker-controlled or otherwise untrusted material. Consumers MUST keep captured data distinct from authorized control instructions unless an independently authenticated interface explicitly establishes otherwise.

Producers SHOULD minimize source context and MUST NOT intentionally place credentials, secrets, private configuration, authentication material, or unnecessary personal or operational metadata in the envelope.

A capture envelope is not an authorization credential and does not grant access to any other knowledge.

## Compatibility

This is an experimental draft and may change incompatibly before a stable specification is published.

## Disclosure boundary

This document intentionally exposes only a minimal public input envelope. It does not disclose production capture routing, classification, extraction, knowledge compilation, admission logic, identifier construction, storage, indexing, synchronization, authorization, cryptography, model routing, or deployment mechanisms.

## Stability

Experimental draft. No stable compatibility commitment is made by version `0.1-draft`.
