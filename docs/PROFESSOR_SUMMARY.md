# Professor Summary

## Project Goal

BrokerGuard was developed as an academic cybersecurity tool to assess MQTT broker hardening status. The core objective is to detect common broker misconfigurations and report clear, interpretable PASS/FAIL outcomes.

## Implemented Modules

The implementation includes:

- CLI entrypoint (`brokerguard.py`) for running scans and rendering text/JSON output
- Central scanner orchestration (`brokerguard/scanner.py`)
- Modular checks in `brokerguard/checks/`:
  - anonymous access validation
  - authentication enforcement validation
  - TLS enforcement and plaintext exposure validation
  - ACL/topic authorization validation
  - publish injection validation
- Logging utility (`brokerguard/utils/logger.py`)

## Docker Testbed

A reproducible Mosquitto-based lab is provided in `docker/` with switchable profiles:

- `insecure` profile for vulnerability demonstration
- `hardened` profile for security baseline validation

This allows side-by-side comparison of scan outputs under different security configurations.

## Validation Approach

Validation was performed by:

- Running scans against both insecure and hardened broker profiles
- Reviewing PASS/FAIL outcomes per security control
- Generating both human-readable and JSON output
- Executing unit tests and Makefile workflow commands for reproducibility

## Limitations

- Runtime behavior depends on broker availability and environment setup.
- TLS trust in local labs may vary based on certificate provisioning.
- Scope is focused on five high-value checks, not full protocol fuzzing/audit.

## Next Steps

- Extend reporting formats (CSV/HTML)
- Integrate CI/CD security gates
- Add broader MQTT abuse-path and protocol robustness checks
- Map findings to formal security standards/frameworks
