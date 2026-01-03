# UiPath Platform Runbook

## Overview
UiPath is an enterprise RPA platform. Projects are exported as `.nupkg` packages.

## Installation Verification
```powershell
# Check UiPath installation
Test-Path "C:\Program Files\UiPath\Studio\UiPath.Studio.exe"
Test-Path "C:\Program Files\UiPath\Robot\UiPath.Robot.exe"

# Check UiPath Assistant
Get-Process -Name "UiPath.Assistant" -ErrorAction SilentlyContinue
```

## Export Instructions (Source Artifact Creation)
1. Open UiPath Studio
2. Open project to export
3. Go to **Design** ribbon → **Publish**
4. Select **Custom** target
5. Choose local folder: `C:\flowbots_lab\artifacts_source\uipath\<tier>\`
6. Click **Publish**
7. Output: `<ProjectName>.<version>.nupkg`

## Import Instructions (Target Artifact Validation)
1. Open UiPath Assistant
2. Click **Add Process** (+ icon)
3. Navigate to `.nupkg` file
4. Click **Install**
5. Process appears in Assistant list

## Run Instructions
### Via UiPath Assistant (GUI)
1. Open UiPath Assistant
2. Find process in list
3. Click **Play** button
4. Monitor execution in Output panel

### Via Command Line
```powershell
# Run process via Robot
& "C:\Program Files\UiPath\Robot\UiPath.Robot.exe" execute --process "<ProcessName>" --input "{'arg1':'value1'}"
```

## Log Locations
- **Studio Logs:** `%LocalAppData%\UiPath\Logs\`
- **Robot Logs:** `%LocalAppData%\UiPath\Logs\<date>_Execution.log`
- **Project Output:** Configured in project settings

## Evidence Capture
```powershell
# Copy execution logs
$date = Get-Date -Format "yyyyMMdd"
Copy-Item "$env:LOCALAPPDATA\UiPath\Logs\${date}_Execution.log" "C:\flowbots_lab\runs\<test_id>\source\"

# Screenshot (requires automation)
# Use Windows Snipping Tool or PowerShell screenshot script
```

## Common Failure Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| "Package not found" | .nupkg not in feed | Manually install via Assistant |
| "Selector not found" | UI element changed | Update selectors in Studio |
| "License required" | Robot not licensed | Activate via Orchestrator or local license |
| "Activity not installed" | Missing dependency | Install activity package in Studio |

## File Formats
- **Project Source:** `.xaml` files + `project.json`
- **Published Package:** `.nupkg` (NuGet format)
- **Logs:** `.log` (text format)

## Test Artifact Specs by Tier

### Simple
- **Name:** `SimpleFileCreate`
- **Actions:** Create text file with timestamp
- **Input:** None
- **Output:** `C:\flowbots_lab\output\simple_output.txt`

### Moderate
- **Name:** `ModerateFileCopy`
- **Actions:** Read file, transform content, write new file
- **Input:** `C:\flowbots_lab\input\source.txt`
- **Output:** `C:\flowbots_lab\output\transformed.txt`

### Complex
- **Name:** `ComplexWebScrape`
- **Actions:** Open browser, navigate, extract data, save to Excel
- **Input:** URL parameter
- **Output:** `C:\flowbots_lab\output\scraped_data.xlsx`

### Super Complex
- **Name:** `SuperComplexDataPipeline`
- **Actions:** API call, database query, file processing, email notification
- **Input:** Config file + API credentials
- **Output:** Multiple files + email sent

### Enterprise
- **Name:** `EnterpriseOrderProcessor`
- **Actions:** ERP integration, multi-system sync, audit logging, error handling
- **Input:** Order queue
- **Output:** Processed orders + audit trail
