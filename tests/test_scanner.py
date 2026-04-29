"""Basic tests for BrokerGuard scanner model behavior."""

import unittest

from brokerguard.scanner import BrokerScanner, CheckResult


class ScannerSerializationTests(unittest.TestCase):
    def test_json_output_shape(self) -> None:
        results = [CheckResult(name="X", status="PASS", message="ok")]
        payload = BrokerScanner.to_json(results)
        self.assertIn('"name": "X"', payload)
        self.assertIn('"status": "PASS"', payload)


if __name__ == "__main__":
    unittest.main()
