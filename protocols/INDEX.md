# CERVEL Public Protocol Index

This index describes only the deliberately published interoperability drafts in this repository. It is not a catalog of CERVEL production capabilities, internal services, or future product commitments.

## Experimental drafts

| Contract | Version | Status | Composition |
| --- | --- | --- | --- |
| Knowledge Reference | `0.1-draft` | Experimental | Standalone public reference envelope |
| Capture Envelope | `0.1-draft` | Experimental | Standalone public input envelope |
| Lookup Request | `0.1-draft` | Experimental | Standalone public lookup expression |
| Lookup Result | `0.1-draft` | Experimental | Contains Knowledge References |
| Error Envelope | `0.1-draft` | Experimental | Generic public failure envelope |

All indexed contracts are experimental and may change incompatibly before any stable specification is published.

## Composition model

A compatible experiment may use the drafts in a flow such as:

```text
Capture Envelope
      ↓
Lookup Request
      ↓
Lookup Result
      ↓
Knowledge Reference
```

An Error Envelope may be used by a compatible public interface to report an unsuccessful interaction. Its presence in the index does not define which operations can fail or how failures are produced internally.

The arrows express a possible public interoperability flow, not a required CERVEL production pipeline.

The only schema-level dependency currently defined is that each `reference` in a Lookup Result is governed by the applicable public Knowledge Reference contract.

## What the index does not claim

Listing a contract here does not mean that:

- every CERVEL implementation exposes it;
- an implementation supports every draft version;
- the drafts describe internal CERVEL objects or storage;
- a public message establishes authentication, authorization, trust, correctness, or admission into persistent knowledge;
- this index documents production topology, algorithms, models, security mechanisms, or deployment architecture.

Conformance is defined separately in `CONFORMANCE.md`.
