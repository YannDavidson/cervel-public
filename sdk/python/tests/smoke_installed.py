from __future__ import annotations

from pathlib import Path

import cervel_public
from cervel_public import (
    LocalClient,
    KnowledgeReference,
    LookupResult,
    LookupResultItem,
    ValidationDependencyError,
    validate_lookup_result,
)


module_path = Path(cervel_public.__file__).resolve()
assert "site-packages" in module_path.parts, module_path

client = LocalClient()
assert client.base_url == "http://127.0.0.1:8765"

payload = LookupResult(
    items=(
        LookupResultItem(
            reference=KnowledgeReference(id="installed-wheel-example"),
            text="Installed wheel smoke test",
        ),
    )
).to_dict()

assert payload == {
    "version": "0.1-draft",
    "items": [
        {
            "reference": {
                "version": "0.1-draft",
                "id": "installed-wheel-example",
            },
            "text": "Installed wheel smoke test",
        }
    ],
}

try:
    validate_lookup_result(payload)
except ValidationDependencyError:
    pass
else:
    raise AssertionError("base wheel unexpectedly has optional validation dependencies")
