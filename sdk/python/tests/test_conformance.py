from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[3]
SDK_ROOT = ROOT / "sdk" / "python"
SCHEMA_DIR = ROOT / "schemas"
sys.path.insert(0, str(SDK_ROOT))

from cervel_public import (  # noqa: E402
    CapabilityContract,
    CapabilityDiscovery,
    CaptureEnvelope,
    ErrorEnvelope,
    KnowledgeReference,
    LookupRequest,
    LookupResult,
    LookupResultItem,
)

SCHEMA_FILES = {
    "knowledge-reference": "knowledge-reference.example.schema.json",
    "capture-envelope": "capture-envelope.example.schema.json",
    "lookup-request": "lookup-request.example.schema.json",
    "lookup-result": "lookup-result.example.schema.json",
    "error-envelope": "error-envelope.example.schema.json",
    "capability-discovery": "capability-discovery.example.schema.json",
}


def load_schema(filename: str) -> dict:
    return json.loads((SCHEMA_DIR / filename).read_text(encoding="utf-8"))


def registry_and_schemas() -> tuple[Registry, dict[str, dict]]:
    registry = Registry()
    schemas: dict[str, dict] = {}
    for contract, filename in SCHEMA_FILES.items():
        schema = load_schema(filename)
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
        schemas[contract] = schema
    return registry, schemas


class PublicSdkConformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry, cls.schemas = registry_and_schemas()

    def assert_conforms(self, contract: str, payload: dict) -> None:
        validator = Draft202012Validator(
            self.schemas[contract],
            registry=self.registry,
        )
        errors = list(validator.iter_errors(payload))
        self.assertEqual([], errors, [error.message for error in errors])

    def test_knowledge_reference(self) -> None:
        self.assert_conforms(
            "knowledge-reference",
            KnowledgeReference(id="example-knowledge-1", kind="note").to_dict(),
        )

    def test_capture_envelope(self) -> None:
        self.assert_conforms(
            "capture-envelope",
            CaptureEnvelope(content="Synthetic public example", content_type="text/plain").to_dict(),
        )

    def test_lookup_request(self) -> None:
        self.assert_conforms(
            "lookup-request",
            LookupRequest(query="synthetic example", limit=3, scope="public-example").to_dict(),
        )

    def test_lookup_result_resolves_knowledge_reference(self) -> None:
        payload = LookupResult(
            items=(
                LookupResultItem(
                    reference=KnowledgeReference(id="example-knowledge-1"),
                    text="Synthetic public result",
                ),
            )
        ).to_dict()
        self.assert_conforms("lookup-result", payload)

    def test_error_envelope(self) -> None:
        self.assert_conforms(
            "error-envelope",
            ErrorEnvelope(code="example_error", message="Synthetic public error").to_dict(),
        )

    def test_capability_discovery(self) -> None:
        self.assert_conforms(
            "capability-discovery",
            CapabilityDiscovery(
                contracts=(CapabilityContract(name="lookup-request", version="0.1-draft"),)
            ).to_dict(),
        )


if __name__ == "__main__":
    unittest.main()
