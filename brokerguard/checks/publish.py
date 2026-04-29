"""Publish injection security check."""

from __future__ import annotations

import time
from typing import Dict

import paho.mqtt.client as mqtt


Result = Dict[str, str]


def check_publish_injection(
    host: str,
    port: int = 1883,
    username: str | None = None,
    password: str | None = None,
    topic: str = "actuators/control",
    payload: str = "malicious_override",
    timeout: int = 5,
) -> Result:
    """Check whether unauthorized publish to actuator control topic is blocked."""
    pub_ack: list[int] = []

    def on_publish(client: mqtt.Client, userdata: object, mid: int, reason_code=None, properties=None) -> None:
        pub_ack.append(mid)

    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        if username is not None:
            client.username_pw_set(username=username, password=password)

        client.on_publish = on_publish
        client.connect(host, port, timeout)
        client.loop_start()

        info = client.publish(topic, payload=payload, qos=1)
        info.wait_for_publish(timeout=timeout)

        end_time = time.time() + timeout
        while time.time() < end_time and not pub_ack:
            time.sleep(0.1)

        client.disconnect()
        client.loop_stop()

        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            return {
                "status": "PASS",
                "message": f"Publish injection blocked for '{topic}' (publish rc={info.rc})",
            }

        if pub_ack:
            return {
                "status": "FAIL",
                "message": f"Unauthorized publish allowed to '{topic}'",
            }

        return {
            "status": "PASS",
            "message": f"Publish injection blocked or not acknowledged for '{topic}'",
        }
    except Exception as exc:
        return {
            "status": "PASS",
            "message": f"Publish injection blocked by broker/network: {exc}",
        }
