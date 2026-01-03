#!/usr/bin/env python3
"""Test FLOWBOTS API for conversion capabilities - runs on Windows Vultr"""

import requests
import json
import os
from datetime import datetime

# FLOWBOTS endpoints
API_BASE = "https://api.flowbotsai.com"
APP_URL = "https://app.flowbotsai.com"
OUTPUT_DIR = r"C:\flowbots_lab\api_tests"

def test_api():
    """Test FLOWBOTS API endpoints"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = {}

    print(f"Testing FLOWBOTS API at {datetime.now()}")
    print("=" * 60)

    # Test 1: Check API health/status
    print("\n[1] Testing API health...")
    try:
        resp = requests.get(f"{API_BASE}/health", timeout=30)
        results["health"] = {"status": resp.status_code, "response": resp.text[:500]}
        print(f"  Status: {resp.status_code}")
        print(f"  Response: {resp.text[:200]}")
    except Exception as e:
        results["health"] = {"error": str(e)}
        print(f"  Error: {e}")

    # Test 2: Check convert/platforms endpoint
    print("\n[2] Testing /convert/platforms...")
    try:
        resp = requests.get(f"{API_BASE}/convert/platforms", timeout=30)
        results["platforms"] = {"status": resp.status_code, "response": resp.text[:1000]}
        print(f"  Status: {resp.status_code}")
        if resp.status_code == 200:
            try:
                platforms = resp.json()
                print(f"  Platforms: {json.dumps(platforms, indent=2)[:500]}")
            except:
                print(f"  Response: {resp.text[:200]}")
    except Exception as e:
        results["platforms"] = {"error": str(e)}
        print(f"  Error: {e}")

    # Test 3: Check app.flowbotsai.com
    print("\n[3] Testing app.flowbotsai.com...")
    try:
        resp = requests.get(APP_URL, timeout=30)
        results["app"] = {"status": resp.status_code, "content_length": len(resp.text)}
        print(f"  Status: {resp.status_code}")
        print(f"  Content length: {len(resp.text)} bytes")
        # Check for key elements
        if "convert" in resp.text.lower():
            print("  Found 'convert' in page")
        if "upload" in resp.text.lower():
            print("  Found 'upload' in page")
        if "uipath" in resp.text.lower():
            print("  Found 'uipath' in page")
        if "power automate" in resp.text.lower():
            print("  Found 'power automate' in page")
    except Exception as e:
        results["app"] = {"error": str(e)}
        print(f"  Error: {e}")

    # Test 4: Try some alternative API endpoints
    print("\n[4] Testing alternative endpoints...")
    endpoints = [
        "/api/health",
        "/api/v1/platforms",
        "/api/convert",
        "/v1/convert",
        "/",
    ]
    for endpoint in endpoints:
        try:
            resp = requests.get(f"{API_BASE}{endpoint}", timeout=10)
            print(f"  {endpoint}: {resp.status_code}")
            results[f"endpoint_{endpoint}"] = {"status": resp.status_code}
        except Exception as e:
            print(f"  {endpoint}: Error - {e}")

    # Save results
    output_file = os.path.join(OUTPUT_DIR, f"api_test_{int(datetime.now().timestamp())}.json")
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_file}")

    return results

if __name__ == "__main__":
    test_api()
