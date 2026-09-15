"""Demonstrate model-replacement continuity against one running CERVEL sandbox.

Run `cervel dev` first, then execute this example with `--run`. It captures
knowledge once, snapshots the public lookup result, asks a local Ollama model,
optionally asks a developer-owned OpenAI-compatible cloud model, and verifies
that the public knowledge snapshot is unchanged after the model switch.

The sandbox is currently in-memory. This proves continuity while the same
sandbox process remains running; it does not claim persistence across restarts.
"""

from __future__ import annotations

import argparse

QUESTION = "What do we know about Project Atlas?"
KNOWLEDGE = (
    "Project Atlas uses CERVEL so its knowledge can remain stable while the "
    "developer changes the reasoning model."
)


def snapshot(items) -> tuple[tuple[str, str | None, str | None], ...]:
    return tuple((item.reference.id, item.reference.source, item.text) for item in items)


def main() -> int:
    parser = argparse.ArgumentParser(description="CERVEL model-replacement continuity demo")
    parser.add_argument("--run", action="store_true", help="run the live continuity demonstration")
    parser.add_argument("--ollama-model", default="llama3")
    parser.add_argument("--cloud-model")
    parser.add_argument("--cloud-base-url", default="https://api.openai.com/v1")
    parser.add_argument("--cloud-api-key-env", default="OPENAI_API_KEY")
    parser.add_argument(
        "--send-context-to-cloud",
        action="store_true",
        help="explicitly allow captured public sandbox context to leave the machine",
    )
    args = parser.parse_args()

    if not args.run:
        print("Live demo is opt-in. Start `cervel dev`, then rerun this example with --run.")
        return 0
    if args.cloud_model and not args.send_context_to_cloud:
        parser.error("--cloud-model requires --send-context-to-cloud")

    # These APIs are repository development surfaces for the next prerelease.
    # Import them only for an explicitly requested live run so the repository's
    # published-package smoke test can continue exercising the currently pinned
    # public release without contacting a sandbox or model provider.
    try:
        from cervel_public import (
            LocalClient,
            ModelRequest,
            OllamaAdapter,
            OpenAICompatibleAdapter,
            context_from_lookup,
        )
    except ImportError as exc:
        raise RuntimeError(
            "the live continuity demo requires the repository development SDK; "
            "install this checkout before using --run"
        ) from exc

    client = LocalClient()
    reference = client.capture(KNOWLEDGE, source="continuity-demo", title="Project Atlas")
    before = client.lookup(QUESTION, limit=5)
    before_snapshot = snapshot(before.items)
    if not before_snapshot:
        raise RuntimeError("continuity demo lookup returned no knowledge after capture")

    print(f"Captured once: {reference.id}")
    print(f"Knowledge snapshot before model switch: {before_snapshot!r}")

    local = OllamaAdapter(args.ollama_model).generate(
        ModelRequest(question=QUESTION, context=context_from_lookup(before.items))
    )
    print(f"\nReasoning model 1: {local.model}")
    print(local.text)

    if args.cloud_model:
        cloud = OpenAICompatibleAdapter(
            args.cloud_model,
            base_url=args.cloud_base_url,
            api_key_env=args.cloud_api_key_env,
        ).generate(ModelRequest(question=QUESTION, context=context_from_lookup(before.items)))
        print(f"\nReasoning model 2: {cloud.model}")
        print(cloud.text)
    else:
        print("\nCloud step skipped; pass --cloud-model plus --send-context-to-cloud for a remote switch.")

    after = client.lookup(QUESTION, limit=5)
    after_snapshot = snapshot(after.items)
    print(f"Knowledge snapshot after model switch:  {after_snapshot!r}")
    if after_snapshot != before_snapshot:
        raise RuntimeError("knowledge snapshot changed while switching reasoning models")

    print("\nPASS: public knowledge snapshot is unchanged.")
    print("Knowledge stayed in the same running sandbox; only the reasoning model changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
