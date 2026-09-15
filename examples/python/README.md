# Python Examples

These examples use only the experimental public `cervel_public` SDK and synthetic data.

Run the contract examples after installing the local SDK as described in `docs/python-quickstart.md`:

```bash
python examples/python/01_capture.py
python examples/python/02_lookup_request.py
python examples/python/03_synthetic_lookup_result.py
python examples/python/04_quickstart_flow.py
```

Those examples demonstrate local construction and handling of published public contract objects only.

The opt-in model-replacement continuity example is different: it talks only to a developer's running loopback sandbox and developer-selected model adapters. Start `cervel dev`, then run:

```bash
python examples/python/model_replacement_continuity.py --run --ollama-model llama3
```

Add `--cloud-model YOUR_MODEL --send-context-to-cloud` (and a developer-owned API key in the configured environment variable) to prove a local-to-cloud reasoning-model switch against the same sandbox knowledge. The example compares public lookup snapshots before and after the switch and fails if they differ.

The sandbox itself now stores public development records in a bounded local SQLite database by default. Restart continuity is covered independently by tests that stop one server and instantiate another against the same database, verifying the same `local-*` reference and content survive without recapture. This local persistence is not the proprietary CERVEL Vault or production persistence architecture.

CI discovers and executes every `*.py` file in this directory against the built and installed wheel. The live continuity example therefore requires explicit `--run`; without it, CI verifies that the example imports and exits safely without contacting a sandbox or model provider.
