"""Minimal LocalClient example for the public localhost sandbox.

Start the sandbox first with `cervel dev`, then set CERVEL_EXAMPLE_LIVE=1 to
exercise the full capture/lookup flow. Without that flag, the example remains
safe to execute in offline conformance CI and prints the exact public calls.
"""

from __future__ import annotations

import os

from cervel_public import LocalClient


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
