"""Central scanner orchestration for BrokerGuard."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Callable, List

from brokerguard.checks import (
    check_acl_subscription,
    check_anonymous_access,
    check_auth_enforcement,
    check_publish_injection,
    check_tls_enforcement,
)
from brokerguard.utils.logger import setup_logger


@dataclass
class CheckResult:
    name: str
    status: str
    message: str


class BrokerScanner:
    """Runs all security checks against an MQTT broker target."""

    def __init__(
        self,
        host: str = "localhost",
        plaintext_port: int = 1883,
        tls_port: int = 8883,
        username: str | None = None,
        password: str | None = None,
        ca_cert: str | None = None,
        timeout: int = 5,
        retries: int = 1,
    ) -> None:
        self.host = host
        self.plaintext_port = plaintext_port
        self.tls_port = tls_port
        self.username = username
        self.password = password
        self.ca_cert = ca_cert
        self.timeout = timeout
        self.retries = max(1, retries)
        self.logger = setup_logger()

    def _run_with_retry(self, check_fn: Callable[[], dict], check_name: str) -> dict:
        last_result: dict = {"status": "FAIL", "message": "No result"}
        for attempt in range(1, self.retries + 1):
            self.logger.info("Running check '%s' (attempt %s/%s)", check_name, attempt, self.retries)
            last_result = check_fn()
            if last_result.get("status") in {"PASS", "FAIL"}:
                return last_result
        return last_result

    def run_all_checks(self) -> List[CheckResult]:
        """Run all BrokerGuard security checks and return structured results."""
        checks: list[tuple[str, Callable[[], dict]]] = [
            (
                "Anonymous Access Check",
                lambda: check_anonymous_access(self.host, self.plaintext_port, self.timeout),
            ),
            (
                "Authentication Enforcement",
                lambda: check_auth_enforcement(self.host, self.plaintext_port, timeout=self.timeout),
            ),
            (
                "TLS Enforcement",
                lambda: check_tls_enforcement(
                    self.host,
                    tls_port=self.tls_port,
                    plaintext_port=self.plaintext_port,
                    ca_cert=self.ca_cert,
                    timeout=self.timeout,
                ),
            ),
            (
                "Topic Authorization (ACL)",
                lambda: check_acl_subscription(
                    self.host,
                    self.plaintext_port,
                    username=self.username,
                    password=self.password,
                    timeout=self.timeout,
                ),
            ),
            (
                "Publish Injection",
                lambda: check_publish_injection(
                    self.host,
                    self.plaintext_port,
                    username=self.username,
                    password=self.password,
                    timeout=self.timeout,
                ),
            ),
        ]

        results: List[CheckResult] = []
        for check_name, check_fn in checks:
            raw = self._run_with_retry(check_fn, check_name)
            results.append(
                CheckResult(
                    name=check_name,
                    status=raw.get("status", "FAIL"),
                    message=raw.get("message", "Unknown check result"),
                )
            )
        return results

    @staticmethod
    def to_json(results: List[CheckResult]) -> str:
        """Serialize scan results to JSON."""
        return json.dumps([asdict(r) for r in results], indent=2)
