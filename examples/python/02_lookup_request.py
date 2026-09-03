from __future__ import annotations

import json

from cervel_public import LookupRequest


request = LookupRequest(
    query="When is the design review?",
    limit=3,
    scope="public-example",
)

payload = request.to_dict()
assert payload == {
    "version": "0.1-draft",
    "query": "When is the design review?",
    "limit": 3,
    "scope": "public-example",
}

print(json.dumps(payload, indent=2, sort_keys=True))
