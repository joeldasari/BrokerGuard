"""Anonymous access security check."""

from __future__ import annotations

import socket
from typing import Dict

import paho.mqtt.client as mqtt


Result = Dict[str, str]


def check_anonymous_access(host: str, port: int = 1883, timeout: int = 5) -> Result:
    """Check whether anonymous MQTT connections are blocked."""
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        # We don't set username/password intentionally for this test.

        client.connect(host, port, timeout)
        client.loop_start()
        client.disconnect()
        client.loop_stop()
        return {
            "status": "FAIL",
            "message": "Anonymous access allowed (connected without credentials)",
        }
    except (ConnectionRefusedError, TimeoutError, socket.timeout):
        return {
            "status": "PASS",
            "message": "Anonymous access blocked (connection refused)",
        }
    except Exception as exc:  # Broad handling for broker/network-specific errors.
        msg = str(exc).lower()
        if "not authorised" in msg or "not authorized" in msg:
            return {
                "status": "PASS",
                "message": "Anonymous access blocked (authorization failure)",
            }
        return {
            "status": "FAIL",
            "message": f"Anonymous access check inconclusive due to error: {exc}",
        }
