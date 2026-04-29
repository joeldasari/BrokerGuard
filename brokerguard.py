"""CLI entry point for BrokerGuard."""

from __future__ import annotations

import argparse
import json
from colorama import Fore, Style, init

from brokerguard.scanner import BrokerScanner, CheckResult


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="BrokerGuard MQTT Security Scanner")
    parser.add_argument("--host", default="localhost", help="Target MQTT broker host")
    parser.add_argument("--port", type=int, default=1883, help="Target plaintext MQTT port")
    parser.add_argument("--tls-port", type=int, default=8883, help="Target TLS MQTT port")
    parser.add_argument("--username", default=None, help="Valid username for authenticated checks")
    parser.add_argument("--password", default=None, help="Valid password for authenticated checks")
    parser.add_argument("--ca-cert", default=None, help="CA certificate file path for TLS validation")
    parser.add_argument("--timeout", type=int, default=5, help="Connection timeout (seconds)")
    parser.add_argument("--retries", type=int, default=1, help="Retry count for each check")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output instead of colored text",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run simulated insecure and hardened demo results",
    )
    return parser.parse_args()


def color_status(status: str) -> str:
    if status == "PASS":
        return f"{Fore.GREEN}[PASS]{Style.RESET_ALL}"
    return f"{Fore.RED}[FAIL]{Style.RESET_ALL}"


def get_risk_level(fail_count: int) -> str:
    if fail_count >= 3:
        return "HIGH"
    if fail_count >= 1:
        return "MEDIUM"
    return "LOW"


def summarize_results(results: list[CheckResult]) -> tuple[int, int, str]:
    pass_count = sum(1 for result in results if result.status == "PASS")
    fail_count = sum(1 for result in results if result.status == "FAIL")
    risk_level = get_risk_level(fail_count)
    return pass_count, fail_count, risk_level


def get_demo_results() -> dict[str, list[CheckResult]]:
    insecure = [
        CheckResult("Anonymous Access Check", "FAIL", "Anonymous access allowed (connected without credentials)"),
        CheckResult("Authentication Enforcement", "FAIL", "Invalid credentials accepted by broker"),
        CheckResult(
            "TLS Enforcement",
            "FAIL",
            "TLS enforcement failed: TLS connection failed: [Errno 61] Connection refused; Plaintext MQTT port is still accessible",
        ),
        CheckResult("Topic Authorization (ACL)", "FAIL", "Unauthorized topic access allowed for 'admin/#'"),
        CheckResult("Publish Injection", "FAIL", "Unauthorized publish allowed to 'actuators/control'"),
    ]
    hardened = [
        CheckResult("Anonymous Access Check", "PASS", "Anonymous access blocked (connection refused)"),
        CheckResult("Authentication Enforcement", "PASS", "Authentication enforced (invalid credentials rejected)"),
        CheckResult(
            "TLS Enforcement",
            "PASS",
            "TLS enforced (TLS connection established successfully; Plaintext MQTT port is disabled)",
        ),
        CheckResult("Topic Authorization (ACL)", "PASS", "ACL enforced (broker denied subscription to 'admin/#')"),
        CheckResult("Publish Injection", "PASS", "Publish injection blocked for 'actuators/control' (publish rc=5)"),
    ]
    return {"insecure": insecure, "hardened": hardened}


def print_results_block(title: str, host: str, port: int, tls_port: int, results: list[CheckResult]) -> None:
    pass_count, fail_count, risk_level = summarize_results(results)
    print(title)
    print(f"Target: host={host}, plaintext_port={port}, tls_port={tls_port}")
    print()
    for result in results:
        print(f"{color_status(result.status)} {result.message}")
    print()
    print(f"Total PASS: {Fore.GREEN}{pass_count}{Style.RESET_ALL}")
    print(f"Total FAIL: {Fore.RED}{fail_count}{Style.RESET_ALL}")
    print(f"Overall Risk Level: {Fore.YELLOW}{risk_level}{Style.RESET_ALL}")
    print("=" * 32)


def main() -> None:
    init(autoreset=True)
    args = parse_args()

    if args.demo:
        demo_results = get_demo_results()

        if args.json:
            output = {"label": "DEMO MODE – SIMULATED RESULTS", "profiles": {}}
            for profile_name, profile_results in demo_results.items():
                pass_count, fail_count, risk_level = summarize_results(profile_results)
                output["profiles"][profile_name] = {
                    "target": {
                        "host": args.host,
                        "plaintext_port": args.port,
                        "tls_port": args.tls_port,
                    },
                    "summary": {
                        "pass_count": pass_count,
                        "fail_count": fail_count,
                        "risk_level": risk_level,
                    },
                    "results": [result.__dict__ for result in profile_results],
                }
            print(json.dumps(output, indent=2))
            return

        print("DEMO MODE – SIMULATED RESULTS")
        print()
        print_results_block(
            "BrokerGuard Scan Results (Insecure Profile)",
            args.host,
            args.port,
            args.tls_port,
            demo_results["insecure"],
        )
        print()
        print_results_block(
            "BrokerGuard Scan Results (Hardened Profile)",
            args.host,
            args.port,
            args.tls_port,
            demo_results["hardened"],
        )
        return

    scanner = BrokerScanner(
        host=args.host,
        plaintext_port=args.port,
        tls_port=args.tls_port,
        username=args.username,
        password=args.password,
        ca_cert=args.ca_cert,
        timeout=args.timeout,
        retries=args.retries,
    )
    results = scanner.run_all_checks()
    pass_count, fail_count, risk_level = summarize_results(results)

    if args.json:
        payload = {
            "target": {
                "host": args.host,
                "plaintext_port": args.port,
                "tls_port": args.tls_port,
            },
            "summary": {
                "pass_count": pass_count,
                "fail_count": fail_count,
                "risk_level": risk_level,
            },
            "results": [result.__dict__ for result in results],
        }
        print(json.dumps(payload, indent=2))
        return

    print_results_block("BrokerGuard Scan Results", args.host, args.port, args.tls_port, results)


if __name__ == "__main__":
    main()
