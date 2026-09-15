from cervel_public.model_adapters import ModelContextItem, ModelRequest, OllamaAdapter, build_prompt


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
