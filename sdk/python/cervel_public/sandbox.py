"""Local-only developer sandbox for the public CERVEL experimental contracts.

This module is deliberately not the CERVEL runtime. It provides a small
localhost compatibility surface for developers to exercise the published
contracts. It supports a bounded SQLite-backed local store for restart
continuity, but does not implement the proprietary CERVEL Vault, production
retrieval, ranking, authorization, provenance, knowledge compilation, routing,
or agent behavior.
"""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
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
DEFAULT_DATA_DIR = Path.home() / ".cervel-public"
DEFAULT_DB_PATH = DEFAULT_DATA_DIR / "sandbox.sqlite3"
_SCHEMA_VERSION = "1"


@dataclass(frozen=True)
class _StoredRecord:
    reference: KnowledgeReference
    content: str


class SandboxStore:
    """Small public sandbox store, in-memory or SQLite-backed when a path is supplied."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = Path(db_path).expanduser() if db_path is not None else None
        self._records: list[_StoredRecord] = []
        self._next_id = 1
        if self._db_path is not None:
            self._initialize_database()

    @property
    def persistent(self) -> bool:
        return self._db_path is not None

    @property
    def db_path(self) -> Path | None:
        return self._db_path

    def _connect(self) -> sqlite3.Connection:
        assert self._db_path is not None
        connection = sqlite3.connect(self._db_path, timeout=5.0)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize_database(self) -> None:
        assert self._db_path is not None
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
            )
            row = connection.execute(
                "SELECT value FROM metadata WHERE key = 'schema_version'"
            ).fetchone()
            if row is None:
                connection.execute(
                    "INSERT INTO metadata(key, value) VALUES ('schema_version', ?)",
                    (_SCHEMA_VERSION,),
                )
            elif row[0] != _SCHEMA_VERSION:
                raise RuntimeError(
                    f"unsupported public sandbox database schema version: {row[0]}"
                )
            connection.execute(
                """CREATE TABLE IF NOT EXISTS records (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT,
                    content TEXT NOT NULL
                )"""
            )

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

    @staticmethod
    def _reference(sequence: int, source: str | None) -> KnowledgeReference:
        reference = KnowledgeReference(
            id=f"local-{sequence:06d}",
            kind="sandbox-record",
            source=source,
        )
        validate_knowledge_reference(reference)
        return reference

    def capture(self, value: Any) -> KnowledgeReference:
        validate_capture_envelope(value)
        payload = value.to_dict() if hasattr(value, "to_dict") else dict(value)
        source = payload.get("source")
        content = payload["content"]
        if self._db_path is None:
            sequence = self._next_id
            self._next_id += 1
            reference = self._reference(sequence, source)
            self._records.append(_StoredRecord(reference=reference, content=content))
            return reference

        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO records(source, content) VALUES (?, ?)",
                (source, content),
            )
            sequence = int(cursor.lastrowid)
        return self._reference(sequence, source)

    def _all_records(self) -> list[_StoredRecord]:
        if self._db_path is None:
            return list(self._records)
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT sequence, source, content FROM records ORDER BY sequence"
            ).fetchall()
        return [
            _StoredRecord(reference=self._reference(int(sequence), source), content=content)
            for sequence, source, content in rows
        ]

    def lookup(self, value: Any) -> LookupResult:
        validate_lookup_request(value)
        payload = value.to_dict() if hasattr(value, "to_dict") else dict(value)
        query = payload["query"]
        limit = payload.get("limit")

        # Deliberately simple sandbox behavior: case-insensitive token overlap.
        # This is public test-fixture logic, not CERVEL retrieval or ranking.
        tokens = {token for token in re.findall(r"[\w'-]+", query.casefold()) if token}
        matches: list[LookupResultItem] = []
        for record in self._all_records():
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


def create_server(port: int = DEFAULT_PORT, db_path: str | Path | None = None) -> ThreadingHTTPServer:
    """Create a loopback-only sandbox server after validation support is verified."""
    store = SandboxStore(db_path=db_path)
    # Fail closed before binding if the optional validation dependency is absent.
    store.capabilities()
    return ThreadingHTTPServer((LOOPBACK_HOST, port), make_handler(store))


def run_dev_server(port: int = DEFAULT_PORT, db_path: str | Path = DEFAULT_DB_PATH) -> None:
    """Run the loopback-only sandbox with bounded local restart persistence."""
    server = create_server(port, db_path=db_path)
    host, bound_port = server.server_address
    resolved_db = Path(db_path).expanduser().resolve()
    print(f"CERVEL public developer sandbox: http://{host}:{bound_port}")
    print("Routes: GET /capabilities, POST /capture, POST /lookup")
    print(f"Local sandbox database: {resolved_db}")
    print("Public local compatibility surface only; not the proprietary CERVEL Vault/runtime.")
    try:
        server.serve_forever()
    finally:
        server.server_close()


__all__ = [
    "DEFAULT_DATA_DIR",
    "DEFAULT_DB_PATH",
    "DEFAULT_PORT",
    "LOOPBACK_HOST",
    "SandboxStore",
    "ValidationDependencyError",
    "create_server",
    "run_dev_server",
]
