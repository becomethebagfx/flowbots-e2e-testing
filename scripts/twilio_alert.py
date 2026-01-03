#!/usr/bin/env python3
"""Twilio SMS alert helper for FLOWBOTS E2E testing"""

import os
from twilio.rest import Client

# Twilio credentials from environment variables
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER", "+18666209504")
TO_NUMBER = os.environ.get("TWILIO_TO_NUMBER", "+12055328682")

def send_alert(message: str, priority: str = "INFO"):
    """Send SMS alert via Twilio

    Args:
        message: Alert message text
        priority: INFO, MEDIUM, HIGH, or CRITICAL
    """
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        # Always send HIGH and CRITICAL alerts
        # For lower priority, could add filtering logic
        if priority in ["HIGH", "CRITICAL", "INFO", "MEDIUM"]:
            client.messages.create(
                body=f"[{priority}] FLOWBOTS: {message}",
                from_=FROM_NUMBER,
                to=TO_NUMBER
            )
            print(f"Alert sent: [{priority}] {message}")
            return True
    except Exception as e:
        print(f"Failed to send alert: {e}")
        return False

def send_test_result(tier: str, passed: int, total: int):
    """Send test batch completion alert"""
    percent = round(passed / total * 100, 1) if total > 0 else 0
    message = f"{tier} tier complete: {passed}/{total} passed ({percent}%)"
    priority = "INFO" if percent >= 85 else "MEDIUM" if percent >= 70 else "HIGH"
    return send_alert(message, priority)

def send_resource_alert(cpu: float, mem: float, disk: float):
    """Send resource threshold alert"""
    alerts = []
    if cpu > 85:
        alerts.append(f"CPU at {cpu}%")
    if mem > 90:
        alerts.append(f"Memory at {mem}%")
    if disk < 10:
        alerts.append(f"Disk only {disk}GB free")

    if alerts:
        message = "Resource critical: " + ", ".join(alerts)
        return send_alert(message, "HIGH")
    return False

def send_failure_alert(test_id: str, error: str):
    """Send test failure alert"""
    message = f"Test {test_id} failed: {error[:100]}"
    return send_alert(message, "MEDIUM")

def send_recovery_alert():
    """Send recovery started alert"""
    return send_alert("Recovery started - resuming from last checkpoint", "INFO")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        msg = " ".join(sys.argv[1:])
        send_alert(msg, "INFO")
    else:
        print("Usage: python twilio_alert.py <message>")
