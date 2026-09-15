# Public model adapters

CERVEL's public developer surface includes a deliberately thin model-adapter boundary so developers can experience model-replacement continuity without exposing the proprietary CERVEL runtime.

The knowledge layer and reasoning model remain separate. The sandbox captures and looks up public experimental knowledge records. A model adapter receives only the lookup context returned through that public surface and translates it into a provider request.

## Switch the reasoning model, not the knowledge

Run the sandbox and capture records once using `LocalClient`:

```bash
cervel dev
```

By default, `cervel dev` stores its public sandbox records in `~/.cervel-public/sandbox.sqlite3`. Stop the process and start `cervel dev` again: the same local records and `local-*` references remain available. Developers may select another local database with `--db PATH`.

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

This is runtime model selection, not a persisted model default. The selected reasoning model belongs to the invocation; the public sandbox knowledge is stored separately.

## Restart continuity

The public developer sandbox now includes deliberately bounded local persistence. The restart proof is:

1. start `cervel dev` and capture a record;
2. record its returned `local-*` reference;
3. stop the sandbox process completely;
4. start `cervel dev` again against the same database;
5. look up the record and verify the same reference and content are returned;
6. ask with Ollama or explicitly switch to a configured cloud model without recapturing the knowledge.

The repository test suite performs this with two distinct server instances against one temporary SQLite database. This is local developer persistence only. It is not the proprietary CERVEL Vault, CKO storage model, production persistence topology, synchronization layer, or provenance system.

## Continuity proof demo

The repository includes `examples/python/model_replacement_continuity.py` as an observable model-switch proof. Run it against `cervel dev` with:

```bash
python examples/python/model_replacement_continuity.py --run --ollama-model llama3
```

That captures one synthetic Project Atlas record, snapshots the public lookup result, asks Ollama, performs the lookup again, and fails if the knowledge snapshot changed.

To demonstrate a local-to-cloud model switch against the same captured knowledge:

```bash
export OPENAI_API_KEY="..."
python examples/python/model_replacement_continuity.py \
  --run \
  --ollama-model llama3 \
  --cloud-model YOUR_MODEL \
  --send-context-to-cloud
```

The model outputs may differ; the public knowledge snapshot must not. No recapture or migration occurs between model calls. Restart continuity is independently enforced by the sandbox persistence tests described above.

## Architectural boundary

This public surface demonstrates two bounded claims: reasoning models can be replaced without moving the public sandbox knowledge, and the local sandbox knowledge can survive a developer sandbox restart.

It is **not** the CERVEL Intelligence Gateway or Vault. It does not expose or reproduce production routing, permission-aware activation/MSAKS, proprietary context compilation/CCP behavior, CKO or CKURI internals, production retrieval/ranking, production Vault persistence, synchronization, agent orchestration, provenance machinery, authentication, hidden endpoints, or CERVEL-managed provider credentials.

`ModelAdapter` remains provider-neutral. The public implementations translate already-returned public lookup context into developer-selected model requests. They do not decide what knowledge should activate, compile a proprietary context package, or route among models automatically.
