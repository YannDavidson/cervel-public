from __future__ import annotations

import json

from cervel_public import KnowledgeReference, LookupResult, LookupResultItem


result = LookupResult(
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

payload = result.to_dict()
assert payload == {
    "version": "0.1-draft",
    "items": [
        {
            "reference": {
                "version": "0.1-draft",
                "id": "example-knowledge-1",
                "kind": "note",
            },
            "text": "The design review is scheduled for Friday.",
        }
    ],
}

for item in result.items:
    assert item.reference.id

print(json.dumps(payload, indent=2, sort_keys=True))
