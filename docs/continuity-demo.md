# One-command continuity demo

Current `main` exposes the CERVEL public continuity proof as one CLI command:

```bash
cervel demo continuity
```

Prerequisites: install the repository development SDK with the `sandbox` extra and have Ollama running locally with the selected model (default: `llama3`). You do **not** need to start `cervel dev` separately.

The command creates a temporary local SQLite database, starts a loopback-only public sandbox, captures one synthetic Project Atlas record, stops that sandbox completely, starts a second sandbox against the same database, and verifies that the same synthetic reference and content are recovered. It then sends that recovered public context to the selected local Ollama model and verifies that the knowledge snapshot is still unchanged afterward.

The temporary demo database is removed when the command finishes. This keeps the proof isolated from the developer's normal `~/.cervel-public/sandbox.sqlite3` database.

## Local proof

```bash
cervel demo continuity --ollama-model llama3
```

Expected milestones include:

```text
✓ Knowledge captured: local-000001
✓ CERVEL sandbox stopped
✓ CERVEL sandbox restarted
✓ Same knowledge recovered: local-000001
✓ Reasoned with local model: ollama:llama3
✓ Knowledge unchanged after reasoning

PASS: CERVEL continuity verified.
```

The generated model text is not used as proof that knowledge persisted. The proof compares the public knowledge reference, source, and content before and after a complete sandbox restart and again after reasoning.

## Optional cloud model switch

A remote switch is opt-in and requires explicit context-transfer consent:

```bash
cervel demo continuity \
  --ollama-model llama3 \
  --cloud-model MODEL \
  --send-context-to-cloud
```

The cloud credential remains developer-owned and is read at execution time from `OPENAI_API_KEY` by default. Use `--cloud-api-key-env NAME` to select another environment variable and `--cloud-base-url HTTPS_URL` for a reviewed OpenAI-compatible HTTPS endpoint.

Supplying `--cloud-model` without `--send-context-to-cloud` is refused before the demo starts. The command does not persist provider API keys.

## Public/private boundary

This command demonstrates only the deliberately public developer invariant:

```text
capture once
   ↓
restart the public sandbox
   ↓
recover the same public reference and content
   ↓
reason with a local model
   ↓
optionally switch to an explicitly consented cloud model
   ↓
verify the public knowledge snapshot stayed unchanged
```

The SQLite store, synthetic `local-*` references, deterministic lookup, model adapters, and CLI orchestration are public developer mechanisms. They are not the proprietary CERVEL Vault, CKO/CKURI storage model, MSAKS, CCP, Knowledge Compiler, provenance system, production retrieval/ranking, Intelligence Gateway, synchronization architecture, production model routing, or agent orchestration.
