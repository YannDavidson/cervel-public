"""Minimal LocalClient example for the public localhost sandbox.

Start the sandbox first with `cervel dev`, then set CERVEL_EXAMPLE_LIVE=1 to
exercise the full capture/lookup flow. The example also executes cleanly when
PyPI smoke tests intentionally run repository examples against an older
published prerelease that does not yet contain LocalClient.
"""

from __future__ import annotations

import os

try:
    from cervel_public import LocalClient
except ImportError:
    print("LocalClient is a repository development surface for the next prerelease.")
else:
    client = LocalClient()
    print(f"Local CERVEL sandbox: {client.base_url}")

    if os.environ.get("CERVEL_EXAMPLE_LIVE") == "1":
        reference = client.capture(
            "CERVEL knowledge should persist independently of the reasoning model.",
            source="local-client-example",
        )
        results = client.lookup("knowledge persist", limit=3)
        print(reference.to_dict())
        print(results.to_dict())
    else:
        print("Start `cervel dev` and set CERVEL_EXAMPLE_LIVE=1 to run capture + lookup.")
