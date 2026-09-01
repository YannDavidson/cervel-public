# Capture Envelope Example

This example shows the experimental public Capture Envelope without sending data to a production CERVEL service.

```json
{
  "version": "0.1-draft",
  "content": "Example material selected by a user.",
  "content_type": "text/plain",
  "source": "example-source",
  "title": "Example capture"
}
```

A compatible experiment can validate the envelope and hand it to an independently configured consumer. The envelope itself does not establish trust, permission, authority, or admission into persistent knowledge.

The example does not demonstrate a CERVEL production endpoint, knowledge compilation, admission logic, storage, synchronization, authorization, model routing, or execution.
