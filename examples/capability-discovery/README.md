# Capability Discovery Example

This synthetic example declares only public contract/version pairs.

```json
{
  "version": "0.1-draft",
  "contracts": [
    {
      "name": "lookup-request",
      "version": "0.1-draft"
    },
    {
      "name": "lookup-result",
      "version": "0.1-draft"
    }
  ]
}
```

The declaration does not identify a production CERVEL node, service, environment, customer, model, agent, entitlement, deployment, or security state.

A declared contract is not an authorization credential and does not guarantee service health or caller access.
