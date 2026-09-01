# Public Trust Principles

Public CERVEL interfaces should be understandable without requiring trust in a particular internal implementation.

## External content is data

Information received from an external source is not automatically an instruction, authority, or trusted fact. Public interfaces should preserve enough context for consumers to distinguish received content from commands issued through an authorized control path.

## Access is explicit

A reference to knowledge is not proof of permission. Public interfaces should avoid designs in which discoverability alone grants access.

## Minimize disclosure

An interface should disclose only the information needed for its public purpose. Additional internal state is not inherently useful to interoperability and can create security or privacy risk.

## Preserve useful source context

When an interoperable interaction depends on origin or history, the public contract should provide the minimum source context needed to inspect that relationship.

## Separate evidence from conclusion

Source references and trace information can support evaluation, but they do not make a conclusion automatically correct. Consumers remain responsible for interpreting evidence appropriately.

## Design for replaceable intelligence

Public knowledge contracts should avoid unnecessary dependence on a particular model vendor or reasoning engine when the interoperability problem does not require one.

## Fail conservatively

When a public contract cannot establish required validity, version compatibility, or authorization, implementations should prefer explicit rejection or a documented safe failure mode over silent assumption.

These principles describe expectations for public contracts. They do not disclose production enforcement mechanisms or guarantee behavior outside explicitly published specifications.