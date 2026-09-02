# CERVEL Capability Discovery — Draft

**Status:** Draft  
**Version:** 0.1-draft

## Purpose

This draft defines a minimal public document for declaring which published CERVEL interoperability drafts an implementation intentionally exposes at a public interface.

It is intentionally narrow. It does not describe private product capabilities, internal services, models, agents, storage, topology, security controls, deployment state, licensing, entitlement, or authorization.

## Contract

A capability discovery document contains:

- `version` — the version of this capability discovery draft;
- `contracts` — an array of declared public contract descriptors.

Each contract descriptor contains:

- `name` — a non-empty public contract name;
- `version` — a non-empty version string for that public contract.

An implementation MUST NOT treat the presence of a contract descriptor as proof that a caller is authenticated, authorized, entitled, or permitted to use the corresponding interface.

A consumer MUST NOT interpret a capability document as proof of service health, resource existence, private feature availability, internal topology, implementation identity, or compatibility with anything other than the explicitly declared public contract/version pairs.

A producer SHOULD declare only public contracts that it intentionally exposes at the interface where the capability document is obtained.

A producer MAY declare only a subset of the contracts listed in the repository's public protocol index.

## Example

```json
{
  "version": "0.1-draft",
  "contracts": [
    {
      "name": "lookup-request",
      "version": "0.1-draft"
    },
    {
      "name": "lookup-result",
      "version": "0.1-draft"
    }
  ]
}
```

All values are synthetic. This example does not identify a production CERVEL node, service, deployment, customer environment, or enabled private capability.

## Validation

A conforming consumer MUST reject a capability document when `version` is absent or unsupported, or when `contracts` is absent or not an array.

Each contract descriptor MUST be an object containing non-empty string values for `name` and `version`.

Unknown fields SHOULD be ignored unless a later specification states otherwise.

## Security and privacy considerations

Capability discovery can become an information-disclosure surface if it exposes private implementation detail.

Producers SHOULD keep declarations limited to intentionally public contract names and versions.

Producers MUST NOT intentionally include internal service names, hostnames, network addresses, deployment identifiers, model names, agent identities, storage details, security state, entitlement state, private feature flags, credentials, secrets, private configuration, or unrelated personal or operational metadata.

A capability document MUST NOT itself grant authority, permission, access, entitlement, or permission to invoke any operation.

Consumers SHOULD treat all externally supplied values as untrusted data.

## Compatibility

A declaration means only that the producer claims support for the named public contract/version at that public interface. It does not imply support for later versions, private implementations, or the complete CERVEL platform.

## Disclosure boundary

This document exposes only public contract names and versions. It does not expose routing, authentication, authorization, permissions, deployment topology, runtime state, model configuration, agent configuration, storage, synchronization, cryptography, observability, internal identifiers, or product entitlements.

## Stability

Experimental draft. No stable compatibility commitment is made by version `0.1-draft`.
