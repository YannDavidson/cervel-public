"""Typed convenience models for the published CERVEL 0.1-draft contracts.

These classes mirror only the deliberately public example schemas. They do not
implement CERVEL runtime behavior, networking, authorization, retrieval,
knowledge compilation, provenance, persistence, or model/agent logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

PUBLIC_DRAFT_VERSION = "0.1-draft"


def _without_none(values: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


@dataclass(frozen=True)
class KnowledgeReference:
    id: str
    version: str = PUBLIC_DRAFT_VERSION
    kind: str | None = None
    source: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return _without_none({
            "version": self.version,
            "id": self.id,
            "kind": self.kind,
            "source": self.source,
        })


@dataclass(frozen=True)
class CaptureEnvelope:
    content: str
    version: str = PUBLIC_DRAFT_VERSION
    content_type: str | None = None
    source: str | None = None
    title: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return _without_none({
            "version": self.version,
            "content": self.content,
            "content_type": self.content_type,
            "source": self.source,
            "title": self.title,
        })


@dataclass(frozen=True)
class LookupRequest:
    query: str
    version: str = PUBLIC_DRAFT_VERSION
    limit: int | None = None
    scope: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return _without_none({
            "version": self.version,
            "query": self.query,
            "limit": self.limit,
            "scope": self.scope,
        })


@dataclass(frozen=True)
class LookupResultItem:
    reference: KnowledgeReference
    text: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return _without_none({
            "reference": self.reference.to_dict(),
            "text": self.text,
        })


@dataclass(frozen=True)
class LookupResult:
    items: tuple[LookupResultItem, ...]
    version: str = PUBLIC_DRAFT_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "items": [item.to_dict() for item in self.items],
        }


@dataclass(frozen=True)
class ErrorEnvelope:
    code: str
    version: str = PUBLIC_DRAFT_VERSION
    message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return _without_none({
            "version": self.version,
            "code": self.code,
            "message": self.message,
        })


@dataclass(frozen=True)
class CapabilityContract:
    name: str
    version: str

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "version": self.version}


@dataclass(frozen=True)
class CapabilityDiscovery:
    contracts: tuple[CapabilityContract, ...]
    version: str = PUBLIC_DRAFT_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "contracts": [contract.to_dict() for contract in self.contracts],
        }
