# Project Status

## Current Version

**Prototype / Academic MVP**

## Completed Features

- Modular MQTT security scanner with five checks:
  - anonymous access
  - authentication enforcement
  - TLS enforcement
  - ACL subscription restriction
  - publish injection restriction
- Text and JSON scan output modes
- PASS/FAIL summary with risk level classification
- Dockerized Mosquitto testbed with insecure and hardened profiles
- Makefile workflow for install, scan, test, and environment lifecycle
- Core documentation set for setup, results, screenshots, demo, and submission summary

## Partially Implemented Features

- Automated end-to-end test coverage is minimal (currently basic unit-level validation)
- TLS lab setup depends on manually provisioned certificates
- Hardening profile supports baseline policy checks but not advanced policy modeling

## Known Limitations

- Scan behavior depends on runtime broker/network availability
- Current checks focus on key misconfigurations, not comprehensive broker penetration testing
- Findings are descriptive (PASS/FAIL + message) and do not include weighted scoring

## Future Improvements

- Add richer report formats (CSV/HTML/PDF)
- Add CVSS-like severity scoring and compliance mapping
- Increase test coverage with integration tests against live broker containers
- Add CI workflow for continuous security validation
- Expand checks to include certificate quality and session-level controls
