# FLOWBOTS Desktop Client Runbook

## Overview
FLOWBOTS Desktop is the local client for executing RPA workflow conversions. It integrates with the flowbotsai.com web platform.

## Installation Verification
```powershell
# Check FLOWBOTS Desktop installation (location TBD)
# Common locations to check:
Test-Path "C:\Program Files\FLOWBOTS\*"
Test-Path "C:\Users\Administrator\AppData\Local\FLOWBOTS\*"
Test-Path "C:\FLOWBOTS\*"

# Check for FLOWBOTS processes
Get-Process -Name "*flowbots*" -ErrorAction SilentlyContinue
```

## Installation (If Missing)
1. Navigate to: https://flowbotsai.com/download (or appropriate URL)
2. Download Windows installer
3. Run installer as Administrator
4. Follow setup wizard
5. Login with FLOWBOTS credentials

## Login Credentials
- **Email:** brandon@flowbotsai.com
- **Password:** FlowBots2026

## Web App Integration
The FLOWBOTS web app at https://flowbotsai.com provides:
1. Upload source automation files
2. Select target platform
3. Run conversion
4. Download converted artifacts

## Conversion Workflow

### Via Web App
1. Navigate to https://flowbotsai.com
2. Login with credentials
3. Go to **Conversions** or **Convert** section
4. Upload source artifact (e.g., `.nupkg` for UiPath)
5. Select target platform (e.g., Power Automate Desktop)
6. Click **Convert**
7. Download converted artifact
8. Save to: `C:\flowbots_lab\artifacts_converted\<target>\<tier>\`

### Via Desktop Client (If Available)
1. Open FLOWBOTS Desktop
2. Login
3. Select **New Conversion**
4. Choose source file
5. Select target platform
6. Click **Convert**
7. Save output

## Supported Conversions

| Source | Target | Status |
|--------|--------|--------|
| UiPath (.nupkg) | Power Automate Desktop | TBD |
| Power Automate Desktop (.zip) | Automation Anywhere | TBD |
| Automation Anywhere (.zip) | Blue Prism (.bprelease) | TBD |
| UiPath | Automation Anywhere | TBD |
| Blue Prism | UiPath | TBD |

## Log Locations
- **Web App:** Browser console, network tab
- **Desktop Client:** `%AppData%\FLOWBOTS\logs\` (TBD)

## Evidence Capture

### Web Conversion
```javascript
// Browser console - capture conversion response
// Or use Playwright to automate and screenshot
```

### Desktop Conversion
```powershell
# Copy FLOWBOTS logs
Copy-Item "$env:APPDATA\FLOWBOTS\logs\*" "C:\flowbots_lab\runs\<test_id>\conversion\"
```

## Common Failure Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| "Unsupported format" | Wrong file type uploaded | Verify file format per platform |
| "Conversion failed" | Internal error | Check logs, retry, report issue |
| "Authentication failed" | Session expired | Re-login |
| "Feature not supported" | Platform limitation | Document as known limitation |

## API Endpoints (If Available)
- **Conversion API:** https://api.flowbotsai.com/convert
- **Status API:** https://api.flowbotsai.com/health

## Test Procedure

### Pre-Conversion Checklist
- [ ] Source artifact validated (runs in native platform)
- [ ] File format correct
- [ ] FLOWBOTS logged in
- [ ] Network connectivity verified

### Post-Conversion Checklist
- [ ] Conversion completed without errors
- [ ] Output file downloaded
- [ ] Output file imported into target platform
- [ ] Converted automation runs successfully

## Conversion Evidence Template
```
Test ID: FB-<TIER>-<SRC>-to-<TGT>-<NNN>
Timestamp: YYYY-MM-DD HH:MM:SS
Source Platform: <platform>
Target Platform: <platform>
Source File: <filename>
Conversion Status: PASS/FAIL
Output File: <filename>
Conversion Time: <seconds>
Notes: <any observations>
```
