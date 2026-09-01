# CERVEL Public Concepts

CERVEL is built around one public thesis:

> Intelligence changes. Knowledge persists.

This document defines a small vocabulary for discussing that thesis without specifying non-public implementation.

## Persistent knowledge

**Persistent knowledge** is knowledge intended to remain useful beyond a single prompt, conversation, application session, device, or intelligence provider.

Persistence does not mean that knowledge is immutable or universally visible. Knowledge can change, expire, be corrected, become inaccessible, or be removed according to the rules of the system that manages it.

## Knowledge identity

A durable knowledge system benefits from being able to refer to a piece of knowledge consistently as applications and intelligence systems change around it.

A public contract may therefore provide a stable reference to knowledge. The format, lifecycle, storage representation, and resolution mechanism of any such reference are defined only by the corresponding published specification.

## Source context

Knowledge is more useful when consumers can understand where it came from. Public CERVEL contracts may carry source context sufficient for interoperable attribution or inspection.

Source context is not a claim that the source is correct. It provides context for evaluating or tracing knowledge.

## Access-aware use

The ability to reference knowledge does not imply permission to read or use it. Public interfaces should make authorization boundaries explicit and should avoid treating possession of an identifier as proof of access.

## Model independence

Persistent knowledge should not be permanently owned by one reasoning model. A compatible intelligence system may change while durable knowledge remains available through approved interfaces.

Model independence does not mean that every model receives the same information. Access, disclosure, and context remain governed by the applicable interface and authorization rules.

## Embodiments

An **embodiment** is a software or device experience through which a person or system interacts with persistent knowledge.

The term intentionally describes a role rather than a particular product implementation. Public specifications may define interoperability between embodiments without exposing how any production embodiment is built.

## Capture

**Capture** is the act of introducing information into a knowledge workflow through an approved interface.

Captured material should be treated according to its source and trust context. Receiving external content does not, by itself, make that content authoritative or executable.

## Provenance

**Provenance** is information that helps a consumer understand the origin or history relevant to a knowledge item or interaction.

Public provenance contracts should expose only what is necessary for interoperability and should not leak private operational metadata.

## Traceability

**Traceability** is the ability to connect an output or interaction to supporting public references when the applicable contract provides that capability.

Traceability is not a guarantee that an output is correct. It provides inspectable context that can support evaluation and accountability.

## What this document does not define

These concepts are intentionally implementation-neutral. They do not define production algorithms, databases, ranking methods, synchronization designs, cryptographic mechanisms, authorization internals, model-routing logic, deployment topology, or unreleased research.

Normative behavior exists only where a versioned specification in this repository explicitly defines it.