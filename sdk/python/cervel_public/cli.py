"""Command-line entry point for the public CERVEL developer surface."""

from __future__ import annotations

import argparse

from .client import LocalClient, LocalClientError
from .continuity_demo import run_continuity_demo
from .model_adapters import (
    ModelAdapterError,
    ModelRequest,
    OllamaAdapter,
    OpenAICompatibleAdapter,
    context_from_lookup,
)
from .sandbox import DEFAULT_DB_PATH, DEFAULT_PORT, ValidationDependencyError, run_dev_server


def _model_selector(value: str) -> tuple[str, str]:
    provider, separator, model = value.partition(":")
    if separator != ":" or provider not in {"ollama", "openai"} or not model.strip():
        raise argparse.ArgumentTypeError("model must be ollama:MODEL or openai:MODEL")
    return provider, model.strip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cervel", description="CERVEL public developer tools")
    subcommands = parser.add_subparsers(dest="command", required=True)
    dev = subcommands.add_parser("dev", help="run the local public developer sandbox")
    dev.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"loopback port (default: {DEFAULT_PORT})")
    dev.add_argument(
        "--db",
        default=str(DEFAULT_DB_PATH),
        help=f"local SQLite sandbox database (default: {DEFAULT_DB_PATH})",
    )

    ask = subcommands.add_parser("ask", help="ask a developer-selected model using public sandbox lookup context")
    ask.add_argument("question")
    ask.add_argument("--model", required=True, type=_model_selector, metavar="PROVIDER:MODEL")
    ask.add_argument("--limit", type=int, default=5)
    ask.add_argument(
        "--send-context-to-cloud",
        action="store_true",
        help="explicitly allow public sandbox lookup context to be sent to a configured cloud provider",
    )
    ask.add_argument(
        "--openai-base-url",
        default="https://api.openai.com/v1",
        help="HTTPS OpenAI-compatible API base URL (default: OpenAI)",
    )
    ask.add_argument(
        "--openai-api-key-env",
        default="OPENAI_API_KEY",
        help="environment variable containing the developer-owned API key",
    )

    demo = subcommands.add_parser("demo", help="run an observable public developer proof")
    demos = demo.add_subparsers(dest="demo_command", required=True)
    continuity = demos.add_parser(
        "continuity",
        help="capture once, restart the sandbox, recover the same knowledge, and reason with a replaceable model",
    )
    continuity.add_argument("--ollama-model", default="llama3")
    continuity.add_argument("--cloud-model")
    continuity.add_argument("--cloud-base-url", default="https://api.openai.com/v1")
    continuity.add_argument("--cloud-api-key-env", default="OPENAI_API_KEY")
    continuity.add_argument(
        "--send-context-to-cloud",
        action="store_true",
        help="explicitly allow demo sandbox context to be sent to a configured cloud provider",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "dev":
        if not 1 <= args.port <= 65535:
            raise SystemExit("--port must be between 1 and 65535")
        try:
            run_dev_server(port=args.port, db_path=args.db)
        except ValidationDependencyError:
            print("cervel dev requires local sandbox validation support.")
            print("Install with: python -m pip install 'cervel-public[sandbox]'")
            return 2
        except KeyboardInterrupt:
            print("\nCERVEL public developer sandbox stopped.")
        return 0

    if args.command == "ask":
        if args.limit < 1:
            raise SystemExit("--limit must be at least 1")
        provider, model = args.model
        if provider == "openai" and not args.send_context_to_cloud:
            print("cervel ask refused to send sandbox context to a cloud provider without --send-context-to-cloud")
            return 2
        try:
            adapter = (
                OllamaAdapter(model)
                if provider == "ollama"
                else OpenAICompatibleAdapter(model, base_url=args.openai_base_url, api_key_env=args.openai_api_key_env)
            )
            client = LocalClient()
            lookup = client.lookup(args.question, limit=args.limit)
            result = adapter.generate(ModelRequest(question=args.question, context=context_from_lookup(lookup.items)))
        except (LocalClientError, ModelAdapterError) as exc:
            print(f"cervel ask failed: {exc}")
            return 2
        print(f"Using: {result.model}")
        print(result.text)
        return 0

    if args.command == "demo" and args.demo_command == "continuity":
        if args.cloud_model and not args.send_context_to_cloud:
            print("cervel demo continuity refused cloud context without --send-context-to-cloud")
            return 2
        try:
            return run_continuity_demo(
                ollama_model=args.ollama_model,
                cloud_model=args.cloud_model,
                cloud_base_url=args.cloud_base_url,
                cloud_api_key_env=args.cloud_api_key_env,
                send_context_to_cloud=args.send_context_to_cloud,
            )
        except (LocalClientError, ModelAdapterError, ValidationDependencyError, RuntimeError, ValueError) as exc:
            print(f"cervel demo continuity failed: {exc}")
            return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
