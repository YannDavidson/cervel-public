# Public Draft Conformance

This document defines a deliberately narrow meaning of conformance for the experimental public contracts in this repository.

It does not define conformance with CERVEL production infrastructure or certify an implementation as secure, authorized, complete, or endorsed by CERVEL.

## Contract conformance

An implementation claiming conformance with a specific public draft and version MUST:

1. identify the contract and version it claims to support;
2. satisfy that contract's required fields and validation requirements for the messages it produces;
3. enforce that contract's normative `MUST` and `MUST NOT` requirements applicable to its role;
4. not claim that conformance grants authority, permission, trust, correctness, or access beyond what the public contract states.

An implementation SHOULD document which optional fields and behaviors it supports.

An implementation MAY support only a subset of the public drafts. Supporting one contract does not imply support for another unless the claimed contract explicitly depends on it.

## Schema and prose

The prose draft is the normative public contract. Illustrative schemas and fixtures are provided to make the contract easier to inspect and test.

A schema or fixture MUST NOT be interpreted as granting semantics, authority, or guarantees that are absent from the corresponding prose contract.

If an illustrative schema or fixture conflicts with the prose draft, the conflict is a specification defect and SHOULD be reported rather than silently treated as a new contract rule.

## Fixtures

Fixtures under `conformance/fixtures/` are synthetic examples for testing public message shape and selected validation behavior.

A fixture marked `valid` SHOULD satisfy the corresponding public draft and illustrative schema at the version named by the fixture set.

A fixture marked `invalid` SHOULD violate the stated validation condition.

Passing the fixtures does not prove compatibility with private CERVEL implementations, production services, security controls, or unreleased behavior.

## Composition

When one public contract incorporates another, a conforming implementation MUST validate the incorporated structure according to the applicable published contract version when it claims conformance with that composition.

For `0.1-draft`, Lookup Result incorporates Knowledge Reference.

## Experimental status

All currently indexed contracts are experimental drafts. Conformance to a draft version is version-specific and does not imply compatibility with a later draft or stable specification.
