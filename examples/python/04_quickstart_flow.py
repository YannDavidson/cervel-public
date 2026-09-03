from __future__ import annotations

import json

from cervel_public import (
    CaptureEnvelope,
    KnowledgeReference,
    LookupRequest,
    LookupResult,
    LookupResultItem,
)


capture = CaptureEnvelope(
    content="The design review is scheduled for Friday.",
    content_type="text/plain",
    title="Synthetic project note",
)

request = LookupRequest(
    query="When is the design review?",
    limit=3,
    scope="public-example",
)

synthetic_result = LookupResult(
    items=(
        LookupResultItem(
            reference=KnowledgeReference(
                id="example-knowledge-1",
                kind="note",
            ),
            text="The design review is scheduled for Friday.",
        ),
    )
)

flow = {
    "capture": capture.to_dict(),
    "lookup_request": request.to_dict(),
    "synthetic_lookup_result": synthetic_result.to_dict(),
}

assert flow["capture"]["version"] == "0.1-draft"
assert flow["lookup_request"]["version"] == "0.1-draft"
assert flow["synthetic_lookup_result"]["items"][0]["reference"]["id"] == "example-knowledge-1"

print(json.dumps(flow, indent=2, sort_keys=True))
