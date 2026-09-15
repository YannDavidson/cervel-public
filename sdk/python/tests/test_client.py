from __future__ import annotations

import threading
import unittest
from pathlib import Path
from unittest import mock
import sys
import urllib.error

SDK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SDK_ROOT))

from cervel_public import (
    LocalClient,
    LocalClientConfigurationError,
    LocalClientConnectionError,
    LocalClientMalformedResponseError,
    LocalClientResponseError,
)
from cervel_public.sandbox import LOOPBACK_HOST, create_server


class _FakeResponse:
    def __init__(self, body: bytes, status: int = 200) -> None:
        self._body = body
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return self._body


class LocalClientIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server = create_server(0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.client = LocalClient(
            f"http://{LOOPBACK_HOST}:{self.server.server_address[1]}", timeout=2
        )

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def test_capabilities_capture_lookup_success(self) -> None:
        capabilities = self.client.capabilities()
        self.assertEqual("0.1-draft", capabilities.version)
        self.assertEqual(6, len(capabilities.contracts))

        reference = self.client.capture(
            "CERVEL knowledge should persist independently of the reasoning model.",
            source="local-client-test",
        )
        self.assertEqual("local-000001", reference.id)
        self.assertEqual("local-client-test", reference.source)

        result = self.client.lookup("knowledge persist", limit=3)
        self.assertEqual(1, len(result.items))
        self.assertEqual(reference.id, result.items[0].reference.id)

    def test_public_validation_error_is_exposed_as_response_error(self) -> None:
        with self.assertRaises(LocalClientResponseError) as context:
            self.client.lookup("example", limit=-1)
        self.assertEqual(400, context.exception.status)
        self.assertIsNotNone(context.exception.error)
        self.assertEqual("invalid_request", context.exception.error.code)


class LocalClientFailureTests(unittest.TestCase):
    def test_connection_failure_is_stable_client_exception(self) -> None:
        client = LocalClient()
        with mock.patch(
            "cervel_public.client.urllib.request.urlopen",
            side_effect=urllib.error.URLError("synthetic connection failure"),
        ):
            with self.assertRaises(LocalClientConnectionError):
                client.capabilities()

    def test_malformed_success_response_fails_closed(self) -> None:
        client = LocalClient()
        with mock.patch(
            "cervel_public.client.urllib.request.urlopen",
            return_value=_FakeResponse(b"not-json"),
        ):
            with self.assertRaises(LocalClientMalformedResponseError):
                client.capabilities()

    def test_malformed_contract_shape_fails_closed(self) -> None:
        client = LocalClient()
        with mock.patch(
            "cervel_public.client.urllib.request.urlopen",
            return_value=_FakeResponse(b'{"version":"0.1-draft","contracts":"wrong"}'),
        ):
            with self.assertRaises(LocalClientMalformedResponseError):
                client.capabilities()

    def test_non_loopback_target_is_rejected(self) -> None:
        with self.assertRaises(LocalClientConfigurationError):
            LocalClient("https://example.com")


if __name__ == "__main__":
    unittest.main()
