from __future__ import annotations

import json
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
import sys

SDK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SDK_ROOT))

from cervel_public.sandbox import LOOPBACK_HOST, SandboxStore, create_server


class SandboxStoreTests(unittest.TestCase):
    def test_capture_lookup_and_capabilities(self) -> None:
        store = SandboxStore()
        capabilities = store.capabilities().to_dict()
        self.assertEqual("0.1-draft", capabilities["version"])
        self.assertEqual(6, len(capabilities["contracts"]))

        reference = store.capture({"version": "0.1-draft", "content": "Design review Friday"})
        self.assertEqual("local-000001", reference.id)

        result = store.lookup({"version": "0.1-draft", "query": "review", "limit": 3})
        self.assertEqual(1, len(result.items))
        self.assertEqual("Design review Friday", result.items[0].text)

    def test_lookup_limit_zero_returns_no_items(self) -> None:
        store = SandboxStore()
        store.capture({"version": "0.1-draft", "content": "alpha beta"})
        result = store.lookup({"version": "0.1-draft", "query": "alpha", "limit": 0})
        self.assertEqual((), result.items)


class SandboxHTTPTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server = create_server(0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://{LOOPBACK_HOST}:{self.server.server_address[1]}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def request(self, path: str, method: str = "GET", payload: dict | None = None):
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(self.base + path, method=method, data=data)
        if data is not None:
            request.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(request, timeout=2) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read())

    def test_http_capture_lookup_and_capability_flow(self) -> None:
        status, capabilities = self.request("/capabilities")
        self.assertEqual(200, status)
        self.assertEqual("0.1-draft", capabilities["version"])

        status, reference = self.request(
            "/capture",
            "POST",
            {"version": "0.1-draft", "content": "The design review is scheduled for Friday."},
        )
        self.assertEqual(201, status)
        self.assertEqual("local-000001", reference["id"])

        status, result = self.request(
            "/lookup",
            "POST",
            {"version": "0.1-draft", "query": "Friday", "limit": 5},
        )
        self.assertEqual(200, status)
        self.assertEqual(1, len(result["items"]))
        self.assertEqual(reference["id"], result["items"][0]["reference"]["id"])

    def test_invalid_capture_fails_closed_with_public_error_envelope(self) -> None:
        status, error = self.request("/capture", "POST", {"version": "0.1-draft"})
        self.assertEqual(400, status)
        self.assertEqual("invalid_request", error["code"])
        self.assertEqual("0.1-draft", error["version"])

    def test_unknown_route_uses_public_error_envelope(self) -> None:
        status, error = self.request("/private-runtime")
        self.assertEqual(404, status)
        self.assertEqual("sandbox_not_found", error["code"])


if __name__ == "__main__":
    unittest.main()
