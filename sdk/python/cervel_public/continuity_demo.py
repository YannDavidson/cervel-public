"""Observable one-command continuity proof for the public CERVEL developer surface.

The demo owns two short-lived loopback sandbox server instances backed by the
same temporary SQLite database. It captures one public record, restarts the
sandbox, verifies the same reference and content, then asks a developer-selected
local Ollama model. An optional OpenAI-compatible cloud switch remains explicitly
consent-gated.

This is a bounded public developer proof. It is not the proprietary CERVEL Vault,
production persistence, retrieval/ranking, authorization, provenance, Knowledge
Compiler, CCP, Intelligence Gateway, or production model-routing behavior.
"""

from __future__ import annotations

import tempfile
import threading
from pathlib import Path

from .client import LocalClient
from .model_adapters import (
    ModelRequest,
    OllamaAdapter,
    OpenAICompatibleAdapter,
    context_from_lookup,
)
from .sandbox import create_server

QUESTION = "What do we know about Project Atlas?"
KNOWLEDGE = (
    "Project Atlas uses CERVEL so its knowledge can remain stable while the "
    "developer changes the reasoning model."
)


def _snapshot(items) -> tuple[tuple[str, str | None, str | None], ...]:
    return tuple((item.reference.id, item.reference.source, item.text) for item in items)


def _start_server(db_path: Path):
    server = create_server(0, db_path=db_path)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    return server, thread, LocalClient(f"http://{host}:{port}")


def _stop_server(server, thread: threading.Thread) -> None:
    server.shutdown()
    server.server_close()
    thread.join(timeout=5)
    if thread.is_alive():
        raise RuntimeError("continuity demo sandbox did not stop cleanly")


def run_continuity_demo(
    *,
    ollama_model: str = "llama3",
    cloud_model: str | None = None,
    cloud_base_url: str = "https://api.openai.com/v1",
    cloud_api_key_env: str = "OPENAI_API_KEY",
    send_context_to_cloud: bool = False,
) -> int:
    """Run restart continuity and model-replacement proof in one invocation."""
    if cloud_model and not send_context_to_cloud:
        raise ValueError("cloud model requires explicit consent to send context")

    print("CERVEL continuity demo")
    print("Public developer proof: restart persistence + replaceable reasoning models.\n")

    with tempfile.TemporaryDirectory(prefix="cervel-continuity-") as directory:
        db_path = Path(directory) / "continuity.sqlite3"

        first_server, first_thread, first_client = _start_server(db_path)
        try:
            reference = first_client.capture(KNOWLEDGE, source="continuity-demo", title="Project Atlas")
            before = first_client.lookup(QUESTION, limit=5)
            before_snapshot = _snapshot(before.items)
            if not before_snapshot:
                raise RuntimeError("continuity lookup returned no knowledge after capture")
            print(f"✓ Knowledge captured: {reference.id}")
        finally:
            _stop_server(first_server, first_thread)
        print("✓ CERVEL sandbox stopped")

        second_server, second_thread, second_client = _start_server(db_path)
        try:
            print("✓ CERVEL sandbox restarted")
            after_restart = second_client.lookup(QUESTION, limit=5)
            restart_snapshot = _snapshot(after_restart.items)
            if restart_snapshot != before_snapshot:
                raise RuntimeError("knowledge changed across sandbox restart")
            if not any(item.reference.id == reference.id for item in after_restart.items):
                raise RuntimeError("captured reference was not recovered after restart")
            print(f"✓ Same knowledge recovered: {reference.id}")

            local = OllamaAdapter(ollama_model).generate(
                ModelRequest(question=QUESTION, context=context_from_lookup(after_restart.items))
            )
            print(f"✓ Reasoned with local model: {local.model}")

            if cloud_model:
                cloud = OpenAICompatibleAdapter(
                    cloud_model,
                    base_url=cloud_base_url,
                    api_key_env=cloud_api_key_env,
                ).generate(ModelRequest(question=QUESTION, context=context_from_lookup(after_restart.items)))
                print(f"✓ Switched reasoning model: {cloud.model}")
            else:
                print("· Cloud switch skipped; local restart/model continuity is complete")

            final_lookup = second_client.lookup(QUESTION, limit=5)
            if _snapshot(final_lookup.items) != restart_snapshot:
                raise RuntimeError("knowledge changed while reasoning models were used")
            print("✓ Knowledge unchanged after reasoning")
        finally:
            _stop_server(second_server, second_thread)

    print("\nPASS: CERVEL continuity verified.")
    print("The sandbox restarted and the knowledge remained; reasoning stayed replaceable.")
    return 0


__all__ = ["KNOWLEDGE", "QUESTION", "run_continuity_demo"]
