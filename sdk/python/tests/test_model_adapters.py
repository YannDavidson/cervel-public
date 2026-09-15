import pytest

from cervel_public.model_adapters import (
    ModelAdapterConfigurationError,
    ModelContextItem,
    ModelRequest,
    OllamaAdapter,
    OpenAICompatibleAdapter,
    build_prompt,
)


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
