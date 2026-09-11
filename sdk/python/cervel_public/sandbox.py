"""Local-only developer sandbox for the public CERVEL experimental contracts.

This module is deliberately not the CERVEL runtime. It provides a small,
in-memory compatibility surface for developers to exercise the published
contracts on localhost. It does not implement production retrieval, ranking,
authorization, persistence, provenance, knowledge compilation, routing, or
agent behavior.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .models import (
    PUBLIC_DRAFT_VERSION,
    CapabilityContract,
    CapabilityDiscovery,
    ErrorEnvelope,
    KnowledgeReference,
    LookupResult,
    LookupResultItem,
)
from .validation import (
    ContractValidationError,
    ValidationDependencyError,
    validate_capability_discovery,
    validate_capture_envelope,
    validate_error_envelope,
    validate_knowledge_reference,
    validate_lookup_request,
    validate_lookup_result,
)

DEFAULT_PORT = 8765
LOOPBACK_HOST = "127.0.0.1"


@dataclass(frozen=True)
class _StoredRecord:
    reference: KnowledgeReference
    content: str


class SandboxStore:
    """Ephemeral in-memory store for the public local developer sandbox."""

    def __init__(self) -> None:
        self._records: list[_StoredRecord] = []
        self._next_id = 1

    def capabilities(self) -> CapabilityDiscovery:
        discovery = CapabilityDiscovery(
            contracts=tuple(
                CapabilityContract(name=name, version=PUBLIC_DRAFT_VERSION)
                for name in (
                    "capture-envelope",
                    "lookup-request",
                    "lookup-result",
                    "knowledge-reference",
                    "error-envelope",
                    "capability-discovery",
                )
            )
        )
        validate_capability_discovery(discovery)
        return discovery

    def capture(self, value: Any) -> KnowledgeReference:
        validate_capture_envelope(value)
        payload = value.to_dict() if hasattr(value, "to_dict") else dict(value)
        reference = KnowledgeReference(
            id=f"local-{self._next_id:06d}",
            kind="sandbox-record",
            source=payload.get("source"),
        )
        validate_knowledge_reference(reference)
        self._next_id += 1
        self._records.append(_StoredRecord(reference=reference, content=payload["content"]))
        return reference

    def lookup(self, value: Any) -> LookupResult:
        validate_lookup_request(value)
        payload = value.to_dict() if hasattr(value, "to_dict") else dict(value)
        query = payload["query"]
        limit = payload.get("limit")

        # Deliberately simple sandbox behavior: case-insensitive token overlap.
        # This is public test-fixture logic, not CERVEL retrieval or ranking.
        tokens = {token for token in re.findall(r"[\w'-]+", query.casefold()) if token}
        matches: list[LookupResultItem] = []
        for record in self._records:
            text_tokens = set(re.findall(r"[\w'-]+", record.content.casefold()))
            if not tokens or tokens.intersection(text_tokens):
                matches.append(LookupResultItem(reference=record.reference, text=record.content))

        if limit is not None:
            matches = matches[:limit]
        result = LookupResult(items=tuple(matches))
        validate_lookup_result(result)
        return result


def _error(code: str, message: str) -> ErrorEnvelope:
    envelope = ErrorEnvelope(code=code, message=message)
    validate_error_envelope(envelope)
    return envelope


def make_handler(store: SandboxStore):
    class SandboxHandler(BaseHTTPRequestHandler):
        server_version = "CERVELPublicSandbox/0.1"

        def _send_json(self, status: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _read_json(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            value = json.loads(raw.decode("utf-8"))
            if not isinstance(value, dict):
                raise ValueError("JSON request body must be an object")
            return value

        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/capabilities":
                self._send_json(200, store.capabilities().to_dict())
                return
            self._send_json(404, _error("sandbox_not_found", "Unknown sandbox route").to_dict())

        def do_POST(self) -> None:  # noqa: N802
            try:
                payload = self._read_json()
                if self.path == "/capture":
                    self._send_json(201, store.capture(payload).to_dict())
                    return
                if self.path == "/lookup":
                    self._send_json(200, store.lookup(payload).to_dict())
                    return
                self._send_json(404, _error("sandbox_not_found", "Unknown sandbox route").to_dict())
            except (json.JSONDecodeError, UnicodeDecodeError, ValueError, ContractValidationError) as exc:
                self._send_json(400, _error("invalid_request", str(exc)).to_dict())

        def log_message(self, format: str, *args: Any) -> None:
            print(f"sandbox: {format % args}")

    return SandboxHandler


def create_server(port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    """Create a loopback-only sandbox server after validation support is verified."""
    store = SandboxStore()
    # Fail closed before binding if the optional validation dependency is absent.
    store.capabilities()
    return ThreadingHTTPServer((LOOPBACK_HOST, port), make_handler(store))


def run_dev_server(port: int = DEFAULT_PORT) -> None:
    """Run the loopback-only sandbox until interrupted."""
    server = create_server(port)
    host, bound_port = server.server_address
    print(f"CERVEL public developer sandbox: http://{host}:{bound_port}")
    print("Routes: GET /capabilities, POST /capture, POST /lookup")
    print("Ephemeral local compatibility surface only; not the proprietary CERVEL runtime.")
    try:
        server.serve_forever()
    finally:
        server.server_close()


__all__ = [
    "DEFAULT_PORT",
    "LOOPBACK_HOST",
    "SandboxStore",
    "ValidationDependencyError",
    "create_server",
    "run_dev_server",
]
