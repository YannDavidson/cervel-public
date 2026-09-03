from __future__ import annotations

import json

from cervel_public import CaptureEnvelope


capture = CaptureEnvelope(
    content="The design review is scheduled for Friday.",
    content_type="text/plain",
    title="Synthetic project note",
)

payload = capture.to_dict()
assert payload == {
    "version": "0.1-draft",
    "content": "The design review is scheduled for Friday.",
    "content_type": "text/plain",
    "title": "Synthetic project note",
}

print(json.dumps(payload, indent=2, sort_keys=True))
