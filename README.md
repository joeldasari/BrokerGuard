# BrokerGuard

**BrokerGuard: Automated Security Scanning and Hardening Validation for MQTT-Based IoT Messaging Brokers**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](#quick-start)
[![MQTT](https://img.shields.io/badge/MQTT-Broker%20Security-orange)](#scanner-checks)
[![Docker](https://img.shields.io/badge/Docker-Mosquitto%20Lab-2496ED)](#docker-lab-instructions)
[![Security](https://img.shields.io/badge/Security-MQTT%20Hardening-critical)](#project-overview)

BrokerGuard is a student-friendly, production-style Python tool that evaluates MQTT broker security controls and reports clear PASS/FAIL outcomes. It is built for capstone demonstrations, local testing, and reproducible security hardening validation.

## Project Overview

MQTT brokers are often deployed in IoT networks with weak defaults (anonymous access, no TLS, broad topic permissions). BrokerGuard helps identify these issues quickly by running protocol-level checks that model realistic abuse paths.

## Architecture

BrokerGuard follows a modular design:

- `brokerguard.py`: CLI entrypoint and result rendering
- `brokerguard/scanner.py`: central orchestration and result model
- `brokerguard/checks/*.py`: one module per security control
- `brokerguard/utils/logger.py`: logging helper
- `docker/`: Mosquitto lab with insecure/hardened profiles

Flow:

1. CLI parses target config.
2. Scanner runs all checks.
3. Each check returns `status` + `message`.
4. CLI prints colored summary and risk level (or JSON).

## Folder Structure

```text
BrokerGuard/
├── brokerguard/
│   ├── __init__.py
│   ├── scanner.py
│   ├── checks/
│   │   ├── __init__.py
│   │   ├── anonymous.py
│   │   ├── auth.py
│   │   ├── tls.py
│   │   ├── acl.py
│   │   └── publish.py
│   └── utils/
│       └── logger.py
├── docker/
│   ├── docker-compose.yml
│   ├── mosquitto.conf
│   ├── profiles/
│   │   ├── insecure.conf
│   │   └── hardened.conf
│   ├── secrets/
│   │   ├── acl.txt
│   │   └── passwords.txt
│   ├── certs/
│   ├── data/
│   └── log/
├── docs/
│   ├── SETUP.md
│   ├── RESULTS.md
│   └── SCREENSHOTS.md
├── examples/
│   ├── insecure-output.txt
│   ├── hardened-output.txt
│   └── hardened-output.json
├── tests/
│   ├── __init__.py
│   └── test_scanner.py
├── .gitignore
├── Makefile
├── brokerguard.py
├── requirements.txt
└── README.md
```

## Quick Start

```bash
cd BrokerGuard
make install
source .venv/bin/activate
make scan
```

Also supported:

```bash
python brokerguard.py
python brokerguard.py --json
python brokerguard.py --demo
python brokerguard.py --demo --json
```

`--demo` prints **DEMO MODE – SIMULATED RESULTS** for environments where Docker is unavailable.

## 5-Minute Demo

For a timed classroom/lab walkthrough, follow `docs/DEMO_GUIDE.md`.

## Docker Lab Instructions

### Insecure profile

```bash
make up-insecure
make scan
```

### Hardened profile

1. Generate a password file:

```bash
cd docker
docker run --rm -it -v "$PWD/secrets:/secrets" eclipse-mosquitto:2 mosquitto_passwd -c /secrets/passwords.txt student
cd ..
```

2. Place TLS certs in `docker/certs/`:

- `ca.crt`
- `server.crt`
- `server.key`

3. Start and scan:

```bash
make up-hardened
make scan
make scan-json
```

Stop environment:

```bash
make down
```

## Scanner Checks

| Check | What BrokerGuard Tries | PASS Condition | FAIL Condition |
|---|---|---|---|
| Anonymous Access | Connect with no username/password | Connection rejected | Connection accepted |
| Authentication Enforcement | Connect with invalid credentials | Invalid login denied | Invalid login accepted |
| TLS Enforcement | Connect via TLS on `8883` and test plaintext `1883` | TLS works and plaintext is disabled | TLS fails or plaintext still open |
| Topic Authorization (ACL) | Subscribe to `admin/#` | Subscription denied | Subscription allowed |
| Publish Injection | Publish to `actuators/control` | Publish blocked/denied | Publish accepted |

## Sample Output

### Text output

```text
BrokerGuard Scan Results
Target: host=localhost, plaintext_port=1883, tls_port=8883

[PASS] Anonymous access blocked (connection refused)
[PASS] Authentication enforced (invalid credentials rejected)
[PASS] TLS enforced (TLS connection established successfully; Plaintext MQTT port is disabled)
[PASS] ACL enforced (broker denied subscription to 'admin/#')
[PASS] Publish injection blocked for 'actuators/control' (publish rc=5)

Total PASS: 5
Total FAIL: 0
Overall Risk Level: LOW
================================
```

### JSON output

```bash
python brokerguard.py --json
```

Produces structured JSON with:

- target host/ports
- pass/fail summary
- risk level
- per-check details

In demo mode:

```bash
python brokerguard.py --demo --json
```

JSON includes both simulated profiles (`insecure` and `hardened`) under a single demo payload.

## Makefile Commands

- `make install` - create virtual environment and install dependencies
- `make up-insecure` - start insecure Mosquitto profile
- `make up-hardened` - start hardened Mosquitto profile
- `make down` - stop Docker lab
- `make scan` - run text scan
- `make scan-json` - run JSON scan
- `make test` - run unit tests
- `make clean` - remove cache, venv, and logs

## Submission Documents

- `docs/SETUP.md`
- `docs/RESULTS.md`
- `docs/SCREENSHOTS.md`
- `docs/PROFESSOR_SUMMARY.md`
- `docs/CONTRIBUTIONS.md`

## Limitations and Future Work

Current limitations:

- Checks depend on active broker configuration and network reachability.
- TLS validation in lab may use relaxed settings unless CA cert is supplied.
- The scanner focuses on five high-value controls, not full MQTT auditing.

Future improvements:

- Add CSV/HTML report export.
- Add CVSS-style scoring per finding.
- Add CI pipeline integration for automated hardening gates.
- Add fuzzing checks for malformed MQTT packets.
