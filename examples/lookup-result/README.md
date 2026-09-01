# Lookup Result Example

This example shows the experimental public Lookup Result without connecting to a production CERVEL service.

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

The result can carry a public Knowledge Reference plus optional display text. Neither the result envelope nor its ordering or text establishes correctness, authority, permission, or completeness.

The example does not demonstrate production retrieval, ranking, scoring, authorization, context construction, provenance computation, model routing, or storage.
