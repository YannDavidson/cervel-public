"""Deliberately thin public model-adapter surface.

Adapters receive already-retrieved public context and execute a developer-selected
reasoning model. They do not implement CERVEL retrieval, activation, permissions,
context compilation, routing, provenance, persistence, or the proprietary
Intelligence Gateway.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol, Sequence
from urllib import error, request


class ModelAdapterError(RuntimeError):
    """Base error for public developer model adapters."""


class ModelAdapterConnectionError(ModelAdapterError):
    """Raised when a configured model endpoint cannot be reached."""


class ModelAdapterResponseError(ModelAdapterError):
    """Raised when a model endpoint returns an unusable response."""


@dataclass(frozen=True)
class ModelContextItem:
    """A public context fragment supplied to a reasoning model."""

    text: str
    reference_id: str | None = None
    source: str | None = None


@dataclass(frozen=True)
class ModelRequest:
    """Provider-neutral input to the public adapter boundary."""

    question: str
    context: tuple[ModelContextItem, ...] = ()


@dataclass(frozen=True)
class ModelResponse:
    """Provider-neutral response from a public model adapter."""

    text: str
    model: str


class ModelAdapter(Protocol):
    """Minimal interface implemented by developer-owned reasoning adapters."""

    @property
    def model_id(self) -> str: ...

    def generate(self, value: ModelRequest) -> ModelResponse: ...


def render_context(value: ModelRequest) -> str:
    """Render public lookup context without adding private CERVEL semantics."""
    if not value.context:
        return "(no matching public sandbox context)"
    parts: list[str] = []
    for index, item in enumerate(value.context, 1):
        label = item.reference_id or f"context-{index}"
        source = f" source={item.source}" if item.source else ""
        parts.append(f"[{label}{source}] {item.text}")
    return "\n".join(parts)


def build_prompt(value: ModelRequest) -> str:
    return (
        "Answer the question using the supplied context. "
        "If the context does not support an answer, say so.\n\n"
        f"Context:\n{render_context(value)}\n\nQuestion:\n{value.question}"
    )


class OllamaAdapter:
    """Small localhost Ollama adapter; no API key or cloud dependency."""

    def __init__(self, model: str, *, base_url: str = "http://127.0.0.1:11434", timeout: float = 60.0) -> None:
        if not model.strip():
            raise ValueError("model must not be empty")
        self._model = model.strip()
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    @property
    def model_id(self) -> str:
        return f"ollama:{self._model}"

    def generate(self, value: ModelRequest) -> ModelResponse:
        payload = json.dumps({"model": self._model, "prompt": build_prompt(value), "stream": False}).encode("utf-8")
        req = request.Request(
            f"{self._base_url}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self._timeout) as response:
                decoded = json.loads(response.read().decode("utf-8"))
        except (error.URLError, OSError) as exc:
            raise ModelAdapterConnectionError(f"could not reach Ollama at {self._base_url}") from exc
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ModelAdapterResponseError("Ollama returned malformed JSON") from exc
        text = decoded.get("response") if isinstance(decoded, dict) else None
        if not isinstance(text, str):
            raise ModelAdapterResponseError("Ollama response is missing text")
        return ModelResponse(text=text, model=self.model_id)


def context_from_lookup(items: Sequence[object]) -> tuple[ModelContextItem, ...]:
    """Convert public LookupResultItem-like values to the thin adapter context."""
    result: list[ModelContextItem] = []
    for item in items:
        reference = getattr(item, "reference", None)
        result.append(
            ModelContextItem(
                text=str(getattr(item, "text")),
                reference_id=getattr(reference, "id", None),
                source=getattr(reference, "source", None),
            )
        )
    return tuple(result)


__all__ = [
    "ModelAdapter",
    "ModelAdapterConnectionError",
    "ModelAdapterError",
    "ModelAdapterResponseError",
    "ModelContextItem",
    "ModelRequest",
    "ModelResponse",
    "OllamaAdapter",
    "build_prompt",
    "context_from_lookup",
    "render_context",
]
