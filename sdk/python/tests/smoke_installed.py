from __future__ import annotations

from pathlib import Path

import cervel_public
from cervel_public import KnowledgeReference, LookupResult, LookupResultItem


module_path = Path(cervel_public.__file__).resolve()
assert "site-packages" in module_path.parts, module_path

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
