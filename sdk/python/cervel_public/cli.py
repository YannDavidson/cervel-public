"""Command-line entry point for the public CERVEL developer surface."""

from __future__ import annotations

import argparse

from .sandbox import DEFAULT_PORT, ValidationDependencyError, run_dev_server


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cervel", description="CERVEL public developer tools")
    subcommands = parser.add_subparsers(dest="command", required=True)
    dev = subcommands.add_parser("dev", help="run the local public developer sandbox")
    dev.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"loopback port (default: {DEFAULT_PORT})")
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
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
