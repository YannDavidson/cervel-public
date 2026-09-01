# Lookup Request Example

This example shows the experimental public Lookup Request without connecting to a production CERVEL service.

```json
{
  "version": "0.1-draft",
  "query": "example project notes",
  "limit": 5,
  "scope": "example-scope"
}
```

A compatible experiment can validate the request and hand it to an independently configured consumer. The request itself does not grant discovery or access rights and does not describe how results are found or ranked.

The example does not demonstrate a CERVEL production endpoint, index, retrieval algorithm, ranking function, authorization mechanism, context construction, model routing, or storage system.
