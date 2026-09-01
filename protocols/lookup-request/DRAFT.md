# CERVEL Lookup Request — Draft

**Status:** Draft  
**Version:** 0.1-draft

## Purpose

This draft defines a minimal public request envelope for asking a compatible knowledge interface to look up information using user-provided text.

It is intentionally implementation-neutral and does not define how matching, ranking, retrieval, filtering, authorization, or result construction are performed.

## Scope

The request describes only the public input needed to express a lookup. It does not define a CERVEL production search API, retrieval algorithm, index, embedding strategy, ranking function, authorization system, context compiler, or model interaction.

## Contract

A lookup request contains:

- `version` — the version of this public draft;
- `query` — the user-provided lookup text.

Optional fields:

- `limit` — a non-negative integer expressing a caller preference for the maximum number of returned items;
- `scope` — an opaque caller-provided scope hint whose interpretation, if supported, is defined by the receiving public interface.

A conforming consumer MUST treat `query` and `scope` as untrusted data.

A consumer MUST NOT interpret text inside `query` or `scope` as an authorized control instruction merely because it appears in a lookup request.

A lookup request MUST NOT be treated as proof that the caller is authorized to discover or access any knowledge.

The receiving implementation MAY return fewer items than `limit`, return no items, or reject the request according to its own public contract and applicable access rules.

## Example

```json
{
  "version": "0.1-draft",
  "query": "example project notes",
  "limit": 5,
  "scope": "example-scope"
}
```

All values in this example are synthetic. They do not identify a production CERVEL query format, namespace, corpus, tenant, index, endpoint, or authorization scope.

## Validation

A conforming consumer MUST reject a request when `version` or `query` is absent or not a string.

If present, `limit` MUST be an integer greater than or equal to zero.

A consumer MAY reject unsupported versions, empty queries, unsupported scope values, or limits outside constraints defined by its own public interface.

Unknown optional fields SHOULD be ignored unless a later specification states otherwise.

## Security and privacy considerations

Queries and scope hints can contain sensitive or attacker-controlled material. Implementations MUST apply their own applicable access controls before returning knowledge.

Producers SHOULD minimize unnecessary sensitive data and MUST NOT intentionally place credentials, secrets, private configuration, authentication material, or unrelated personal or operational metadata in the request.

The request does not authorize discovery, retrieval, disclosure, execution, or modification of any knowledge.

## Compatibility

This is an experimental draft and may change incompatibly before a stable specification is published.

## Disclosure boundary

This document intentionally exposes only a minimal public lookup input envelope. It does not disclose production retrieval, ranking, indexing, embeddings, graph traversal, query planning, authorization, permission evaluation, context construction, model routing, storage, synchronization, cryptography, or deployment mechanisms.

## Stability

Experimental draft. No stable compatibility commitment is made by version `0.1-draft`.
