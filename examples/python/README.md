# Python Examples

These examples use only the experimental public `cervel_public` SDK and synthetic data.

Run them after installing the local SDK as described in `docs/python-quickstart.md`:

```bash
python examples/python/01_capture.py
python examples/python/02_lookup_request.py
python examples/python/03_synthetic_lookup_result.py
python examples/python/04_quickstart_flow.py
```

They demonstrate local construction and handling of published public contract objects only. They do not call a CERVEL endpoint, perform capture or retrieval, persist knowledge, apply authorization, rank results, or expose private runtime behavior.

CI discovers and executes every `*.py` file in this directory against the built and installed wheel.