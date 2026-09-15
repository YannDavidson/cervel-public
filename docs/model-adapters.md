# Public model adapters

CERVEL's public developer surface includes a deliberately thin model-adapter boundary so developers can experience model-replacement continuity without exposing the proprietary CERVEL runtime.

The knowledge layer and reasoning model remain separate. The sandbox captures and looks up public experimental knowledge records. A model adapter receives only the lookup context returned through that public surface and translates it into a provider request.

## Local-first demo

Run the sandbox:

```bash
cervel dev
```

Capture records using `LocalClient`, then run a local Ollama model in another terminal and ask:

```bash
cervel ask "What do we know about Project Atlas?" --model ollama:llama3
```

The command performs public sandbox lookup, converts the returned `LookupResultItem` values into provider-neutral `ModelContextItem` values, and sends that context to the developer's local Ollama endpoint.

## Architectural boundary

This interface demonstrates one claim: knowledge can remain stable while the reasoning engine is replaceable.

It is **not** the CERVEL Intelligence Gateway. It does not expose or reproduce production routing, permission-aware activation/MSAKS, proprietary context compilation/CCP behavior, CKO or CKURI internals, production retrieval/ranking, durable Vault persistence, agent orchestration, provenance machinery, authentication, hidden endpoints, or provider credentials.

The initial public alpha ships an Ollama adapter because it permits a fully local demonstration with no CERVEL-managed API key and no cloud-model dependency. The `ModelAdapter` protocol is intentionally provider-neutral so future reviewed adapters can be added without coupling the knowledge layer to a model vendor.

Provider API keys, when cloud adapters are added, remain developer-owned and must never be committed to the repository or routed through CERVEL's public sandbox.
