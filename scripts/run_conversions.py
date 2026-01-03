#!/usr/bin/env python3
"""FLOWBOTS E2E Conversion Test Runner - runs on Windows Vultr"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path

# Configuration
API_BASE = "https://api.flowbotsai.com"
APP_URL = "https://app.flowbotsai.com"
LAB_DIR = r"C:\flowbots_lab"
ARTIFACTS_SOURCE = os.path.join(LAB_DIR, "artifacts_source")
ARTIFACTS_CONVERTED = os.path.join(LAB_DIR, "artifacts_converted")
RUNS_DIR = os.path.join(LAB_DIR, "runs")
LOGS_DIR = os.path.join(LAB_DIR, "logs")

# Platform mapping
PLATFORMS = {
    "uipath": {"name": "UiPath", "ext": ".nupkg"},
    "pad": {"name": "Power Automate Desktop", "ext": ".zip"},
    "pacloud": {"name": "Power Automate Cloud", "ext": ".json"},
    "blueprism": {"name": "Blue Prism", "ext": ".bprelease"},
    "aa": {"name": "Automation Anywhere", "ext": ".zip"},
}

# Conversion matrix (24 directions)
CONVERSION_MATRIX = [
    ("uipath", "pad"), ("uipath", "pacloud"), ("uipath", "aa"), ("uipath", "blueprism"),
    ("pad", "uipath"), ("pad", "pacloud"), ("pad", "aa"), ("pad", "blueprism"),
    ("pacloud", "uipath"), ("pacloud", "pad"), ("pacloud", "aa"), ("pacloud", "blueprism"),
    ("aa", "uipath"), ("aa", "pad"), ("aa", "pacloud"), ("aa", "blueprism"),
    ("blueprism", "uipath"), ("blueprism", "pad"), ("blueprism", "pacloud"), ("blueprism", "aa"),
    # Plus FlowBots target
    ("uipath", "flowbots"), ("pad", "flowbots"), ("aa", "flowbots"), ("blueprism", "flowbots"),
]

# Simple tier tests
SIMPLE_TESTS = [f"S{i:02d}" for i in range(1, 21)]


def log(msg):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")


def ensure_dirs():
    """Create necessary directories"""
    for d in [ARTIFACTS_CONVERTED, RUNS_DIR, LOGS_DIR]:
        os.makedirs(d, exist_ok=True)


def find_artifact(source_platform, tier, test_id):
    """Find source artifact file"""
    tier_dir = os.path.join(ARTIFACTS_SOURCE, source_platform, tier.lower())
    if not os.path.exists(tier_dir):
        return None

    # Look for matching file
    for f in os.listdir(tier_dir):
        if test_id.lower() in f.lower() or f"Simple_{test_id}" in f:
            return os.path.join(tier_dir, f)

    # Try pattern matching
    for f in os.listdir(tier_dir):
        if f.endswith(PLATFORMS.get(source_platform, {}).get("ext", ".zip")):
            # Get test number from filename
            parts = f.replace(".zip", "").replace(".nupkg", "").replace(".bprelease", "").split("_")
            for part in parts:
                if part.upper() == test_id.upper():
                    return os.path.join(tier_dir, f)

    return None


def convert_artifact(source_file, source_platform, target_platform, test_id):
    """
    Convert an artifact using FLOWBOTS API.

    This is a placeholder for the actual conversion API call.
    The actual implementation will depend on the FLOWBOTS API structure.
    """
    result = {
        "test_id": test_id,
        "source_platform": source_platform,
        "target_platform": target_platform,
        "source_file": source_file,
        "timestamp": datetime.now().isoformat(),
        "status": "pending"
    }

    try:
        # Read source file
        with open(source_file, "rb") as f:
            file_content = f.read()

        # Try to find the correct API endpoint
        # Common patterns for conversion APIs:
        endpoints_to_try = [
            f"{API_BASE}/convert",
            f"{API_BASE}/api/convert",
            f"{API_BASE}/api/v1/convert",
            f"{API_BASE}/workflow/convert",
        ]

        for endpoint in endpoints_to_try:
            try:
                # Attempt multipart form upload
                files = {
                    "file": (os.path.basename(source_file), file_content),
                }
                data = {
                    "source": source_platform,
                    "target": target_platform,
                }

                resp = requests.post(endpoint, files=files, data=data, timeout=60)

                if resp.status_code == 200:
                    result["status"] = "success"
                    result["endpoint"] = endpoint
                    result["response"] = resp.text[:500]
                    break
                elif resp.status_code == 404:
                    continue
                else:
                    result["status"] = "error"
                    result["error"] = f"HTTP {resp.status_code}: {resp.text[:200]}"
                    break

            except requests.exceptions.Timeout:
                result["status"] = "timeout"
                result["error"] = "Request timed out"
            except Exception as e:
                result["status"] = "error"
                result["error"] = str(e)

        # If no endpoint worked, mark as needs_investigation
        if result["status"] == "pending":
            result["status"] = "needs_api_discovery"
            result["note"] = "Need to discover correct API endpoint structure"

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def run_simple_tier():
    """Run all Simple tier tests"""
    log("Starting Simple tier tests")
    results = []

    ensure_dirs()

    # For each conversion direction
    for source, target in CONVERSION_MATRIX:
        # Skip if source artifacts don't exist
        source_dir = os.path.join(ARTIFACTS_SOURCE, source, "simple")
        if not os.path.exists(source_dir):
            log(f"  Skipping {source} -> {target}: no source artifacts")
            continue

        log(f"\n  Testing {source.upper()} -> {target.upper()}")

        # Find and list available artifacts
        artifacts = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
        log(f"    Found {len(artifacts)} artifacts")

        # Test each artifact
        for artifact_file in artifacts[:5]:  # Limit to first 5 for initial run
            artifact_path = os.path.join(source_dir, artifact_file)
            test_id = artifact_file.split(".")[0]

            log(f"    Testing: {test_id}")

            result = convert_artifact(artifact_path, source, target, test_id)
            results.append(result)

            log(f"      Status: {result['status']}")

    # Save results
    results_file = os.path.join(LOGS_DIR, f"simple_tier_results_{int(time.time())}.json")
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)

    log(f"\nResults saved to: {results_file}")

    # Summary
    statuses = {}
    for r in results:
        s = r["status"]
        statuses[s] = statuses.get(s, 0) + 1

    log("\nSummary:")
    for status, count in statuses.items():
        log(f"  {status}: {count}")

    return results


def main():
    """Main entry point"""
    log("=" * 60)
    log("FLOWBOTS E2E Conversion Test Runner")
    log("=" * 60)

    # Check available artifacts
    log("\nChecking available artifacts:")
    for platform in PLATFORMS:
        for tier in ["simple", "moderate", "complex", "supercomplex", "enterprise"]:
            tier_dir = os.path.join(ARTIFACTS_SOURCE, platform, tier)
            if os.path.exists(tier_dir):
                count = len([f for f in os.listdir(tier_dir) if os.path.isfile(os.path.join(tier_dir, f))])
                if count > 0:
                    log(f"  {platform}/{tier}: {count} artifacts")

    # Run Simple tier
    log("\n" + "=" * 60)
    results = run_simple_tier()

    log("\n" + "=" * 60)
    log("Test run complete")

    return results


if __name__ == "__main__":
    main()
