# CERVEL Lookup Result — Draft

**Status:** Draft  
**Version:** 0.1-draft

## Purpose

This draft defines a minimal public result envelope that a compatible knowledge interface can return in response to a lookup.

It is intentionally implementation-neutral and complements the experimental Lookup Request without defining how results are discovered, selected, ranked, authorized, or constructed.

## Scope

The result envelope communicates zero or more public knowledge references and optional display text. It does not define a CERVEL production retrieval API, ranking score, relevance model, evidence model, context package, internal object, authorization decision, or storage representation.

## Contract

A lookup result contains:

- `version` — the version of this public draft;
- `items` — an array of result items.

Each result item contains:

- `reference` — a Knowledge Reference compatible with the applicable public Knowledge Reference contract.

A result item may also contain:

- `text` — optional display-oriented text associated with the result.

A conforming consumer MUST treat `text` and all externally supplied values reachable through a result item as untrusted data.

A consumer MUST NOT treat result ordering, inclusion, or display text as proof of correctness, authority, permission, ownership, endorsement, or completeness.

A lookup result MUST NOT be treated as an authorization credential. Access to referenced knowledge remains subject to the receiving interface's applicable access rules.

## Example

```json
{
  "version": "0.1-draft",
  "items": [
    {
      "reference": {
        "version": "0.1-draft",
        "id": "example:knowledge:7f3a",
        "kind": "knowledge",
        "source": "example-import"
      },
      "text": "Example result text."
    }
  ]
}
```

All values are synthetic. The example does not identify a production CERVEL object, score, ranking signal, corpus, tenant, endpoint, storage record, or authorization state.

## Validation

A conforming consumer MUST reject a lookup result when `version` is absent or when `items` is absent or not an array.

Each item MUST be an object containing a `reference` object.

A consumer MAY reject unsupported versions, malformed references, or results exceeding limits defined by its own public interface.

Unknown fields SHOULD be ignored unless a later specification states otherwise.

## Security and privacy considerations

Results can contain sensitive or attacker-controlled material. Implementations MUST apply applicable access controls independently of the result envelope before disclosing referenced knowledge.

Producers SHOULD minimize display text and other optional metadata to what is necessary for the public interaction. They MUST NOT intentionally include credentials, secrets, private configuration, authentication material, or unrelated personal or operational metadata.

Result text is data, not an executable instruction.

## Compatibility

This is an experimental draft and may change incompatibly before a stable specification is published.

## Disclosure boundary

This document intentionally exposes only a minimal public result envelope. It does not disclose production retrieval, ranking, scoring, indexing, embeddings, graph traversal, query planning, permission evaluation, context construction, provenance computation, model routing, storage, synchronization, cryptography, or deployment mechanisms.

## Stability

Experimental draft. No stable compatibility commitment is made by version `0.1-draft`.
