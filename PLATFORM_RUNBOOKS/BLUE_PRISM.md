# Blue Prism Platform Runbook

## Overview
Blue Prism is an enterprise RPA platform. Processes and Objects are exported as `.bprelease` files.

## Installation Verification
```powershell
# Check Blue Prism installation
Test-Path "C:\Program Files\Blue Prism Limited\Blue Prism Automate\Automate.exe"

# Check Blue Prism services
Get-Service -Name "Blue Prism*" -ErrorAction SilentlyContinue
```

## License Status
- **License Expires:** 2026-07-03 (180 days from Jan 3, 2026)
- **Username:** BrandonHayman
- **Credentials:** info@thesolutionservice.com / Ewh111518!

## Launch Blue Prism
1. Run: `"C:\Program Files\Blue Prism Limited\Blue Prism Automate\Automate.exe"`
2. Connect to database (local or server)
3. Login with credentials

## Export Instructions (Source Artifact Creation)
1. Open Blue Prism
2. Navigate to **Studio** → **Processes** or **Objects**
3. Select item to export
4. Click **File** → **Export**
5. Choose **Release** format (`.bprelease`)
6. Save to: `C:\flowbots_lab\artifacts_source\blueprism\<tier>\`

## Import Instructions (Target Artifact Validation)
1. Open Blue Prism
2. Click **File** → **Import**
3. Navigate to `.bprelease` file
4. Click **Open**
5. Resolve any conflicts
6. Process/Object appears in Studio

## Run Instructions
### Via Control Room
1. Navigate to **Control** → **Control Room**
2. Add process to schedule or run immediately
3. Assign to available resource
4. Monitor execution

### Via Studio (Debug)
1. Open process in Studio
2. Click **Run** or **Step** buttons
3. Monitor execution in debug panel

## Log Locations
- **Process Logs:** Blue Prism Database (audit tables)
- **Application Logs:** `%ProgramData%\Blue Prism Limited\Automate\`
- **Event Viewer:** Application log, source "Blue Prism"

## Evidence Capture
```powershell
# Export session logs from Control Room
# Navigate to Session Logs → Filter → Export

# Copy application logs
Copy-Item "$env:ProgramData\Blue Prism Limited\Automate\*.log" "C:\flowbots_lab\runs\<test_id>\source\"
```

## Common Failure Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| "Element not found" | Application spy failed | Re-spy element in Object Studio |
| "Database connection" | SQL Server not available | Start SQL Server service |
| "License expired" | License key expired | Renew license |
| "Resource unavailable" | No free resources | Release locked resources |

## File Formats
- **Release Package:** `.bprelease` (XML-based, includes process + dependencies)
- **Process/Object:** Stored in Blue Prism database
- **Skill:** `.bpskill` (reusable component)

## Test Artifact Specs by Tier

### Simple
- **Name:** `Simple_FileOperation`
- **Actions:** Create text file with content
- **Input:** Filename, content text
- **Output:** Created file at specified path

### Moderate
- **Name:** `Moderate_DataTransform`
- **Actions:** Read CSV, transform columns, write new CSV
- **Input:** `C:\flowbots_lab\input\data.csv`
- **Output:** `C:\flowbots_lab\output\transformed.csv`

### Complex
- **Name:** `Complex_WebNavigation`
- **Actions:** Browser automation, multi-page navigation, data collection
- **Input:** URL + navigation parameters
- **Output:** Collected data in Excel

### Super Complex
- **Name:** `SuperComplex_APIIntegration`
- **Actions:** REST API calls, data mapping, error handling, retry logic
- **Input:** API endpoints + credentials
- **Output:** Integrated data + status report

### Enterprise
- **Name:** `Enterprise_MainframeIntegration`
- **Actions:** Terminal emulation, screen scraping, transaction processing
- **Input:** Mainframe connection + transaction queue
- **Output:** Processed transactions + reconciliation report

## Blue Prism Concepts
- **Process:** Top-level automation workflow
- **Object:** Reusable component (Application Model + Actions)
- **Work Queue:** Built-in queueing mechanism
- **Credential Manager:** Secure credential storage
- **Resource:** Runtime agent (robot)
