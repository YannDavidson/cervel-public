from cervel_public import cli


def test_cloud_model_refuses_context_without_explicit_consent(monkeypatch, capsys):
    called = False

    class UnexpectedClient:
        def __init__(self):
            nonlocal called
            called = True

    monkeypatch.setattr(cli, "LocalClient", UnexpectedClient)
    result = cli.main(["ask", "What do we know?", "--model", "openai:example-model"])
    assert result == 2
    assert called is False
    assert "without --send-context-to-cloud" in capsys.readouterr().out


def test_local_model_does_not_require_cloud_consent(monkeypatch, capsys):
    class Lookup:
        items = ()

    class Client:
        def lookup(self, question, limit):
            return Lookup()

    class Adapter:
        def __init__(self, model):
            self.model = model

        def generate(self, value):
            return type("Response", (), {"model": f"ollama:{self.model}", "text": "local answer"})()

    monkeypatch.setattr(cli, "LocalClient", Client)
    monkeypatch.setattr(cli, "OllamaAdapter", Adapter)
    result = cli.main(["ask", "What do we know?", "--model", "ollama:llama3"])
    assert result == 0
    output = capsys.readouterr().out
    assert "Using: ollama:llama3" in output
    assert "local answer" in output


def test_cloud_model_runs_only_after_explicit_consent(monkeypatch, capsys):
    class Lookup:
        items = ()

    class Client:
        def lookup(self, question, limit):
            return Lookup()

    class Adapter:
        def __init__(self, model, *, base_url, api_key_env):
            self.model = model

        def generate(self, value):
            return type("Response", (), {"model": f"openai:{self.model}", "text": "cloud answer"})()

    monkeypatch.setattr(cli, "LocalClient", Client)
    monkeypatch.setattr(cli, "OpenAICompatibleAdapter", Adapter)
    result = cli.main(
        ["ask", "What do we know?", "--model", "openai:example-model", "--send-context-to-cloud"]
    )
    assert result == 0
    output = capsys.readouterr().out
    assert "Using: openai:example-model" in output
    assert "cloud answer" in output
