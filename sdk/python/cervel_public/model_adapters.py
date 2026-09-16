"""Deliberately thin public model-adapter surface.

Adapters receive already-retrieved public context and execute a developer-selected
reasoning model. They do not implement CERVEL retrieval, activation, permissions,
context compilation, routing, provenance, persistence, or the proprietary
Intelligence Gateway.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Protocol, Sequence
from urllib import error, request
from urllib.parse import urlparse


class ModelAdapterError(RuntimeError):
    """Base error for public developer model adapters."""


class ModelAdapterConfigurationError(ModelAdapterError):
    """Raised when developer-owned model configuration is invalid."""


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


def _validate_timeout(timeout: float) -> float:
    if timeout <= 0:
        raise ModelAdapterConfigurationError("timeout must be greater than zero")
    return timeout


def _validate_ollama_base_url(base_url: str) -> str:
    parsed = urlparse(base_url)
    if (
        parsed.scheme != "http"
        or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or parsed.path not in {"", "/"}
    ):
        raise ModelAdapterConfigurationError(
            "Ollama base_url must be an HTTP loopback origin without credentials, path, query, or fragment"
        )
    try:
        port = parsed.port
    except ValueError as exc:
        raise ModelAdapterConfigurationError("Ollama base_url contains an invalid port") from exc
    if port is not None and not 1 <= port <= 65535:
        raise ModelAdapterConfigurationError("Ollama base_url port must be between 1 and 65535")
    return base_url.rstrip("/")


class OllamaAdapter:
    """Small loopback-only Ollama adapter; no API key or cloud dependency."""

    def __init__(self, model: str, *, base_url: str = "http://127.0.0.1:11434", timeout: float = 60.0) -> None:
        if not model.strip():
            raise ModelAdapterConfigurationError("model must not be empty")
        self._model = model.strip()
        self._base_url = _validate_ollama_base_url(base_url)
        self._timeout = _validate_timeout(timeout)

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
        except error.HTTPError as exc:
            raise ModelAdapterResponseError(f"Ollama returned HTTP {exc.code}") from exc
        except (error.URLError, OSError) as exc:
            raise ModelAdapterConnectionError(f"could not reach Ollama at {self._base_url}") from exc
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ModelAdapterResponseError("Ollama returned malformed JSON") from exc
        text = decoded.get("response") if isinstance(decoded, dict) else None
        if not isinstance(text, str):
            raise ModelAdapterResponseError("Ollama response is missing text")
        return ModelResponse(text=text, model=self.model_id)


class OpenAICompatibleAdapter:
    """Developer-owned adapter for OpenAI-compatible chat-completions endpoints."""

    def __init__(
        self,
        model: str,
        *,
        api_key: str | None = None,
        api_key_env: str = "OPENAI_API_KEY",
        base_url: str = "https://api.openai.com/v1",
        timeout: float = 60.0,
    ) -> None:
        if not model.strip():
            raise ModelAdapterConfigurationError("model must not be empty")
        parsed = urlparse(base_url)
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ModelAdapterConfigurationError("cloud model base_url must be an HTTPS origin/path without credentials, query, or fragment")
        key = api_key if api_key is not None else os.environ.get(api_key_env)
        if not key or not key.strip():
            raise ModelAdapterConfigurationError(f"missing developer-owned API key in {api_key_env}")
        self._model = model.strip()
        self._api_key = key.strip()
        self._base_url = base_url.rstrip("/")
        self._timeout = _validate_timeout(timeout)

    @property
    def model_id(self) -> str:
        return f"openai:{self._model}"

    def generate(self, value: ModelRequest) -> ModelResponse:
        payload = json.dumps(
            {"model": self._model, "messages": [{"role": "user", "content": build_prompt(value)}]}
        ).encode("utf-8")
        req = request.Request(
            f"{self._base_url}/chat/completions",
            data=payload,
            headers={"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self._timeout) as response:
                decoded = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            raise ModelAdapterResponseError(f"cloud model endpoint returned HTTP {exc.code}") from exc
        except (error.URLError, OSError) as exc:
            raise ModelAdapterConnectionError("could not reach configured cloud model endpoint") from exc
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ModelAdapterResponseError("cloud model endpoint returned malformed JSON") from exc
        try:
            text = decoded["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ModelAdapterResponseError("cloud model response is missing assistant text") from exc
        if not isinstance(text, str):
            raise ModelAdapterResponseError("cloud model response is missing assistant text")
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
    "ModelAdapterConfigurationError",
    "ModelAdapterConnectionError",
    "ModelAdapterError",
    "ModelAdapterResponseError",
    "ModelContextItem",
    "ModelRequest",
    "ModelResponse",
    "OllamaAdapter",
    "OpenAICompatibleAdapter",
    "build_prompt",
    "context_from_lookup",
    "render_context",
]
