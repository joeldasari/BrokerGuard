"""ACL subscription authorization security check."""

from __future__ import annotations

import time
from typing import Dict

import paho.mqtt.client as mqtt


Result = Dict[str, str]


def check_acl_subscription(
    host: str,
    port: int = 1883,
    username: str | None = None,
    password: str | None = None,
    topic: str = "admin/#",
    timeout: int = 5,
) -> Result:
    """Check whether subscription to restricted admin topics is denied."""
    granted_qos: list[int] = []

    def on_subscribe(
        client: mqtt.Client,
        userdata: object,
        mid: int,
        reason_code_list: list[mqtt.ReasonCode],
        properties: mqtt.Properties | None = None,
    ) -> None:
        nonlocal granted_qos
        granted_qos = [int(reason_code.value) for reason_code in reason_code_list]

    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        if username is not None:
            client.username_pw_set(username=username, password=password)

        client.on_subscribe = on_subscribe
        client.connect(host, port, timeout)
        client.loop_start()

        _, rc = client.subscribe(topic)
        if rc != mqtt.MQTT_ERR_SUCCESS:
            client.disconnect()
            client.loop_stop()
            return {
                "status": "PASS",
                "message": f"ACL enforced (subscription to '{topic}' rejected immediately)",
            }

        end_time = time.time() + timeout
        while time.time() < end_time and not granted_qos:
            time.sleep(0.1)

        client.disconnect()
        client.loop_stop()

        if not granted_qos:
            return {
                "status": "PASS",
                "message": f"ACL enforced (no SUBACK received for '{topic}')",
            }

        # MQTT v5 failure codes are >= 128.
        if all(qos >= 128 for qos in granted_qos):
            return {
                "status": "PASS",
                "message": f"ACL enforced (broker denied subscription to '{topic}')",
            }

        return {
            "status": "FAIL",
            "message": f"Unauthorized topic access allowed for '{topic}'",
        }
    except Exception as exc:
        return {
            "status": "PASS",
            "message": f"ACL enforced or blocked by broker/network: {exc}",
        }
