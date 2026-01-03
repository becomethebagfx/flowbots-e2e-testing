# FLOWBOTS E2E - ISSUES REGISTER

## Issue Format
```
### ISSUE-NNN: <Title>
- **Test ID:** FB-XXX-XXX-XXX-NNN
- **Tier:** Simple/Moderate/Complex/Super Complex/Enterprise
- **Conversion:** Source → Target
- **Status:** OPEN / IN_PROGRESS / RESOLVED / BLOCKED
- **Severity:** Critical / High / Medium / Low
- **Failure Signature:** <error message or behavior>
- **Repro Steps:** <numbered steps>
- **Logs:** <path to logs>
- **Hypothesis:** <root cause guess>
- **Fix Plan:** <proposed solution>
- **Resolution:** <what was done>
- **Resolved Date:** <date or N/A>
```

---

## Open Issues

### ISSUE-001: SSH to Windows Vultr Fails
- **Test ID:** SETUP-001
- **Tier:** N/A (Infrastructure)
- **Conversion:** N/A
- **Status:** IN_PROGRESS
- **Severity:** Critical
- **Failure Signature:** `Permission denied (publickey,password,keyboard-interactive)`
- **Repro Steps:**
  1. Run `ssh Administrator@45.63.68.224`
  2. Enter password when prompted
  3. Connection rejected
- **Logs:** N/A
- **Hypothesis:** Password has special characters `}b3MaiC+rL))2N4n` that may need escaping, or OpenSSH server not configured for password auth
- **Fix Plan:**
  1. Try sshpass with escaped password
  2. Try PowerShell remoting
  3. Fall back to RDP + Peekaboo agent
  4. If all fail, TEXT user for manual OpenSSH config
- **Resolution:** TBD
- **Resolved Date:** N/A

---

## Resolved Issues
(none yet)

---

## Blocked Issues
(none yet)
