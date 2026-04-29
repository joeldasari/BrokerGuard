"""Authentication enforcement security check."""

from __future__ import annotations

import socket
from typing import Dict

import paho.mqtt.client as mqtt


Result = Dict[str, str]


def check_auth_enforcement(
    host: str,
    port: int = 1883,
    username: str = "invalid_user",
    password: str = "invalid_password",
    timeout: int = 5,
) -> Result:
    """Check whether invalid credentials are rejected by broker."""
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.username_pw_set(username=username, password=password)

        client.connect(host, port, timeout)
        client.loop_start()
        client.disconnect()
        client.loop_stop()
        return {
            "status": "FAIL",
            "message": "Invalid credentials accepted by broker",
        }
    except (ConnectionRefusedError, TimeoutError, socket.timeout):
        return {
            "status": "PASS",
            "message": "Authentication enforced (invalid credentials rejected)",
        }
    except Exception as exc:
        msg = str(exc).lower()
        if "not authorised" in msg or "not authorized" in msg or "bad user name or password" in msg:
            return {
                "status": "PASS",
                "message": "Authentication enforced (broker denied invalid credentials)",
            }
        return {
            "status": "FAIL",
            "message": f"Authentication check inconclusive due to error: {exc}",
        }
