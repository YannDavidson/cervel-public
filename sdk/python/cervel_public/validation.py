"""Local validation helpers for the deliberately public CERVEL contracts.

Validation is performed only against the public experimental schemas embedded
in this module. No network request, service discovery, authentication,
authorization, retrieval, persistence, or private CERVEL runtime behavior is
performed.
"""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from typing import Any


class ValidationDependencyError(RuntimeError):
    """Raised when optional JSON Schema validation dependencies are unavailable."""


class UnsupportedContractError(ValueError):
    """Raised when a caller requests a contract not published by this SDK."""


class ContractValidationError(ValueError):
    """Raised when a payload does not satisfy a published public schema."""

    def __init__(self, contract: str, errors: tuple[str, ...]) -> None:
        self.contract = contract
        self.errors = errors
        detail = "; ".join(errors) if errors else "payload is invalid"
        super().__init__(f"{contract} validation failed: {detail}")


PUBLIC_SCHEMAS: dict[str, dict[str, Any]] = {
    "capture-envelope": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://cervel.ai/public/schemas/capture-envelope.example.schema.json",
        "title": "CERVEL Capture Envelope — Experimental Draft",
        "description": "Illustrative public schema for the experimental capture envelope. This is not a production CERVEL capture schema or API contract.",
        "type": "object",
        "additionalProperties": True,
        "required": ["version", "content"],
        "properties": {
            "version": {"const": "0.1-draft"},
            "content": {"type": "string"},
            "content_type": {"type": "string", "minLength": 1},
            "source": {
                "type": "string",
                "minLength": 1,
                "description": "Optional non-authoritative source context.",
            },
            "title": {"type": "string"},
        },
    },
    "lookup-request": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://cervel.ai/public/schemas/lookup-request.example.schema.json",
        "title": "CERVEL Lookup Request — Experimental Draft",
        "description": "Illustrative public schema for the experimental lookup request. This is not a production CERVEL search or retrieval API schema.",
        "type": "object",
        "additionalProperties": True,
        "required": ["version", "query"],
        "properties": {
            "version": {"const": "0.1-draft"},
            "query": {"type": "string"},
            "limit": {"type": "integer", "minimum": 0},
            "scope": {
                "type": "string",
                "minLength": 1,
                "description": "Optional opaque caller-provided scope hint.",
            },
        },
    },
    "knowledge-reference": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://cervel.ai/public/schemas/knowledge-reference.example.schema.json",
        "title": "CERVEL Knowledge Reference — Experimental Draft",
        "description": "Illustrative public schema for the experimental knowledge reference draft. This is not a production CERVEL object schema.",
        "type": "object",
        "additionalProperties": True,
        "required": ["version", "id"],
        "properties": {
            "version": {"const": "0.1-draft"},
            "id": {
                "type": "string",
                "minLength": 1,
                "description": "Opaque interoperability identifier. Consumers must not infer internal semantics from its syntax.",
            },
            "kind": {"type": "string", "minLength": 1},
            "source": {
                "type": "string",
                "minLength": 1,
                "description": "Optional minimal source context; not an authority or access claim.",
            },
        },
    },
    "lookup-result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://cervel.ai/public/schemas/lookup-result.example.schema.json",
        "title": "CERVEL Lookup Result — Experimental Draft",
        "description": "Illustrative public schema for the experimental lookup result. This is not a production CERVEL retrieval response schema.",
        "type": "object",
        "additionalProperties": True,
        "required": ["version", "items"],
        "properties": {
            "version": {"const": "0.1-draft"},
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": True,
                    "required": ["reference"],
                    "properties": {
                        "reference": {
                            "$ref": "https://cervel.ai/public/schemas/knowledge-reference.example.schema.json",
                            "description": "Knowledge Reference governed by the applicable public Knowledge Reference contract.",
                        },
                        "text": {"type": "string"},
                    },
                },
            },
        },
    },
    "error-envelope": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://cervel.ai/public/schemas/error-envelope.example.schema.json",
        "title": "CERVEL Error Envelope — Experimental Draft",
        "description": "Illustrative public schema for the experimental error envelope. This is not a production CERVEL error or exception schema.",
        "type": "object",
        "additionalProperties": True,
        "required": ["version", "code"],
        "properties": {
            "version": {"const": "0.1-draft"},
            "code": {"type": "string", "minLength": 1},
            "message": {"type": "string"},
        },
    },
    "capability-discovery": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://cervel.ai/public/schemas/capability-discovery.example.schema.json",
        "title": "CERVEL Capability Discovery — Experimental Draft",
        "description": "Illustrative public schema for the experimental capability discovery document. This is not a production CERVEL service-discovery or control-plane schema.",
        "type": "object",
        "additionalProperties": True,
        "required": ["version", "contracts"],
        "properties": {
            "version": {"const": "0.1-draft"},
            "contracts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": True,
                    "required": ["name", "version"],
                    "properties": {
                        "name": {"type": "string", "minLength": 1},
                        "version": {"type": "string", "minLength": 1},
                    },
                },
            },
        },
    },
}

SUPPORTED_CONTRACTS = tuple(PUBLIC_SCHEMAS)


def get_public_schema(contract: str) -> dict[str, Any]:
    """Return a defensive copy of one embedded public experimental schema."""
    try:
        return deepcopy(PUBLIC_SCHEMAS[contract])
    except KeyError as exc:
        raise UnsupportedContractError(
            f"unsupported public contract {contract!r}; expected one of {SUPPORTED_CONTRACTS!r}"
        ) from exc


def _payload_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        payload = to_dict()
        if isinstance(payload, Mapping):
            return dict(payload)
    raise TypeError("value must be a mapping or expose to_dict() returning a mapping")


def _validator(contract: str):
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
    except ImportError as exc:
        raise ValidationDependencyError(
            "contract validation requires the optional 'validation' extra; "
            "install with: pip install 'cervel-public[validation]'"
        ) from exc

    schema = get_public_schema(contract)
    registry = Registry()
    for public_schema in PUBLIC_SCHEMAS.values():
        registry = registry.with_resource(
            public_schema["$id"], Resource.from_contents(public_schema)
        )
    return Draft202012Validator(schema, registry=registry)


def validation_errors(contract: str, value: Any) -> tuple[str, ...]:
    """Return stable human-readable errors for a public contract payload."""
    payload = _payload_dict(value)
    validator = _validator(contract)
    issues: list[str] = []
    errors = sorted(
        validator.iter_errors(payload),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    for error in errors:
        path = ".".join(str(part) for part in error.absolute_path) or "$"
        issues.append(f"{path}: {error.message}")
    return tuple(issues)


def validate_payload(contract: str, value: Any) -> None:
    """Validate a mapping or public SDK model against a named public contract."""
    errors = validation_errors(contract, value)
    if errors:
        raise ContractValidationError(contract, errors)


def validate_capture_envelope(value: Any) -> None:
    validate_payload("capture-envelope", value)


def validate_lookup_request(value: Any) -> None:
    validate_payload("lookup-request", value)


def validate_knowledge_reference(value: Any) -> None:
    validate_payload("knowledge-reference", value)


def validate_lookup_result(value: Any) -> None:
    validate_payload("lookup-result", value)


def validate_error_envelope(value: Any) -> None:
    validate_payload("error-envelope", value)


def validate_capability_discovery(value: Any) -> None:
    validate_payload("capability-discovery", value)
