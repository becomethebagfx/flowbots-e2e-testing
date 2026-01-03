# FLOWBOTS E2E TEST MATRIX

## Test ID Format
`FB-<TIER>-<SRC>-to-<TGT>-<NNN>`

Example: `FB-SIMPLE-UIPATH-to-PAD-001`

## Tier Definitions

### SIMPLE
- **Inputs:** Single file or hardcoded value
- **Steps:** 1-3 sequential actions (open app, click, type)
- **Outputs:** Single file or message box
- **Runtime:** < 30 seconds

### MODERATE
- **Inputs:** File + user input OR multiple files
- **Steps:** 4-8 actions with basic conditionals (if/else)
- **Outputs:** Multiple files or formatted report
- **Runtime:** 30s - 2min

### COMPLEX
- **Inputs:** Multiple sources (file, web, database)
- **Steps:** 10-20 actions with loops, error handling
- **Outputs:** Multi-file output with validation
- **Runtime:** 2-5 min

### SUPER COMPLEX
- **Inputs:** API + file + database + UI interaction
- **Steps:** 20-50 actions with nested loops, exception handling, retry logic
- **Outputs:** Complex report, multiple destinations, audit trail
- **Runtime:** 5-15 min

### ENTERPRISE
- **Inputs:** Multiple systems integration (ERP, CRM, legacy)
- **Steps:** 50+ actions with orchestration, sub-workflows, queues
- **Outputs:** Full audit, compliance logging, multi-system sync
- **Runtime:** 15+ min, may be scheduled/batched

---

## Test Cases

### UiPath → Power Automate Desktop

| Test ID | Tier | Source Artifact | Status | Source Valid | Converted | Target Valid | Evidence |
|---------|------|-----------------|--------|--------------|-----------|--------------|----------|
| FB-SIMPLE-UIPATH-to-PAD-001 | Simple | TBD | PENDING | - | - | - | - |
| FB-MODERATE-UIPATH-to-PAD-001 | Moderate | TBD | PENDING | - | - | - | - |
| FB-COMPLEX-UIPATH-to-PAD-001 | Complex | TBD | PENDING | - | - | - | - |
| FB-SUPERCOMPLEX-UIPATH-to-PAD-001 | Super Complex | TBD | PENDING | - | - | - | - |
| FB-ENTERPRISE-UIPATH-to-PAD-001 | Enterprise | TBD | PENDING | - | - | - | - |

### Power Automate Desktop → Automation Anywhere

| Test ID | Tier | Source Artifact | Status | Source Valid | Converted | Target Valid | Evidence |
|---------|------|-----------------|--------|--------------|-----------|--------------|----------|
| FB-SIMPLE-PAD-to-AA-001 | Simple | TBD | PENDING | - | - | - | - |
| FB-MODERATE-PAD-to-AA-001 | Moderate | TBD | PENDING | - | - | - | - |
| FB-COMPLEX-PAD-to-AA-001 | Complex | TBD | PENDING | - | - | - | - |
| FB-SUPERCOMPLEX-PAD-to-AA-001 | Super Complex | TBD | PENDING | - | - | - | - |
| FB-ENTERPRISE-PAD-to-AA-001 | Enterprise | TBD | PENDING | - | - | - | - |

### Automation Anywhere → Blue Prism

| Test ID | Tier | Source Artifact | Status | Source Valid | Converted | Target Valid | Evidence |
|---------|------|-----------------|--------|--------------|-----------|--------------|----------|
| FB-SIMPLE-AA-to-BP-001 | Simple | TBD | PENDING | - | - | - | - |
| FB-MODERATE-AA-to-BP-001 | Moderate | TBD | PENDING | - | - | - | - |
| FB-COMPLEX-AA-to-BP-001 | Complex | TBD | PENDING | - | - | - | - |
| FB-SUPERCOMPLEX-AA-to-BP-001 | Super Complex | TBD | PENDING | - | - | - | - |
| FB-ENTERPRISE-AA-to-BP-001 | Enterprise | TBD | PENDING | - | - | - | - |

---

## Artifact Locations

### Windows Lab (C:\flowbots_lab\)
- `artifacts_source\uipath\<tier>\` - UiPath .nupkg files
- `artifacts_source\pad\<tier>\` - PAD .zip exports
- `artifacts_source\aa\<tier>\` - AA bot exports
- `artifacts_source\blueprism\<tier>\` - Blue Prism .bprelease files
- `artifacts_converted\<target>\<tier>\` - Converted outputs
- `runs\<test_id>\source\` - Source run evidence
- `runs\<test_id>\target\` - Target run evidence

### Mac Lab (/Users/bjwet/flowbots_e2e_lab/)
- `evidence/` - Screenshots, logs, recordings
- `scripts/` - Automation scripts
- `PLATFORM_RUNBOOKS/` - Per-platform documentation
