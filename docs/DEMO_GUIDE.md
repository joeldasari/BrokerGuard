# 5-Minute Demo Guide

This guide is designed for a short academic demonstration of BrokerGuard.

## Demo Objective

Show that BrokerGuard can detect insecure MQTT broker settings and verify security improvements after hardening.

## Timeline (Approx. 5 Minutes)

## 1) Start Insecure Broker (1 minute)

```bash
make up-insecure
```

Explain that this profile intentionally allows weak settings (anonymous access, no TLS enforcement, weak/no ACL restrictions).

## 2) Run First Scan (1 minute)

```bash
make scan
```

What to say:

- BrokerGuard tests five security controls.
- In insecure mode, several checks should return `FAIL`.
- The overall risk level should typically be `HIGH` (or `MEDIUM` depending on environment).

## 3) Explain Failed Checks (1 minute)

Briefly interpret each likely failure:

- Anonymous access accepted
- Invalid credentials accepted or authentication weak
- TLS not enforced and plaintext still available
- Unauthorized subscription to `admin/#` allowed
- Unauthorized publish to `actuators/control` allowed

## 4) Switch to Hardened Broker (1 minute)

Stop insecure profile:

```bash
make down
```

Start hardened profile:

```bash
make up-hardened
```

Explain that hardened mode enables authentication, TLS listener, and ACL restrictions.

## 5) Run Hardened Scan and Compare (1 minute)

```bash
make scan
```

What to say:

- `PASS` results should increase significantly.
- Risk level should drop (ideally to `LOW`).
- This demonstrates practical security validation and measurable hardening impact.

## Optional Closing (30 seconds)

- Show JSON output for reporting automation:

```bash
make scan-json
```

- Mention that setup details and expected outcomes are documented in `docs/SETUP.md` and `docs/RESULTS.md`.
