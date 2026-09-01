# Error Envelope Example

This example shows the experimental public Error Envelope without connecting to a production CERVEL service.

```json
{
  "version": "0.1-draft",
  "code": "example_error",
  "message": "Synthetic example error."
}
```

The code is intentionally implementation-defined. The envelope does not reveal or establish authentication state, authorization state, internal failure cause, resource existence, service topology, or retry safety.

The example does not demonstrate a production CERVEL error taxonomy, exception hierarchy, security decision, endpoint, internal identifier, or operational diagnostic.
