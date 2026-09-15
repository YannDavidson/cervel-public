"""Command-line entry point for the public CERVEL developer surface."""

from __future__ import annotations

import argparse

from .client import LocalClient, LocalClientError
from .model_adapters import ModelAdapterError, ModelRequest, OllamaAdapter, context_from_lookup
from .sandbox import DEFAULT_PORT, ValidationDependencyError, run_dev_server


def _ollama_model(value: str) -> str:
    prefix = "ollama:"
    if not value.startswith(prefix) or not value[len(prefix):].strip():
        raise argparse.ArgumentTypeError("public alpha supports model selectors like ollama:llama3")
    return value[len(prefix):].strip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cervel", description="CERVEL public developer tools")
    subcommands = parser.add_subparsers(dest="command", required=True)
    dev = subcommands.add_parser("dev", help="run the local public developer sandbox")
    dev.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"loopback port (default: {DEFAULT_PORT})")

    ask = subcommands.add_parser("ask", help="ask a developer-selected model using public sandbox lookup context")
    ask.add_argument("question")
    ask.add_argument("--model", required=True, type=_ollama_model, metavar="ollama:MODEL")
    ask.add_argument("--limit", type=int, default=5)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "dev":
        if not 1 <= args.port <= 65535:
            raise SystemExit("--port must be between 1 and 65535")
        try:
            run_dev_server(port=args.port)
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
        client = LocalClient()
        adapter = OllamaAdapter(args.model)
        try:
            lookup = client.lookup(args.question, limit=args.limit)
            result = adapter.generate(ModelRequest(question=args.question, context=context_from_lookup(lookup.items)))
        except (LocalClientError, ModelAdapterError) as exc:
            print(f"cervel ask failed: {exc}")
            return 2
        print(f"Using: {result.model}")
        print(result.text)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
