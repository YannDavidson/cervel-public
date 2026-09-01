# Public Specification Model

CERVEL Public separates conceptual documentation from normative interoperability contracts.

## Publication levels

Public material can have one of three roles:

### Concept

A concept explains vocabulary or architectural intent. Concept documents are informative and do not create compatibility requirements.

### Draft specification

A draft specification proposes an interoperable contract for review and experimentation. Drafts may change incompatibly and must identify themselves as drafts.

### Stable specification

A stable specification defines a versioned public contract with documented compatibility expectations. Stability applies only to the explicitly published surface.

## Normative language

Specifications may use the terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** to distinguish requirements from recommendations and optional behavior. A specification should define how it uses these terms.

Concept documents should avoid normative language where possible.

## Minimum specification contents

Before a public contract is treated as stable, its document should identify:

- its name and version;
- its purpose and scope;
- normative data or behavior exposed to interoperating implementations;
- validation requirements;
- compatibility expectations;
- security and privacy considerations;
- error or rejection behavior where interoperability depends on it;
- extension behavior, including treatment of unknown fields when applicable;
- disclosure status and stability level.

## Versioning

A public specification should change versions when a consumer that correctly implements the existing contract could no longer interoperate without modification.

Backward-compatible clarification does not necessarily require a new major version. Specifications should document their own versioning rules before stable release.

## Minimal disclosure

A specification should expose the smallest contract required for useful interoperability.

Public contracts should not reproduce internal database layouts, private configuration, operational topology, secret material, internal security state, proprietary algorithms, or implementation-specific metadata unless publication is independently necessary and explicitly approved.

## Implementation freedom

Conforming implementations may use different internal designs. Public compatibility is determined by the published contract, not by similarity to a CERVEL production implementation.

## No implied publication

Naming a concept or reserving a specification area does not commit CERVEL to publish an internal component. Only files explicitly released as public specifications define public contracts.