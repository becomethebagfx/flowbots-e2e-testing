# FLOWBOTS E2E - EVIDENCE INDEX

## Evidence Types
- **LOG**: Execution logs from RPA tools
- **SCREENSHOT**: Visual proof of execution state
- **RECORDING**: Video capture of automation run
- **EXPORT**: Native tool export/report
- **CONVERSION**: FLOWBOTS conversion output/logs

## Evidence Naming Convention
`<TEST_ID>_<TYPE>_<TIMESTAMP>.<ext>`

Example: `FB-SIMPLE-UIPATH-to-PAD-001_LOG_20260103-193000.txt`

---

## Evidence Registry

### Infrastructure Setup

| Test ID | Type | Filename | Location | Timestamp | Notes |
|---------|------|----------|----------|-----------|-------|
| SETUP-001 | LOG | setup_ssh_attempt.log | /Users/bjwet/flowbots_e2e_lab/evidence/ | 2026-01-03 | SSH connection attempts |

---

### Source Validation Evidence

| Test ID | Type | Filename | Location | Timestamp | Valid |
|---------|------|----------|----------|-----------|-------|
| (pending) | | | | | |

---

### Conversion Evidence

| Test ID | Type | Filename | Location | Timestamp | Success |
|---------|------|----------|----------|-----------|---------|
| (pending) | | | | | |

---

### Target Validation Evidence

| Test ID | Type | Filename | Location | Timestamp | Valid |
|---------|------|----------|----------|-----------|-------|
| (pending) | | | | | |

---

## Windows Lab Paths (C:\flowbots_lab\)
- `runs\<test_id>\source\` - Source platform run evidence
- `runs\<test_id>\target\` - Target platform run evidence
- `logs\` - Aggregated logs
- `screenshots\` - Screenshots
- `recordings\` - Video recordings
