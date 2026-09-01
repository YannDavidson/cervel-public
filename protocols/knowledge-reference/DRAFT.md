# CERVEL Knowledge Reference — Draft

**Status:** Draft  
**Version:** 0.1-draft

## Purpose

This draft defines a minimal, implementation-neutral way for interoperating software to refer to a knowledge item without prescribing how CERVEL or another implementation stores, resolves, ranks, synchronizes, or authorizes that knowledge.

## Scope

This draft defines only a portable reference envelope. It does not define a database record, network endpoint, object lifecycle, authorization system, synchronization protocol, or production identifier format.

## Contract

A knowledge reference contains:

- `id` — an opaque string that identifies the referenced knowledge within the namespace understood by the producer and consumer;
- `version` — the version of this public reference contract.

Optional fields:

- `kind` — a non-authoritative hint describing the referenced material at a broad interoperability level;
- `source` — minimal source context suitable for the public interaction.

Consumers MUST treat `id` as opaque. They MUST NOT infer storage location, authority, permission, ownership, or trust from its syntax or possession.

Consumers MUST NOT treat `kind` or `source` as proof that the referenced knowledge is correct, accessible, or authoritative.

## Example

```json
{
  "version": "0.1-draft",
  "id": "example:knowledge:7f3a",
  "kind": "knowledge",
  "source": "example-import"
}
```

The example identifier and source are illustrative only. They do not represent a CERVEL production identifier, namespace, endpoint, storage key, or internal object.

## Validation

A conforming consumer MUST reject a reference when `version` or `id` is absent or not a string.

A consumer MAY reject unsupported versions. Unknown optional fields SHOULD be ignored unless a later specification states otherwise.

## Security and privacy considerations

A reference is not an authorization credential. Implementations MUST apply their own applicable access controls before returning referenced knowledge.

Producers SHOULD minimize source context and MUST NOT place credentials, secrets, private configuration, or unnecessary personal or operational metadata in the envelope.

External values MUST be treated as data rather than executable instructions.

## Compatibility

This is an experimental draft. It may change incompatibly before any stable specification is published.

## Disclosure boundary

This document intentionally exposes only the shape and interpretation of a minimal public reference. It does not disclose production identifier construction, resolution, storage, indexing, synchronization, authorization, cryptography, ranking, routing, or deployment mechanisms.

## Stability

Experimental draft. No stable compatibility commitment is made by version `0.1-draft`.
