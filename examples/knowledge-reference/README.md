# Knowledge Reference Example

This example demonstrates the experimental public Knowledge Reference draft without connecting to a production CERVEL service.

```json
{
  "version": "0.1-draft",
  "id": "example:knowledge:7f3a",
  "kind": "knowledge",
  "source": "example-import"
}
```

A consumer can validate the envelope shape, retain the opaque `id`, and pass the reference through an integration that has independently established access to the underlying knowledge.

The example does not demonstrate resolution, authorization, storage, synchronization, model routing, or any other production CERVEL mechanism.
