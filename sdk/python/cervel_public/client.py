"""Loopback-only client for the public CERVEL developer sandbox.

The client speaks only the deliberately published experimental contracts over
HTTP to a loopback address. It is not a production CERVEL client and does not
implement authentication, authorization, permission-aware activation,
production routing, persistence, retrieval/ranking semantics, or private
runtime behavior.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import urlsplit

from .models import (
    PUBLIC_DRAFT_VERSION,
    CapabilityContract,
    CapabilityDiscovery,
    CaptureEnvelope,
    ErrorEnvelope,
    KnowledgeReference,
    LookupRequest,
    LookupResult,
    LookupResultItem,
)

DEFAULT_LOCAL_BASE_URL = "http://127.0.0.1:8765"
_LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}


class LocalClientError(RuntimeError):
    """Base exception for the bounded public local client."""


class LocalClientConfigurationError(LocalClientError, ValueError):
    """Raised when a client target is outside the supported loopback boundary."""


class LocalClientConnectionError(LocalClientError, ConnectionError):
    """Raised when the localhost sandbox cannot be reached."""


class LocalClientMalformedResponseError(LocalClientError, ValueError):
    """Raised when a sandbox response does not match the expected public shape."""


class LocalClientResponseError(LocalClientError):
    """Raised when the sandbox returns a public HTTP error response."""

    def __init__(self, status: int, error: ErrorEnvelope | None = None) -> None:
        self.status = status
        self.error = error
        if error is None:
            detail = f"sandbox request failed with HTTP {status}"
        else:
            detail = f"sandbox request failed with HTTP {status}: {error.code}"
            if error.message:
                detail += f": {error.message}"
        super().__init__(detail)


def _require_object(value: Any, contract: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise LocalClientMalformedResponseError(f"{contract} response must be a JSON object")
    return value


def _require_string(value: Any, field: str, contract: str, *, nonempty: bool = False) -> str:
    if not isinstance(value, str) or (nonempty and not value):
        suffix = " non-empty" if nonempty else ""
        raise LocalClientMalformedResponseError(
            f"{contract} response field {field!r} must be a{suffix} string"
        )
    return value


def _optional_string(value: Any, field: str, contract: str) -> str | None:
    if value is None:
        return None
    return _require_string(value, field, contract)


def _require_public_version(payload: dict[str, Any], contract: str) -> str:
    version = _require_string(payload.get("version"), "version", contract, nonempty=True)
    if version != PUBLIC_DRAFT_VERSION:
        raise LocalClientMalformedResponseError(
            f"{contract} response version {version!r} is not {PUBLIC_DRAFT_VERSION!r}"
        )
    return version


def _parse_reference(value: Any) -> KnowledgeReference:
    contract = "knowledge-reference"
    payload = _require_object(value, contract)
    version = _require_public_version(payload, contract)
    return KnowledgeReference(
        id=_require_string(payload.get("id"), "id", contract, nonempty=True),
        version=version,
        kind=_optional_string(payload.get("kind"), "kind", contract),
        source=_optional_string(payload.get("source"), "source", contract),
    )


def _parse_lookup_result(value: Any) -> LookupResult:
    contract = "lookup-result"
    payload = _require_object(value, contract)
    version = _require_public_version(payload, contract)
    raw_items = payload.get("items")
    if not isinstance(raw_items, list):
        raise LocalClientMalformedResponseError("lookup-result response field 'items' must be an array")
    items: list[LookupResultItem] = []
    for index, raw_item in enumerate(raw_items):
        item = _require_object(raw_item, f"lookup-result item {index}")
        if "reference" not in item:
            raise LocalClientMalformedResponseError(
                f"lookup-result item {index} is missing required field 'reference'"
            )
        items.append(
            LookupResultItem(
                reference=_parse_reference(item["reference"]),
                text=_optional_string(item.get("text"), "text", f"lookup-result item {index}"),
            )
        )
    return LookupResult(items=tuple(items), version=version)


def _parse_capabilities(value: Any) -> CapabilityDiscovery:
    contract = "capability-discovery"
    payload = _require_object(value, contract)
    version = _require_public_version(payload, contract)
    raw_contracts = payload.get("contracts")
    if not isinstance(raw_contracts, list):
        raise LocalClientMalformedResponseError(
            "capability-discovery response field 'contracts' must be an array"
        )
    contracts: list[CapabilityContract] = []
    for index, raw_contract in enumerate(raw_contracts):
        item = _require_object(raw_contract, f"capability-discovery contract {index}")
        contracts.append(
            CapabilityContract(
                name=_require_string(
                    item.get("name"), "name", f"capability-discovery contract {index}", nonempty=True
                ),
                version=_require_string(
                    item.get("version"),
                    "version",
                    f"capability-discovery contract {index}",
                    nonempty=True,
                ),
            )
        )
    return CapabilityDiscovery(contracts=tuple(contracts), version=version)


def _parse_error(value: Any) -> ErrorEnvelope:
    contract = "error-envelope"
    payload = _require_object(value, contract)
    version = _require_public_version(payload, contract)
    return ErrorEnvelope(
        code=_require_string(payload.get("code"), "code", contract, nonempty=True),
        version=version,
        message=_optional_string(payload.get("message"), "message", contract),
    )


def _decode_json(raw: bytes, contract: str) -> Any:
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LocalClientMalformedResponseError(
            f"{contract} response was not valid UTF-8 JSON"
        ) from exc


class LocalClient:
    """Small stdlib-only client for the loopback public developer sandbox."""

    def __init__(self, base_url: str = DEFAULT_LOCAL_BASE_URL, *, timeout: float = 5.0) -> None:
        parsed = urlsplit(base_url)
        if parsed.scheme != "http" or parsed.hostname not in _LOOPBACK_HOSTS:
            raise LocalClientConfigurationError(
                "LocalClient accepts only http:// loopback targets (127.0.0.1, localhost, or ::1)"
            )
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise LocalClientConfigurationError(
                "LocalClient base_url must not include credentials, query parameters, or fragments"
            )
        if parsed.path not in ("", "/"):
            raise LocalClientConfigurationError("LocalClient base_url must not include a path")
        if timeout <= 0:
            raise LocalClientConfigurationError("LocalClient timeout must be greater than zero")
        self.base_url = base_url.rstrip("/")
        self.timeout = float(timeout)

    def capabilities(self) -> CapabilityDiscovery:
        payload = self._request("GET", "/capabilities", expected_status=200)
        return _parse_capabilities(payload)

    def capture(
        self,
        content: str,
        *,
        content_type: str | None = None,
        source: str | None = None,
        title: str | None = None,
    ) -> KnowledgeReference:
        envelope = CaptureEnvelope(
            content=content,
            content_type=content_type,
            source=source,
            title=title,
        )
        payload = self._request("POST", "/capture", envelope.to_dict(), expected_status=201)
        return _parse_reference(payload)

    def lookup(
        self,
        query: str,
        *,
        limit: int | None = None,
        scope: str | None = None,
    ) -> LookupResult:
        request = LookupRequest(query=query, limit=limit, scope=scope)
        payload = self._request("POST", "/lookup", request.to_dict(), expected_status=200)
        return _parse_lookup_result(payload)

    def _request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
        *,
        expected_status: int,
    ) -> Any:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(self.base_url + path, data=data, method=method)
        if data is not None:
            request.add_header("Content-Type", "application/json")
        request.add_header("Accept", "application/json")

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                status = response.status
                raw = response.read()
        except urllib.error.HTTPError as exc:
            raw = exc.read()
            try:
                error = _parse_error(_decode_json(raw, "error-envelope"))
            except LocalClientMalformedResponseError:
                error = None
            raise LocalClientResponseError(exc.code, error) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise LocalClientConnectionError(
                f"could not reach CERVEL public sandbox at {self.base_url}"
            ) from exc

        if status != expected_status:
            raise LocalClientResponseError(status)
        return _decode_json(raw, "sandbox")


__all__ = [
    "DEFAULT_LOCAL_BASE_URL",
    "LocalClient",
    "LocalClientConfigurationError",
    "LocalClientConnectionError",
    "LocalClientError",
    "LocalClientMalformedResponseError",
    "LocalClientResponseError",
]
