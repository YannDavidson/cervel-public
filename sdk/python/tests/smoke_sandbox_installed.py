from __future__ import annotations

import json
import threading
import urllib.request

from cervel_public.sandbox import LOOPBACK_HOST, create_server


server = create_server(0)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
base = f"http://{LOOPBACK_HOST}:{server.server_address[1]}"


def request(path: str, method: str = "GET", payload: dict | None = None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(base + path, method=method, data=data)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=2) as response:
        return response.status, json.loads(response.read())


try:
    status, capabilities = request("/capabilities")
    assert status == 200
    assert capabilities["version"] == "0.1-draft"

    status, reference = request(
        "/capture",
        "POST",
        {"version": "0.1-draft", "content": "Installed sandbox design review Friday"},
    )
    assert status == 201
    assert reference["id"] == "local-000001"

    status, result = request(
        "/lookup",
        "POST",
        {"version": "0.1-draft", "query": "Friday", "limit": 3},
    )
    assert status == 200
    assert len(result["items"]) == 1
    assert result["items"][0]["reference"]["id"] == reference["id"]
    print("PASS installed sandbox localhost capture -> lookup -> capability flow")
finally:
    server.shutdown()
    server.server_close()
    thread.join(timeout=2)
