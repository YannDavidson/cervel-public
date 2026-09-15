"""Public Python helpers for CERVEL experimental interoperability drafts."""

from .client import (
    DEFAULT_LOCAL_BASE_URL,
    LocalClient,
    LocalClientConfigurationError,
    LocalClientConnectionError,
    LocalClientError,
    LocalClientMalformedResponseError,
    LocalClientResponseError,
)
from .model_adapters import (
    ModelAdapter,
    ModelAdapterConnectionError,
    ModelAdapterError,
    ModelAdapterResponseError,
    ModelContextItem,
    ModelRequest,
    ModelResponse,
    OllamaAdapter,
    build_prompt,
    context_from_lookup,
    render_context,
)
from .models import (
    PUBLIC_DRAFT_VERSION,
    CapabilityContract,
    CapabilityDiscovery,
    CaptureEnvelope,
    ErrorEnvelope,
    KnowledgeReference,
    LookupRequest,
    LookupResult,
    LookupResultItem,
)
from .validation import (
    SUPPORTED_CONTRACTS,
    ContractValidationError,
    UnsupportedContractError,
    ValidationDependencyError,
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

__all__ = [
    "DEFAULT_LOCAL_BASE_URL", "PUBLIC_DRAFT_VERSION", "SUPPORTED_CONTRACTS",
    "CapabilityContract", "CapabilityDiscovery", "CaptureEnvelope", "ContractValidationError",
    "ErrorEnvelope", "KnowledgeReference", "LocalClient", "LocalClientConfigurationError",
    "LocalClientConnectionError", "LocalClientError", "LocalClientMalformedResponseError",
    "LocalClientResponseError", "LookupRequest", "LookupResult", "LookupResultItem",
    "ModelAdapter", "ModelAdapterConnectionError", "ModelAdapterError", "ModelAdapterResponseError",
    "ModelContextItem", "ModelRequest", "ModelResponse", "OllamaAdapter", "UnsupportedContractError",
    "ValidationDependencyError", "build_prompt", "context_from_lookup", "get_public_schema",
    "render_context", "validate_capability_discovery", "validate_capture_envelope",
    "validate_error_envelope", "validate_knowledge_reference", "validate_lookup_request",
    "validate_lookup_result", "validate_payload", "validation_errors",
]
