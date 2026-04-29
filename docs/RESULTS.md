# Expected Results

Use this page in your report to compare insecure and hardened runs.

## Insecure Profile (Expected)

With `make up-insecure`, the broker is intentionally weak:

- Anonymous access is allowed
- Invalid credentials may be accepted or not required
- TLS is not enforced
- ACL restrictions are missing
- Unauthorized publish may be accepted

Typical outcome: multiple `FAIL` results and **HIGH** overall risk.

## Hardened Profile (Expected)

With `make up-hardened`, the broker should enforce:

- No anonymous access
- Invalid credential rejection
- TLS listener on `8883`
- Plaintext listener disabled
- ACL deny rules for `admin/#` and `actuators/#`

Typical outcome: mostly/all `PASS` results and **LOW** overall risk.

## Risk Level Interpretation

- **HIGH**: 3 or more failed checks
- **MEDIUM**: 1-2 failed checks
- **LOW**: 0 failed checks

## Notes for Grading / Demonstration

- Show both insecure and hardened scans.
- Explain at least one failed check and how hardening fixed it.
- Include terminal screenshots plus saved outputs from `examples/`.

## Demo Mode (No Docker Environments)

If Docker is unavailable, run:

```bash
python brokerguard.py --demo
python brokerguard.py --demo --json
```

Behavior:

- Output is clearly labeled as `DEMO MODE – SIMULATED RESULTS`.
- The insecure simulation returns mostly `FAIL` with `HIGH` risk.
- The hardened simulation returns mostly `PASS` with `LOW` risk.
- JSON mode includes both simulated profiles in one payload for reporting.
