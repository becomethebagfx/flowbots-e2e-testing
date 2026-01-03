#!/usr/bin/env python3
"""FLOWBOTS Conversion API Client - runs on Windows Vultr"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# Configuration
API_BASE = "https://api.flowbotsai.com"
LAB_DIR = r"C:\flowbots_lab"
ARTIFACTS_SOURCE = os.path.join(LAB_DIR, "artifacts_source")
ARTIFACTS_CONVERTED = os.path.join(LAB_DIR, "artifacts_converted")
RUNS_DIR = os.path.join(LAB_DIR, "runs")
LOGS_DIR = os.path.join(LAB_DIR, "logs")

# Platform mappings (from OpenAPI spec)
SOURCE_PLATFORMS = ["uipath", "automationAnywhere", "powerAutomate", "bluePrism", "flowbots"]
TARGET_PLATFORMS = ["flowbots", "automationAnywhere", "powerAutomate", "powerAutomateCloud", "uipath"]

# Map directory names to API platform names
DIR_TO_API = {
    "uipath": "uipath",
    "pad": "powerAutomate",
    "pacloud": "powerAutomateCloud",
    "blueprism": "bluePrism",
    "aa": "automationAnywhere",
}

API_TO_DIR = {v: k for k, v in DIR_TO_API.items()}


class FlowBotsClient:
    """Client for FLOWBOTS Conversion API"""

    def __init__(self, api_key: str = None):
        self.base_url = API_BASE
        self.api_key = api_key or os.environ.get("FLOWBOTS_API_KEY", "")
        self.session = requests.Session()
        if self.api_key:
            self.session.headers["X-API-Key"] = self.api_key

    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        resp = self.session.get(f"{self.base_url}/health", timeout=30)
        return resp.json()

    def convert(
        self,
        file_path: str,
        source_platform: str,
        target_platform: str,
        generate_api: bool = False,
        generate_docker: bool = False,
        generate_documentation: bool = True,
        use_agent: bool = False,
    ) -> Dict[str, Any]:
        """
        Start a conversion job.

        Returns: {"jobId": "...", "status": "pending", "statusUrl": "...", "filesUrl": "..."}
        """
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            data = {
                "sourcePlatform": source_platform,
                "targetPlatform": target_platform,
                "generateApi": str(generate_api).lower(),
                "generateDocker": str(generate_docker).lower(),
                "generateDocumentation": str(generate_documentation).lower(),
                "useAgent": str(use_agent).lower(),
            }

            resp = self.session.post(
                f"{self.base_url}/api/v1/convert",
                files=files,
                data=data,
                timeout=120,
            )

        if resp.status_code == 202:
            return resp.json()
        else:
            return {"error": f"HTTP {resp.status_code}", "message": resp.text[:500]}

    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get job status"""
        resp = self.session.get(f"{self.base_url}/api/v1/jobs/{job_id}", timeout=30)
        return resp.json()

    def wait_for_job(self, job_id: str, timeout: int = 300, poll_interval: int = 5) -> Dict[str, Any]:
        """Wait for job to complete"""
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_job_status(job_id)
            job_status = status.get("status", "unknown")

            if job_status in ["completed", "failed"]:
                return status

            time.sleep(poll_interval)

        return {"error": "timeout", "message": f"Job did not complete within {timeout}s"}

    def get_converted_files(self, job_id: str, output_dir: str) -> str:
        """Download converted files as ZIP"""
        resp = self.session.get(
            f"{self.base_url}/api/v1/jobs/{job_id}/files",
            params={"format": "zip"},
            timeout=120,
        )

        if resp.status_code == 200:
            os.makedirs(output_dir, exist_ok=True)
            zip_path = os.path.join(output_dir, f"{job_id}.zip")
            with open(zip_path, "wb") as f:
                f.write(resp.content)
            return zip_path
        else:
            return None

    def assess(self, file_path: str, source_platform: str, target_platform: str) -> Dict[str, Any]:
        """Assess workflow for migration"""
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            data = {
                "sourcePlatform": source_platform,
                "targetPlatform": target_platform,
                "includeEstimation": "true",
                "includeSecurityScan": "true",
                "includeStatistics": "true",
            }

            resp = self.session.post(
                f"{self.base_url}/api/v1/assess",
                files=files,
                data=data,
                timeout=120,
            )

        return resp.json()


def run_conversion_test(
    client: FlowBotsClient,
    source_file: str,
    source_platform: str,
    target_platform: str,
    test_id: str,
) -> Dict[str, Any]:
    """Run a single conversion test"""
    result = {
        "test_id": test_id,
        "source_platform": source_platform,
        "target_platform": target_platform,
        "source_file": source_file,
        "timestamp": datetime.now().isoformat(),
        "status": "pending",
    }

    try:
        # Start conversion
        print(f"    Starting conversion: {source_platform} -> {target_platform}")
        conv_result = client.convert(source_file, source_platform, target_platform)

        if "error" in conv_result:
            result["status"] = "error"
            result["error"] = conv_result.get("message", conv_result.get("error"))
            return result

        job_id = conv_result.get("jobId")
        if not job_id:
            result["status"] = "error"
            result["error"] = "No job ID returned"
            return result

        result["job_id"] = job_id
        print(f"    Job ID: {job_id}")

        # Wait for completion
        job_status = client.wait_for_job(job_id, timeout=300)
        result["job_status"] = job_status

        if job_status.get("status") == "completed":
            result["status"] = "success"

            # Download converted files
            output_dir = os.path.join(
                ARTIFACTS_CONVERTED,
                target_platform,
                "simple",
                test_id,
            )
            zip_path = client.get_converted_files(job_id, output_dir)
            if zip_path:
                result["output_file"] = zip_path

        elif job_status.get("status") == "failed":
            result["status"] = "failed"
            result["error"] = job_status.get("error", "Unknown error")
        else:
            result["status"] = "timeout"

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def main():
    """Main entry point"""
    print("=" * 60)
    print("FLOWBOTS Conversion API Test Runner")
    print("=" * 60)

    # Create client
    client = FlowBotsClient()

    # Health check
    print("\nChecking API health...")
    try:
        health = client.health_check()
        print(f"  API Status: {health.get('status', 'unknown')}")
    except Exception as e:
        print(f"  Error: {e}")
        return

    # List available artifacts
    print("\nAvailable artifacts:")
    for platform_dir, api_name in DIR_TO_API.items():
        tier_dir = os.path.join(ARTIFACTS_SOURCE, platform_dir, "simple")
        if os.path.exists(tier_dir):
            count = len([f for f in os.listdir(tier_dir) if os.path.isfile(os.path.join(tier_dir, f))])
            if count > 0:
                print(f"  {platform_dir} ({api_name}): {count} artifacts")

    # Run test conversions
    print("\n" + "=" * 60)
    print("Running test conversions (first 3 per direction)...")

    results = []

    # Test UiPath -> FlowBots (Node.js)
    uipath_dir = os.path.join(ARTIFACTS_SOURCE, "uipath", "simple")
    if os.path.exists(uipath_dir):
        print(f"\nTesting UiPath -> FlowBots:")
        artifacts = sorted([f for f in os.listdir(uipath_dir) if f.endswith(".nupkg")])[:3]

        for artifact in artifacts:
            artifact_path = os.path.join(uipath_dir, artifact)
            test_id = artifact.replace(".nupkg", "")
            print(f"  [{test_id}]")

            result = run_conversion_test(
                client,
                artifact_path,
                "uipath",
                "flowbots",
                test_id,
            )
            results.append(result)
            print(f"    Result: {result['status']}")

    # Test PAD -> UiPath
    pad_dir = os.path.join(ARTIFACTS_SOURCE, "pad", "simple")
    if os.path.exists(pad_dir):
        print(f"\nTesting PAD -> UiPath:")
        artifacts = sorted([f for f in os.listdir(pad_dir) if f.endswith(".zip")])[:3]

        for artifact in artifacts:
            artifact_path = os.path.join(pad_dir, artifact)
            test_id = artifact.replace(".zip", "")
            print(f"  [{test_id}]")

            result = run_conversion_test(
                client,
                artifact_path,
                "powerAutomate",
                "uipath",
                test_id,
            )
            results.append(result)
            print(f"    Result: {result['status']}")

    # Save results
    os.makedirs(LOGS_DIR, exist_ok=True)
    results_file = os.path.join(LOGS_DIR, f"conversion_results_{int(time.time())}.json")
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n" + "=" * 60)
    print(f"Results saved to: {results_file}")

    # Summary
    statuses = {}
    for r in results:
        s = r["status"]
        statuses[s] = statuses.get(s, 0) + 1

    print("\nSummary:")
    for status, count in statuses.items():
        print(f"  {status}: {count}")


if __name__ == "__main__":
    main()
