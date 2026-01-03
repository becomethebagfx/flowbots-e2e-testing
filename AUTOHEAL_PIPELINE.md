# FLOWBOTS Auto-Heal Pre-Release Validation Pipeline

## Executive Summary
This pipeline ensures converted automations are validated before delivery to clients. No artifact is released until it passes execution tests in the target platform.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     FLOWBOTS CONVERSION PIPELINE                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────┐    ┌────────────┐    ┌──────────────┐    ┌────────────┐  │
│  │  INGEST  │───►│  CONVERT   │───►│   VALIDATE   │───►│  RELEASE   │  │
│  │          │    │            │    │              │    │            │  │
│  │ Source   │    │ FLOWBOTS   │    │ Windows Lab  │    │ Client     │  │
│  │ Artifact │    │ Engine     │    │ Runner       │    │ Delivery   │  │
│  └──────────┘    └────────────┘    └──────────────┘    └────────────┘  │
│        │              │                   │                   │         │
│        │              │                   │                   │         │
│        ▼              ▼                   ▼                   ▼         │
│  ┌──────────┐    ┌────────────┐    ┌──────────────┐    ┌────────────┐  │
│  │  FORMAT  │    │  CONVRSN   │    │  EXECUTION   │    │  RELEASE   │  │
│  │  CHECK   │    │  LOGS      │    │  LOGS        │    │  AUDIT     │  │
│  └──────────┘    └────────────┘    └──────────────┘    └────────────┘  │
│                                                                          │
│                         ┌────────────┐                                  │
│                         │ AUTO-HEAL  │◄─── On Failure                   │
│                         │   ENGINE   │                                  │
│                         └────────────┘                                  │
│                               │                                          │
│                               ▼                                          │
│                         ┌────────────┐                                  │
│                         │   RETRY    │───► Max 3 attempts               │
│                         │   QUEUE    │                                  │
│                         └────────────┘                                  │
│                               │                                          │
│                               ▼                                          │
│                         ┌────────────┐                                  │
│                         │   ISSUE    │───► Manual Review                │
│                         │   TRACKER  │                                  │
│                         └────────────┘                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Specifications

### 1. Ingest Component
**Purpose:** Accept source automation artifacts

**Inputs:**
- Source file (various formats per platform)
- Metadata (source platform, version, tier)
- Client identifier

**Validations:**
- File format verification
- Size limits (max 100MB default)
- Malware scan
- Duplicate detection

**Outputs:**
- Ingestion ID
- Validated source artifact in queue

### 2. Convert Component
**Purpose:** Execute FLOWBOTS conversion engine

**Inputs:**
- Validated source artifact
- Target platform specification
- Conversion options

**Process:**
- Call FLOWBOTS conversion API
- Monitor progress
- Capture conversion logs

**Outputs:**
- Converted artifact
- Conversion log
- Status (success/failure)

### 3. Validate Component
**Purpose:** Execute converted automation in isolated environment

**Execution Environment:**
- **Primary:** Windows Vultr VPS (45.63.68.224)
- **Isolation:** Fresh user session per test
- **Timeout:** 5 minutes default, configurable per tier

**Test Procedure:**
1. Import converted artifact into target platform
2. Configure test inputs (standardized per tier)
3. Execute automation
4. Capture execution logs
5. Verify expected outputs
6. Generate pass/fail verdict

**Outputs:**
- Execution result (PASS/FAIL)
- Execution logs
- Screenshots/recordings
- Output artifacts

### 4. Release Component
**Purpose:** Deliver validated artifact to client

**Gates:**
- Validation PASS required
- Manual approval for Enterprise tier
- Audit log complete

**Delivery Methods:**
- Web download
- API retrieval
- Email notification

### 5. Auto-Heal Engine
**Purpose:** Attempt automatic fixes for common failures

**Triggers:**
- Validation failure
- Known error patterns

**Healing Strategies:**

| Error Pattern | Auto-Heal Action |
|---------------|------------------|
| Missing dependency | Inject standard dependencies |
| Path mismatch | Normalize paths to target convention |
| Selector format | Convert selector syntax |
| Variable naming | Rename to target platform convention |
| Action unavailable | Map to equivalent action |

**Limits:**
- Max 3 auto-heal attempts per conversion
- Escalate to manual review after limit

### 6. Issue Tracker
**Purpose:** Track failures requiring manual intervention

**Fields:**
- Conversion ID
- Source/Target platforms
- Error signature
- Auto-heal attempts
- Manual review status
- Resolution

## Queue Management

### Priority Levels
1. **Urgent:** Client-flagged, 15-min SLA
2. **Standard:** Normal conversions, 1-hour SLA
3. **Batch:** Bulk conversions, 24-hour SLA

### Queue States
- PENDING: Awaiting processing
- IN_PROGRESS: Currently processing
- VALIDATING: In validation stage
- HEALING: Auto-heal in progress
- BLOCKED: Awaiting manual review
- COMPLETE: Successfully delivered

## Gating Rules

### Release Gates
- [ ] Source format validated
- [ ] Conversion completed without fatal errors
- [ ] Target artifact parseable
- [ ] Execution test passed OR manual override
- [ ] Audit log complete

### Escalation Gates
- Conversion timeout (>10 minutes)
- Validation failure after 3 attempts
- Unknown error pattern
- Enterprise tier (requires manual review)

## Audit Requirements

### Logged Events
- Ingest: timestamp, source, client, hash
- Convert: start, end, status, logs
- Validate: attempts, results, evidence
- Release: timestamp, recipient, method
- Heal: attempts, actions, outcomes

### Retention
- Logs: 90 days
- Artifacts: 30 days (source), 90 days (converted)
- Evidence: 90 days

## SLA Bounds

| Tier | Conversion SLA | Validation SLA | Total SLA |
|------|----------------|----------------|-----------|
| Simple | 2 min | 2 min | 5 min |
| Moderate | 5 min | 5 min | 12 min |
| Complex | 10 min | 10 min | 25 min |
| Super Complex | 15 min | 15 min | 35 min |
| Enterprise | 30 min | 30 min + manual | 24 hours |

## Retry Bounds

| Stage | Max Retries | Backoff |
|-------|-------------|---------|
| Ingest | 3 | Exponential (1s, 2s, 4s) |
| Convert | 2 | Linear (30s) |
| Validate | 3 | Linear (60s) |
| Heal | 3 | None (immediate) |

## Implementation Phases

### Phase 1: Manual Pipeline (Current)
- Manual upload via web
- Manual validation on Windows lab
- Manual evidence collection
- Issue tracking via markdown files

### Phase 2: Semi-Automated
- API-based conversion trigger
- Automated validation execution
- Automated log collection
- Issue tracking integration

### Phase 3: Fully Automated
- CI/CD pipeline integration
- Container-based validation (where possible)
- Automated healing
- Dashboard and metrics

## Windows Lab Runner Details

### Environment
- **Host:** Windows Vultr VPS (45.63.68.224)
- **User:** Administrator
- **Lab Path:** C:\flowbots_lab\

### Installed Platforms
- UiPath Studio/Robot
- Power Automate Desktop
- Automation Anywhere Bot Agent
- Blue Prism

### Execution Isolation
- Create test-specific subfolder per run
- Clean up after successful validation
- Preserve evidence on failure

### Resource Limits
- Max 1 concurrent validation
- CPU threshold: 85%
- Memory threshold: 80%
- Disk: Min 10GB free

## Monitoring and Alerts

### Metrics
- Conversion success rate
- Validation success rate
- Average processing time
- Queue depth
- Auto-heal effectiveness

### Alerts
- Queue depth > 10
- Conversion failure rate > 20%
- Validation timeout
- Resource exhaustion
- Pipeline stuck > 30 min

## Future Enhancements
1. Container-based validation for web automations
2. Parallel validation runners
3. ML-based auto-heal improvements
4. Client self-service portal
5. Real-time conversion streaming
