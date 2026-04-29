# Screenshot Checklist for Report Submission

Capture these screenshots exactly for a complete academic submission.

1. **Project root tree**
   - Show `brokerguard/`, `docker/`, `docs/`, `examples/`, `Makefile`, and `README.md`.

2. **Insecure Docker profile running**
   - Command: `make up-insecure`
   - Show container running in `docker compose ps` output.

3. **Insecure scan results**
   - Command: `make scan`
   - Show multiple `FAIL` entries and `HIGH` risk level.

4. **Hardened Docker profile running**
   - Command: `make up-hardened`
   - Show container state and configured secure profile.

5. **Hardened scan results (text)**
   - Command: `make scan`
   - Show mostly/all `PASS` entries and `LOW` risk level.

6. **Hardened scan results (JSON)**
   - Command: `make scan-json`
   - Show structured JSON with target, summary, and results.

7. **Test execution**
   - Command: `make test`
   - Show successful test run.

8. **README sections visible**
   - Show overview, architecture, scanner checks, and limitations/future work.
