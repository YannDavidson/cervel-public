# Public model adapters

CERVEL's public developer surface includes a deliberately thin model-adapter boundary so developers can experience model-replacement continuity without exposing the proprietary CERVEL runtime.

The knowledge layer and reasoning model remain separate. The sandbox captures and looks up public experimental knowledge records. A model adapter receives only the lookup context returned through that public surface and translates it into a provider request.

## Switch the reasoning model, not the knowledge

Run the sandbox and capture records once using `LocalClient`:

```bash
cervel dev
```

Ask the same local knowledge with Ollama:

```bash
cervel ask "What do we know about Project Atlas?" --model ollama:llama3
```

Then select a developer-owned OpenAI model without recapturing or migrating the sandbox knowledge:

```bash
export OPENAI_API_KEY="..."
cervel ask "What do we know about Project Atlas?" --model openai:YOUR_MODEL --send-context-to-cloud
```

The cloud path is deliberately explicit. CERVEL does not store, broker, or manage the API key. The key is read from the developer's environment at execution time. Public sandbox context is not sent to a cloud provider unless the developer passes `--send-context-to-cloud`.

For another reviewed OpenAI-compatible HTTPS endpoint, the developer may set `--openai-base-url` and optionally `--openai-api-key-env`. Credentials in URLs, plaintext configuration files, and non-HTTPS cloud endpoints are rejected by this public adapter.

This is runtime selection, not a persisted default. The selected model belongs to the invocation; the public knowledge remains in the same sandbox. The current sandbox is in-memory and therefore does not claim durable persistence across sandbox restarts.

## Architectural boundary

This interface demonstrates one claim: knowledge can remain stable while the reasoning engine is replaceable.

It is **not** the CERVEL Intelligence Gateway. It does not expose or reproduce production routing, permission-aware activation/MSAKS, proprietary context compilation/CCP behavior, CKO or CKURI internals, production retrieval/ranking, durable Vault persistence, agent orchestration, provenance machinery, authentication, hidden endpoints, or CERVEL-managed provider credentials.

`ModelAdapter` remains provider-neutral. The public implementations translate already-returned public lookup context into developer-selected model requests. They do not decide what knowledge should activate, compile a proprietary context package, or route among models automatically.
