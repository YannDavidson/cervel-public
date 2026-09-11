from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SDK_ROOT = ROOT / "sdk" / "python"
SCHEMA_DIR = ROOT / "schemas"
sys.path.insert(0, str(SDK_ROOT))

from cervel_public import (  # noqa: E402
    CapabilityContract,
    CapabilityDiscovery,
    CaptureEnvelope,
    ContractValidationError,
    ErrorEnvelope,
    KnowledgeReference,
    LookupRequest,
    LookupResult,
    LookupResultItem,
    SUPPORTED_CONTRACTS,
    UnsupportedContractError,
    get_public_schema,
    validate_capability_discovery,
    validate_capture_envelope,
    validate_error_envelope,
    validate_knowledge_reference,
    validate_lookup_request,
    validate_lookup_result,
    validate_payload,
    validation_errors,
)

SCHEMA_FILES = {
    "capture-envelope": "capture-envelope.example.schema.json",
    "lookup-request": "lookup-request.example.schema.json",
    "knowledge-reference": "knowledge-reference.example.schema.json",
    "lookup-result": "lookup-result.example.schema.json",
    "error-envelope": "error-envelope.example.schema.json",
    "capability-discovery": "capability-discovery.example.schema.json",
}


class PublicValidationHelperTests(unittest.TestCase):
    def test_supported_contracts_are_exactly_public_schema_set(self) -> None:
        self.assertEqual(tuple(SCHEMA_FILES), SUPPORTED_CONTRACTS)

    def test_embedded_schemas_match_authoritative_repository_schemas(self) -> None:
        for contract, filename in SCHEMA_FILES.items():
            authoritative = json.loads((SCHEMA_DIR / filename).read_text(encoding="utf-8"))
            self.assertEqual(authoritative, get_public_schema(contract), contract)

    def test_schema_accessor_returns_defensive_copy(self) -> None:
        schema = get_public_schema("capture-envelope")
        schema["required"].append("private-field")
        self.assertNotIn("private-field", get_public_schema("capture-envelope")["required"])

    def test_validate_capture_envelope_accepts_model_and_mapping(self) -> None:
        model = CaptureEnvelope(content="Synthetic public example", content_type="text/plain")
        validate_capture_envelope(model)
        validate_payload("capture-envelope", model.to_dict())

    def test_specialized_helpers_accept_all_public_models(self) -> None:
        reference = KnowledgeReference(id="example-knowledge-1", kind="note")
        validate_knowledge_reference(reference)
        validate_lookup_request(LookupRequest(query="synthetic", limit=2))
        validate_lookup_result(
            LookupResult(items=(LookupResultItem(reference=reference, text="Example"),))
        )
        validate_error_envelope(ErrorEnvelope(code="example_error"))
        validate_capability_discovery(
            CapabilityDiscovery(
                contracts=(CapabilityContract(name="lookup-request", version="0.1-draft"),)
            )
        )

    def test_invalid_payload_raises_structured_validation_error(self) -> None:
        with self.assertRaises(ContractValidationError) as caught:
            validate_payload("knowledge-reference", {"version": "0.1-draft", "id": ""})
        self.assertEqual("knowledge-reference", caught.exception.contract)
        self.assertTrue(caught.exception.errors)
        self.assertIn("id", str(caught.exception))

    def test_validation_errors_is_non_throwing_for_schema_failures(self) -> None:
        errors = validation_errors(
            "lookup-request", {"version": "0.1-draft", "query": "x", "limit": -1}
        )
        self.assertEqual(1, len(errors))
        self.assertIn("limit", errors[0])

    def test_lookup_result_resolves_embedded_knowledge_reference(self) -> None:
        with self.assertRaises(ContractValidationError):
            validate_lookup_result(
                {
                    "version": "0.1-draft",
                    "items": [{"reference": {"version": "0.1-draft", "id": ""}}],
                }
            )

    def test_unsupported_contract_fails_closed(self) -> None:
        with self.assertRaises(UnsupportedContractError):
            get_public_schema("private-runtime")
        with self.assertRaises(UnsupportedContractError):
            validate_payload("private-runtime", {})

    def test_non_mapping_without_to_dict_is_rejected(self) -> None:
        with self.assertRaises(TypeError):
            validate_capture_envelope("not-a-payload")


if __name__ == "__main__":
    unittest.main()
