# Automation Anywhere Platform Runbook

## Overview
Automation Anywhere is a cloud-native RPA platform. Bots are managed via Control Room and exported as `.zip` packages.

## Access Methods
1. **Control Room (Cloud):** https://community.cloud.automationanywhere.digital/#/login
2. **Bot Agent (Local):** Installed on Windows machine
3. **Desktop Bot Creator:** Local development

## Installation Verification
```powershell
# Check Bot Agent installation
Test-Path "C:\Program Files\Automation Anywhere\Bot Agent\*"
Get-Service -Name "Automation Anywhere Bot Agent" -ErrorAction SilentlyContinue

# Check if Bot Agent is running
Get-Process -Name "AABotAgent" -ErrorAction SilentlyContinue
```

## Login (Control Room)
1. Navigate to: https://community.cloud.automationanywhere.digital/#/login
2. Credentials: info@thesolutionservice.com / Ewh111518!
3. Navigate to **Bots** section

## Export Instructions (Source Artifact Creation)
### From Control Room
1. Navigate to **Automation** → **Bots**
2. Select bot(s) to export
3. Click **Actions** → **Export**
4. Download `.zip` package
5. Transfer to: `C:\flowbots_lab\artifacts_source\aa\<tier>\`

### From Local (Bot Creator)
1. Open Bot Creator
2. Right-click on bot → **Export**
3. Save to: `C:\flowbots_lab\artifacts_source\aa\<tier>\`

## Import Instructions (Target Artifact Validation)
1. Login to Control Room
2. Navigate to **Automation** → **Bots**
3. Click **Import bots** (or drag-drop)
4. Select `.zip` file
5. Resolve any dependency conflicts
6. Bot appears in library

## Run Instructions
### Via Control Room
1. Navigate to **Automation** → **Bots**
2. Select bot
3. Click **Run**
4. Choose device (registered Bot Agent)
5. Monitor execution in Activity log

### Via Bot Agent (Local)
```powershell
# Run via command line (if configured)
# Bot Agent typically runs bots deployed from Control Room
```

## Log Locations
- **Control Room:** Activity → Historical data
- **Bot Agent Logs:** `C:\ProgramData\AutomationAnywhere\Bot Agent\Logs\`
- **Bot Execution Logs:** Control Room → Audit Log

## Evidence Capture
```powershell
# Copy Bot Agent logs
Copy-Item "C:\ProgramData\AutomationAnywhere\Bot Agent\Logs\*" "C:\flowbots_lab\runs\<test_id>\source\"

# Export from Control Room: Activity → Export (CSV/PDF)
```

## Common Failure Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| "Bot Runner not available" | Device offline | Start Bot Agent service |
| "Package dependency" | Missing action package | Install required packages |
| "Credential vault" | Missing credentials | Add to Credential Vault |
| "License limit" | Concurrent license exceeded | Wait or upgrade license |

## File Formats
- **Bot Package:** `.zip` containing bot files + dependencies
- **Bot Definition:** `.atmx` (XML format) or newer JSON format
- **Logs:** Control Room audit + local agent logs

## Test Artifact Specs by Tier

### Simple
- **Name:** `SimpleCalculator`
- **Actions:** Open Calculator, perform operation, close
- **Input:** Two numbers
- **Output:** Calculation result logged

### Moderate
- **Name:** `ModeratePDFExtract`
- **Actions:** Open PDF, extract text, save to file
- **Input:** `C:\flowbots_lab\input\document.pdf`
- **Output:** `C:\flowbots_lab\output\extracted.txt`

### Complex
- **Name:** `ComplexDatabaseSync`
- **Actions:** Query database, transform data, update target system
- **Input:** Database connection + query
- **Output:** Sync report + updated records

### Super Complex
- **Name:** `SuperComplexInvoiceProcessor`
- **Actions:** Email attachment download, OCR, data validation, ERP entry
- **Input:** Email inbox config
- **Output:** Processed invoices + ERP records

### Enterprise
- **Name:** `EnterpriseClaimsWorkflow`
- **Actions:** Multi-system integration, rules engine, exception handling, SLA tracking
- **Input:** Claims queue
- **Output:** Processed claims + compliance report
