# CERVEL Public Architecture

CERVEL is designed as a persistent semantic layer that remains independent from any single reasoning model, agent, application, or device.

This document describes the public architectural model. It intentionally does not specify proprietary production algorithms or internal enforcement implementations.

## Layer model

```text
World / Reality
      ↓
Embodiments
Browser · Desktop · Mobile · Agents · APIs · Machines
      ↓
Interactions
Capture · Search · Ask · Observe · Act
      ↓
Intelligence
Replaceable models and agents operating through governed interfaces
      ↓
Persistent Semantic Layer
Knowledge objects · Claims · Relationships · Events · State · Memory
Provenance · Permissions · Identity
      ↓
Storage / Transport
Local persistence · Encrypted synchronization · Organization-controlled nodes
```

The central architectural separation is between **persistent knowledge** and **replaceable intelligence**.

## Persistent knowledge

Information admitted into CERVEL can become a durable semantic object rather than remaining only a transient prompt or model conversation. Public specifications will progressively define interoperable representations for these objects and their evidence.

## Embodiments

An embodiment is an interface through which a human, agent, application, or machine interacts with the same underlying knowledge world.

A browser capture, desktop retrieval, mobile memory view, and agent context request should not require four unrelated copies of the same knowledge. The intended invariant is continuity of canonical knowledge identity across authorized embodiments.

## Provenance

Knowledge should carry evidence about its origin and transformation. Outputs that depend on knowledge should be capable of referring back to supporting evidence through traceable interfaces.

## Permissions

Access is not implied by possession of a model or connection to an agent. Implementations must evaluate the requesting identity and applicable knowledge scope before activation or disclosure.

## Model neutrality

CERVEL does not require persistent knowledge to belong to one model provider. Models are consumers and processors of scoped context; they are not the authoritative long-term container for the knowledge itself.

## Trust boundary

External captured content is treated as untrusted data. Capturing a webpage, document, message, or shared item must not convert instructions embedded in that content into trusted system commands.

## Public vs. production implementation

This repository can define contracts, schemas, expected behavior, compatibility rules, examples, and reference integrations. It should not be interpreted as a publication of every algorithm, enforcement mechanism, infrastructure component, optimization, enterprise feature, or research direction used by production CERVEL systems.
