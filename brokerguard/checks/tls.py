"""TLS enforcement security check."""

from __future__ import annotations

import socket
import ssl
from typing import Dict

import paho.mqtt.client as mqtt


Result = Dict[str, str]


def _test_tls_connection(host: str, tls_port: int, ca_cert: str | None, timeout: int) -> tuple[bool, str]:
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        if ca_cert:
            client.tls_set(ca_certs=ca_cert, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS_CLIENT)
        else:
            # Support local lab testing where self-signed cert validation may be skipped.
            client.tls_set(cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLS_CLIENT)
            client.tls_insecure_set(True)

        client.connect(host, tls_port, timeout)
        client.loop_start()
        client.disconnect()
        client.loop_stop()
        return True, "TLS connection established successfully"
    except Exception as exc:
        return False, f"TLS connection failed: {exc}"


def _test_plaintext_disabled(host: str, plaintext_port: int, timeout: int) -> tuple[bool, str]:
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.connect(host, plaintext_port, timeout)
        client.loop_start()
        client.disconnect()
        client.loop_stop()
        return False, "Plaintext MQTT port is still accessible"
    except (ConnectionRefusedError, TimeoutError, socket.timeout):
        return True, "Plaintext MQTT port is disabled"
    except Exception:
        return True, "Plaintext MQTT blocked or restricted"


def check_tls_enforcement(
    host: str,
    tls_port: int = 8883,
    plaintext_port: int = 1883,
    ca_cert: str | None = None,
    timeout: int = 5,
) -> Result:
    """Verify TLS endpoint works and plaintext endpoint is disabled."""
    tls_ok, tls_msg = _test_tls_connection(host, tls_port, ca_cert, timeout)
    plain_disabled, plain_msg = _test_plaintext_disabled(host, plaintext_port, timeout)

    if tls_ok and plain_disabled:
        return {
            "status": "PASS",
            "message": f"TLS enforced ({tls_msg}; {plain_msg})",
        }

    failure_reasons = []
    if not tls_ok:
        failure_reasons.append(tls_msg)
    if not plain_disabled:
        failure_reasons.append(plain_msg)

    return {
        "status": "FAIL",
        "message": "TLS enforcement failed: " + "; ".join(failure_reasons),
    }
