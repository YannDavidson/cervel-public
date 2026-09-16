from cervel_public import cli
from cervel_public import continuity_demo
from cervel_public.model_adapters import ModelResponse


def test_continuity_demo_restarts_and_recovers_same_knowledge(monkeypatch, capsys):
    class LocalAdapter:
        def __init__(self, model):
            self.model = model

        def generate(self, value):
            assert value.context
            return ModelResponse(text="local answer", model=f"ollama:{self.model}")

    monkeypatch.setattr(continuity_demo, "OllamaAdapter", LocalAdapter)
    result = continuity_demo.run_continuity_demo(ollama_model="test-model")
    assert result == 0
    output = capsys.readouterr().out
    assert "✓ Knowledge captured: local-000001" in output
    assert "✓ CERVEL sandbox stopped" in output
    assert "✓ CERVEL sandbox restarted" in output
    assert "✓ Same knowledge recovered: local-000001" in output
    assert "✓ Reasoned with local model: ollama:test-model" in output
    assert "PASS: CERVEL continuity verified." in output


def test_continuity_demo_cloud_switch_requires_explicit_consent():
    try:
        continuity_demo.run_continuity_demo(cloud_model="example-model")
    except ValueError as exc:
        assert "explicit consent" in str(exc)
    else:
        raise AssertionError("cloud continuity switch should require explicit consent")


def test_cli_continuity_refuses_cloud_before_running_demo(monkeypatch, capsys):
    called = False

    def unexpected(**kwargs):
        nonlocal called
        called = True
        return 0

    monkeypatch.setattr(cli, "run_continuity_demo", unexpected)
    result = cli.main(["demo", "continuity", "--cloud-model", "example-model"])
    assert result == 2
    assert called is False
    assert "refused cloud context" in capsys.readouterr().out


def test_cli_continuity_dispatches_one_command(monkeypatch):
    received = {}

    def fake_demo(**kwargs):
        received.update(kwargs)
        return 0

    monkeypatch.setattr(cli, "run_continuity_demo", fake_demo)
    result = cli.main(["demo", "continuity", "--ollama-model", "llama3"])
    assert result == 0
    assert received["ollama_model"] == "llama3"
    assert received["cloud_model"] is None
    assert received["send_context_to_cloud"] is False
