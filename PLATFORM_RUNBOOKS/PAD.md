# Power Automate Desktop (PAD) Platform Runbook

## Overview
Power Automate Desktop is Microsoft's free RPA tool. Flows are exported as `.zip` files containing `.pad` flow definitions.

## Installation Verification
```powershell
# Check PAD installation
Test-Path "C:\Program Files (x86)\Power Automate Desktop\PAD.Console.Host.exe"

# Check if PAD is running
Get-Process -Name "PAD.Console.Host" -ErrorAction SilentlyContinue
```

## Export Instructions (Source Artifact Creation)
1. Open Power Automate Desktop
2. Right-click on flow to export
3. Select **Export**
4. Save to: `C:\flowbots_lab\artifacts_source\pad\<tier>\`
5. Output: `<FlowName>.zip` containing `.pad` file

## Import Instructions (Target Artifact Validation)
1. Open Power Automate Desktop
2. Click **Import** button (top toolbar)
3. Navigate to `.zip` file
4. Click **Open**
5. Flow appears in flow list

## Run Instructions
### Via GUI
1. Open Power Automate Desktop
2. Find flow in list
3. Double-click to open designer OR click **Run** button
4. Monitor execution in Run panel

### Via Command Line
```powershell
# Run flow via PAD CLI (if available)
& "C:\Program Files (x86)\Power Automate Desktop\PAD.Console.Host.exe" /run "<FlowName>"
```

## Log Locations
- **Application Logs:** `%LocalAppData%\Microsoft\Power Automate Desktop\Logs\`
- **Flow Run History:** Available in PAD UI under flow details
- **Windows Event Log:** Application log, source "Power Automate Desktop"

## Evidence Capture
```powershell
# Copy PAD logs
Copy-Item "$env:LOCALAPPDATA\Microsoft\Power Automate Desktop\Logs\*" "C:\flowbots_lab\runs\<test_id>\source\"

# Export run history (manual - screenshot or screen recording recommended)
```

## Common Failure Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| "Flow not found" | Import failed | Re-import flow |
| "Action failed" | UI element not found | Update selectors in designer |
| "Sign-in required" | Microsoft account needed | Sign in with M365 account |
| "Premium action" | Requires paid license | Use alternative actions or license |

## File Formats
- **Flow Definition:** `.pad` (JSON-like format)
- **Export Package:** `.zip` containing `.pad` + metadata
- **Logs:** `.log` files in Logs folder

## Test Artifact Specs by Tier

### Simple
- **Name:** `SimpleMessageBox`
- **Actions:** Display message box with timestamp
- **Input:** None
- **Output:** Message box displayed

### Moderate
- **Name:** `ModerateFileProcessor`
- **Actions:** Read file, parse content, write transformed output
- **Input:** `C:\flowbots_lab\input\data.txt`
- **Output:** `C:\flowbots_lab\output\processed.txt`

### Complex
- **Name:** `ComplexExcelReport`
- **Actions:** Open Excel, read data, apply formulas, generate chart, save
- **Input:** `C:\flowbots_lab\input\sales.xlsx`
- **Output:** `C:\flowbots_lab\output\report.xlsx`

### Super Complex
- **Name:** `SuperComplexWebAutomation`
- **Actions:** Browser automation, form filling, data extraction, error handling
- **Input:** URL + credentials config
- **Output:** Extracted data + screenshots

### Enterprise
- **Name:** `EnterpriseDocumentWorkflow`
- **Actions:** SharePoint integration, document processing, approval workflow, notifications
- **Input:** Document library + workflow config
- **Output:** Processed documents + audit log
