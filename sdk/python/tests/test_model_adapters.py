import io
from urllib import error

import pytest

from cervel_public.model_adapters import (
    ModelAdapterConfigurationError,
    ModelAdapterConnectionError,
    ModelAdapterResponseError,
    ModelContextItem,
    ModelRequest,
    OllamaAdapter,
    OpenAICompatibleAdapter,
    build_prompt,
)


class _Response:
    def __init__(self, body: bytes):
        self._body = body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self._body


def test_prompt_contains_only_question_and_supplied_context():
    value = ModelRequest(
        question="What do we know about Project Atlas?",
        context=(ModelContextItem(text="Atlas uses durable knowledge.", reference_id="local-1"),),
    )
    prompt = build_prompt(value)
    assert "Project Atlas" in prompt
    assert "Atlas uses durable knowledge." in prompt
    assert "local-1" in prompt


def test_ollama_model_id_is_explicit():
    adapter = OllamaAdapter("llama3")
    assert adapter.model_id == "ollama:llama3"


@pytest.mark.parametrize(
    "base_url",
    [
        "https://127.0.0.1:11434",
        "http://example.com:11434",
        "http://user:secret@127.0.0.1:11434",
        "http://127.0.0.1:11434/api",
        "http://127.0.0.1:11434?x=1",
        "http://127.0.0.1:11434#fragment",
    ],
)
def test_ollama_rejects_non_loopback_or_decorated_endpoints(base_url):
    with pytest.raises(ModelAdapterConfigurationError, match="loopback origin"):
        OllamaAdapter("llama3", base_url=base_url)


def test_ollama_accepts_supported_loopback_hosts():
    assert OllamaAdapter("llama3", base_url="http://localhost:11434").model_id == "ollama:llama3"
    assert OllamaAdapter("llama3", base_url="http://[::1]:11434").model_id == "ollama:llama3"


@pytest.mark.parametrize("timeout", [0, -1])
def test_ollama_requires_positive_timeout(timeout):
    with pytest.raises(ModelAdapterConfigurationError, match="greater than zero"):
        OllamaAdapter("llama3", timeout=timeout)


def test_ollama_success_response(monkeypatch):
    monkeypatch.setattr("cervel_public.model_adapters.request.urlopen", lambda req, timeout: _Response(b'{"response":"local answer"}'))
    result = OllamaAdapter("llama3").generate(ModelRequest(question="Question?"))
    assert result.text == "local answer"
    assert result.model == "ollama:llama3"


def test_ollama_connection_failure(monkeypatch):
    def fail(req, timeout):
        raise error.URLError("offline")

    monkeypatch.setattr("cervel_public.model_adapters.request.urlopen", fail)
    with pytest.raises(ModelAdapterConnectionError, match="could not reach Ollama"):
        OllamaAdapter("llama3").generate(ModelRequest(question="Question?"))


def test_ollama_http_failure_is_response_error(monkeypatch):
    def fail(req, timeout):
        raise error.HTTPError(req.full_url, 500, "boom", {}, io.BytesIO())

    monkeypatch.setattr("cervel_public.model_adapters.request.urlopen", fail)
    with pytest.raises(ModelAdapterResponseError, match="HTTP 500"):
        OllamaAdapter("llama3").generate(ModelRequest(question="Question?"))


def test_ollama_malformed_response(monkeypatch):
    monkeypatch.setattr("cervel_public.model_adapters.request.urlopen", lambda req, timeout: _Response(b"not-json"))
    with pytest.raises(ModelAdapterResponseError, match="malformed JSON"):
        OllamaAdapter("llama3").generate(ModelRequest(question="Question?"))


def test_openai_compatible_model_id_is_explicit():
    adapter = OpenAICompatibleAdapter("example-model", api_key="developer-test-key")
    assert adapter.model_id == "openai:example-model"


def test_openai_compatible_requires_developer_owned_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ModelAdapterConfigurationError, match="OPENAI_API_KEY"):
        OpenAICompatibleAdapter("example-model")


def test_openai_compatible_reads_key_from_named_environment(monkeypatch):
    monkeypatch.setenv("MY_MODEL_KEY", "developer-test-key")
    adapter = OpenAICompatibleAdapter("example-model", api_key_env="MY_MODEL_KEY")
    assert adapter.model_id == "openai:example-model"


def test_cloud_endpoint_requires_https():
    with pytest.raises(ModelAdapterConfigurationError, match="HTTPS"):
        OpenAICompatibleAdapter("example-model", api_key="developer-test-key", base_url="http://example.com/v1")


def test_cloud_endpoint_rejects_embedded_credentials():
    with pytest.raises(ModelAdapterConfigurationError, match="without credentials"):
        OpenAICompatibleAdapter(
            "example-model",
            api_key="developer-test-key",
            base_url="https://user:secret@example.com/v1",
        )


@pytest.mark.parametrize("timeout", [0, -1])
def test_cloud_adapter_requires_positive_timeout(timeout):
    with pytest.raises(ModelAdapterConfigurationError, match="greater than zero"):
        OpenAICompatibleAdapter("example-model", api_key="developer-test-key", timeout=timeout)


def test_cloud_success_response(monkeypatch):
    monkeypatch.setattr(
        "cervel_public.model_adapters.request.urlopen",
        lambda req, timeout: _Response(b'{"choices":[{"message":{"content":"cloud answer"}}]}'),
    )
    result = OpenAICompatibleAdapter("example-model", api_key="developer-test-key").generate(ModelRequest(question="Question?"))
    assert result.text == "cloud answer"
    assert result.model == "openai:example-model"


def test_cloud_connection_failure(monkeypatch):
    def fail(req, timeout):
        raise error.URLError("offline")

    monkeypatch.setattr("cervel_public.model_adapters.request.urlopen", fail)
    with pytest.raises(ModelAdapterConnectionError, match="could not reach configured cloud"):
        OpenAICompatibleAdapter("example-model", api_key="developer-test-key").generate(ModelRequest(question="Question?"))


def test_cloud_malformed_response(monkeypatch):
    monkeypatch.setattr("cervel_public.model_adapters.request.urlopen", lambda req, timeout: _Response(b"not-json"))
    with pytest.raises(ModelAdapterResponseError, match="malformed JSON"):
        OpenAICompatibleAdapter("example-model", api_key="developer-test-key").generate(ModelRequest(question="Question?"))
