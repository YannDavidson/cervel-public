from __future__ import annotations

import json
import tempfile
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

    def test_sqlite_store_survives_reinstantiation_with_stable_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "sandbox.sqlite3"
            first = SandboxStore(db_path)
            reference = first.capture(
                {
                    "version": "0.1-draft",
                    "content": "Project Atlas knowledge survives a sandbox restart.",
                    "source": "restart-test",
                }
            )
            self.assertEqual("local-000001", reference.id)

            restarted = SandboxStore(db_path)
            result = restarted.lookup(
                {"version": "0.1-draft", "query": "Atlas", "limit": 5}
            )
            self.assertEqual(1, len(result.items))
            self.assertEqual(reference.id, result.items[0].reference.id)
            self.assertEqual("restart-test", result.items[0].reference.source)
            self.assertEqual(
                "Project Atlas knowledge survives a sandbox restart.", result.items[0].text
            )

            second_reference = restarted.capture(
                {"version": "0.1-draft", "content": "A second durable record."}
            )
            self.assertEqual("local-000002", second_reference.id)


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


class SandboxRestartHTTPTests(unittest.TestCase):
    def test_new_server_reads_same_database_after_restart(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "sandbox.sqlite3"
            first = create_server(0, db_path=db_path)
            first_thread = threading.Thread(target=first.serve_forever, daemon=True)
            first_thread.start()
            first_base = f"http://{LOOPBACK_HOST}:{first.server_address[1]}"
            capture = urllib.request.Request(
                first_base + "/capture",
                method="POST",
                data=json.dumps(
                    {
                        "version": "0.1-draft",
                        "content": "Restart continuity belongs to the public local sandbox.",
                        "source": "http-restart-test",
                    }
                ).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(capture, timeout=2) as response:
                reference = json.loads(response.read())
            first.shutdown()
            first.server_close()
            first_thread.join(timeout=2)

            second = create_server(0, db_path=db_path)
            second_thread = threading.Thread(target=second.serve_forever, daemon=True)
            second_thread.start()
            try:
                second_base = f"http://{LOOPBACK_HOST}:{second.server_address[1]}"
                lookup = urllib.request.Request(
                    second_base + "/lookup",
                    method="POST",
                    data=json.dumps(
                        {"version": "0.1-draft", "query": "continuity", "limit": 5}
                    ).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                )
                with urllib.request.urlopen(lookup, timeout=2) as response:
                    result = json.loads(response.read())
                self.assertEqual(1, len(result["items"]))
                self.assertEqual(reference["id"], result["items"][0]["reference"]["id"])
                self.assertEqual(
                    "Restart continuity belongs to the public local sandbox.",
                    result["items"][0]["text"],
                )
            finally:
                second.shutdown()
                second.server_close()
                second_thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
