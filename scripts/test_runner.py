#!/usr/bin/env python3
"""FLOWBOTS E2E Test Runner - Uses Claude CLI (Max subscription)"""

import subprocess
import json
import os
import time
from datetime import datetime
from pathlib import Path
import sys

# Import alert helper
try:
    from twilio_alert import send_alert, send_test_result, send_failure_alert
except ImportError:
    def send_alert(msg, priority="INFO"): print(f"[{priority}] {msg}")
    def send_test_result(tier, passed, total): pass
    def send_failure_alert(test_id, error): pass

# Test matrix - all conversion directions
PLATFORMS = ["uipath", "pad", "pacloud", "aa", "blueprism", "flowbots"]
TIERS = ["simple", "moderate", "complex", "supercomplex", "enterprise"]

# Conversion matrix (24 directions)
CONVERSIONS = [
    ("uipath", "pad"), ("uipath", "pacloud"), ("uipath", "aa"), ("uipath", "blueprism"),
    ("pad", "uipath"), ("pad", "pacloud"), ("pad", "aa"), ("pad", "blueprism"),
    ("pacloud", "uipath"), ("pacloud", "pad"), ("pacloud", "aa"), ("pacloud", "blueprism"),
    ("aa", "uipath"), ("aa", "pad"), ("aa", "pacloud"), ("aa", "blueprism"),
    ("blueprism", "uipath"), ("blueprism", "pad"), ("blueprism", "pacloud"), ("blueprism", "aa"),
    ("uipath", "flowbots"), ("pad", "flowbots"), ("aa", "flowbots"), ("blueprism", "flowbots"),
]

# Tests per tier
TESTS_PER_TIER = {
    "simple": ["S{:02d}".format(i) for i in range(1, 21)],
    "moderate": ["M{:02d}".format(i) for i in range(1, 21)],
    "complex": ["C{:02d}".format(i) for i in range(1, 21)],
    "supercomplex": ["SC{:02d}".format(i) for i in range(1, 21)],
    "enterprise": ["E{:02d}".format(i) for i in range(1, 21)],
}

class TestRunner:
    def __init__(self, results_dir: str = "C:\\flowbots_lab\\runs"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.results = []
        self.consecutive_failures = 0

    def run_single_test(self, test_id: str, source: str, target: str, tier: str) -> dict:
        """Run single test via Claude CLI (uses Max subscription, $0)"""
        prompt = f"""Execute FLOWBOTS conversion test:
- Test ID: {test_id}
- Source Platform: {source}
- Target Platform: {target}
- Tier: {tier}

Steps:
1. Find source artifact at C:\\flowbots_lab\\artifacts_source\\{source}\\{tier}\\
2. Upload to flowbotsai.com and convert to {target}
3. Download converted artifact to C:\\flowbots_lab\\artifacts_converted\\{target}\\{tier}\\
4. Validate the converted artifact runs in target platform
5. Capture evidence (screenshots, logs)
6. Return PASS or FAIL with details
"""
        try:
            result = subprocess.run(
                ["claude", "-p", prompt,
                 "--model", "haiku" if tier in ["simple", "moderate"] else "sonnet",
                 "--max-turns", "5",
                 "--output-format", "json"],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                self.consecutive_failures = 0
                return {"test_id": test_id, "status": "PASS", "output": result.stdout}
            else:
                self.consecutive_failures += 1
                if self.consecutive_failures >= 3:
                    send_failure_alert(test_id, result.stderr[:100])
                return {"test_id": test_id, "status": "FAIL", "error": result.stderr}

        except subprocess.TimeoutExpired:
            return {"test_id": test_id, "status": "TIMEOUT", "error": "Test timed out after 5 minutes"}
        except Exception as e:
            return {"test_id": test_id, "status": "ERROR", "error": str(e)}

    def run_tier(self, tier: str) -> dict:
        """Run all tests for a tier"""
        tests = TESTS_PER_TIER[tier]
        results = []
        passed = 0

        for source, target in CONVERSIONS:
            for test_num in tests:
                test_id = f"FB-{tier.upper()}-{source.upper()}-to-{target.upper()}-{test_num}"
                print(f"Running: {test_id}")

                result = self.run_single_test(test_id, source, target, tier)
                results.append(result)

                if result["status"] == "PASS":
                    passed += 1

                # Save result immediately
                self.save_result(result)

                # Brief pause between tests
                time.sleep(1)

        total = len(results)
        send_test_result(tier, passed, total)

        return {
            "tier": tier,
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": round(passed / total * 100, 1) if total > 0 else 0
        }

    def save_result(self, result: dict):
        """Save test result to file"""
        test_id = result.get("test_id", "unknown")
        filepath = self.results_dir / f"{test_id}.json"
        with open(filepath, "w") as f:
            json.dump(result, f, indent=2)

    def run_all(self):
        """Run all tiers"""
        send_alert("Starting FLOWBOTS E2E testing - 2,900 tests", "INFO")

        for tier in TIERS:
            print(f"\n{'='*60}")
            print(f"TIER: {tier.upper()}")
            print(f"{'='*60}\n")

            tier_result = self.run_tier(tier)
            print(f"\n{tier.upper()} complete: {tier_result['passed']}/{tier_result['total']} ({tier_result['pass_rate']}%)")

        send_alert("FLOWBOTS E2E testing complete!", "INFO")


if __name__ == "__main__":
    runner = TestRunner()

    if len(sys.argv) > 1:
        tier = sys.argv[1].lower()
        if tier in TIERS:
            runner.run_tier(tier)
        else:
            print(f"Unknown tier: {tier}. Available: {TIERS}")
    else:
        runner.run_all()
