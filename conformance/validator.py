#!/usr/bin/env python3
"""Validate synthetic public CERVEL conformance fixtures.

This utility checks fixture JSON against the deliberately published example
schemas in this repository. It does not implement or test private CERVEL
runtime behavior, authorization, retrieval, knowledge compilation, provenance,
synchronization, cryptography, model routing, storage, or deployment logic.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
FIXTURE_DIR = ROOT / "conformance" / "fixtures"

SCHEMA_FILES = {
    "knowledge-reference": "knowledge-reference.example.schema.json",
    "capture-envelope": "capture-envelope.example.schema.json",
    "lookup-request": "lookup-request.example.schema.json",
    "lookup-result": "lookup-result.example.schema.json",
    "error-envelope": "error-envelope.example.schema.json",
    "capability-discovery": "capability-discovery.example.schema.json",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_registry() -> tuple[Registry, dict[str, dict]]:
    registry = Registry()
    schemas: dict[str, dict] = {}

    for contract, filename in SCHEMA_FILES.items():
        schema = load_json(SCHEMA_DIR / filename)
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            raise ValueError(f"Schema {filename} is missing a non-empty $id")
        registry = registry.with_resource(schema_id, Resource.from_contents(schema))
        schemas[contract] = schema

    return registry, schemas


def validate_fixture(
    contract: str,
    fixture: Path,
    registry: Registry,
    schemas: dict[str, dict],
) -> tuple[bool, str]:
    schema = schemas[contract]
    instance = load_json(fixture)
    validator = Draft202012Validator(schema, registry=registry)
    errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.path))

    expected_valid = fixture.name.startswith("valid-")
    actual_valid = not errors

    if expected_valid == actual_valid:
        return True, "valid" if actual_valid else "invalid as expected"

    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "<root>"
        return False, f"unexpected validation failure at {location}: {first.message}"

    return False, "fixture unexpectedly validated"


def selected_contracts(requested: list[str] | None) -> list[str]:
    if not requested:
        return list(SCHEMA_FILES)

    unknown = sorted(set(requested) - set(SCHEMA_FILES))
    if unknown:
        raise ValueError(f"Unknown contract(s): {', '.join(unknown)}")

    return requested


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate synthetic fixtures against public CERVEL schemas."
    )
    parser.add_argument(
        "contracts",
        nargs="*",
        help="Optional contract names to validate; defaults to all published fixture sets.",
    )
    args = parser.parse_args()

    try:
        registry, schemas = build_registry()
        contracts = selected_contracts(args.contracts)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    failures = 0
    checked = 0

    for contract in contracts:
        directory = FIXTURE_DIR / contract
        if not directory.is_dir():
            print(f"FAIL {contract}: fixture directory not found")
            failures += 1
            continue

        fixtures = sorted(
            path
            for path in directory.glob("*.json")
            if path.name.startswith(("valid-", "invalid-"))
        )

        if not fixtures:
            print(f"FAIL {contract}: no valid-/invalid- JSON fixtures found")
            failures += 1
            continue

        for fixture in fixtures:
            checked += 1
            try:
                passed, detail = validate_fixture(contract, fixture, registry, schemas)
            except (OSError, json.JSONDecodeError) as exc:
                passed, detail = False, f"could not read fixture: {exc}"

            status = "PASS" if passed else "FAIL"
            print(f"{status} {contract}/{fixture.name}: {detail}")
            if not passed:
                failures += 1

    print(f"\nChecked {checked} fixture(s); failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
