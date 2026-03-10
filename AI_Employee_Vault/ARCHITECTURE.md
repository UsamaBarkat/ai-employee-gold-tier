# AI Employee Architecture Documentation

**Project:** Personal AI Employee - Panaversity Hackathon
**Author:** Usama Nizamani
**Tier Completed:** Gold Tier
**Date:** March 10, 2026

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Layers](#architecture-layers)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [Technology Stack](#technology-stack)
6. [Security & Privacy](#security--privacy)
7. [Deployment](#deployment)

---

## System Overview

The AI Employee is an autonomous, local-first agent system that manages personal and business tasks 24/7. Built on Claude Code as the reasoning engine and Obsidian as the knowledge base, it combines watchers (perception), AI reasoning, and MCP servers (actions) to create a fully autonomous digital assistant.

### Key Capabilities
- **24/7 Monitoring:** LinkedIn, file system, and future integrations
- **Autonomous Reasoning:** Claude Code processes tasks and makes decisions
- **Human-in-the-Loop:** Sensitive actions require approval
- **Multi-Channel Actions:** Email, SMS, calendar, social media
- **Self-Monitoring:** Watchdog, error recovery, audit logging
- **Strategic Analysis:** Weekly CEO briefings with insights

### Architecture Philosophy
- **Local-First:** Privacy-focused, data stays on your machine
- **Agent-Driven:** AI decides what to do, not just what you ask
- **Human-in-the-Loop:** Safety through approval workflows
- **Resilient:** Error recovery, retry logic, watchdog monitoring

---

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL WORLD                           │
│   LinkedIn | Gmail | Files | Twitter | Calendar             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              PERCEPTION LAYER (Watchers)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   LinkedIn   │  │ File System  │  │ Twitter (Future)│  │
│  │   Watcher    │  │   Watcher    │  │    Watcher      │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬────────┘  │
└─────────┼──────────────────┼───────────────────┼───────────┘
          │                  │                   │
          ▼                  ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│           KNOWLEDGE BASE (Obsidian Vault)                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ /inbox/ → /Needs_Action/ → /Done/                     │ │
│  │ Dashboard.md | Business_Goals.md | Plans/             │ │
│  │ /Pending_Approval/ → /Approved/ | /Rejected/          │ │
│  │ /Briefings/ | /logs/ | /calendar/                     │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│           REASONING LAYER (Claude Code)                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Agent Skills (15 skills)                              │ │
│  │  • Task Management: check-inbox, process-task, etc.   │ │
│  │  • Approval: approve-task, reject-task, review-tasks  │ │
│  │  • Content: generate-twitter-post, copy-linkedin-post │ │
│  │  • Strategic: generate-ceo-briefing, generate-plan    │ │
│  │  • Actions: send-email, post-to-twitter, etc.         │ │
│  │  • Autonomous: ralph-loop (multi-step completion)     │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │
         ┌───────────────────┴────────────────────┐
         ▼                                        ▼
┌──────────────────────┐           ┌──────────────────────────┐
│  HUMAN-IN-THE-LOOP   │           │     ACTION LAYER         │
│  Approval Workflow   │           │   (MCP Servers)          │
│                      │           │  ┌──────────────────┐    │
│  Review → Approve    │──────────▶│  │ Email MCP        │    │
│     or Reject        │           │  │ SMS/Notify MCP   │    │
└──────────────────────┘           │  │ Calendar MCP     │    │
                                   │  │ (Twitter Future) │    │
                                   │  └──────────────────┘    │
                                   └──────────┬───────────────┘
                                              │
                                              ▼
                            ┌──────────────────────────────────┐
                            │     EXTERNAL ACTIONS             │
                            │  Send Email | Post Social Media  │
                            │  Create Calendar Event | Send SMS│
                            └──────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│         INFRASTRUCTURE LAYER (Gold Tier)                    │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐  │
│  │ Audit Logging  │  │ Error Recovery │  │   Watchdog   │  │
│  │ (All actions)  │  │ (Retry logic)  │  │ (Monitoring) │  │
│  └────────────────┘  └────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Watchers (Perception)

**LinkedIn Watcher** (`linkedin_watcher.py`)
- Monitors your LinkedIn posts for tracked hashtags
- Tracks connection requests
- Detects posts from followed users
- Runs every 5 minutes via Task Scheduler
- Creates tasks in `/inbox/` when activity detected

**File System Watcher** (`file_watcher.py`)
- Monitors file drops in watched folders
- Automatically creates tasks for new files
- Supports drag-and-drop workflows

**Future:** Twitter Watcher (planned, infrastructure ready)

### 2. Knowledge Base (Obsidian Vault)

**Folder Structure:**
```
AI_Employee_Vault/
├── inbox/                  # New unprocessed tasks
├── Needs_Action/          # Approved, ready to work on
├── Done/                  # Completed tasks
├── Pending_Approval/      # Awaiting human approval
├── Approved/              # Approved for action
├── rejected/              # Rejected tasks
├── plans/                 # Strategic plans
├── Briefings/             # CEO briefings
├── logs/                  # Audit logs
├── calendar/              # Events and reminders
├── Dashboard.md           # System overview
├── Business_Goals.md      # Objectives and metrics
└── Company_Handbook.md    # Operating guidelines
```

### 3. Reasoning Engine (Claude Code)

**15 Agent Skills:**

| Skill | Purpose | Tier |
|-------|---------|------|
| `check-inbox` | List pending tasks | Bronze |
| `process-task` | Move inbox → needs_action | Bronze |
| `complete-task` | Move to done | Bronze |
| `update-dashboard` | Refresh dashboard | Bronze |
| `approve-task` | Approve for action | Silver |
| `reject-task` | Reject with reason | Silver |
| `review-tasks` | List all pending approvals | Silver |
| `copy-linkedin-post` | Generate LinkedIn content | Silver |
| `post-to-linkedin` | Manual LinkedIn posting | Silver |
| `generate-plan` | Create strategic plans | Silver |
| `send-email` | Send via Email MCP | Silver |
| `generate-ceo-briefing` | Weekly business analysis | Gold |
| `ralph-loop` | Autonomous multi-step tasks | Gold |
| `generate-twitter-post` | Create Twitter content | Gold |
| `post-to-twitter` | Publish to Twitter | Gold |
| `view-audit-logs` | Review system logs | Gold |

### 4. Action Layer (MCP Servers)

**Email MCP Server** (`email_mcp_server.py`)
- Sends emails via Gmail SMTP
- Logs all sent emails
- Supports attachments

**SMS/Notification MCP** (`sms_mcp_server.py`)
- Sends SMS via email-to-SMS gateways
- Supports major carriers (Verizon, AT&T, T-Mobile, etc.)
- Notification logging

**Calendar/Reminder MCP** (`calendar_mcp_server.py`)
- Create calendar events
- Set reminders
- Check upcoming events
- Trigger time-based actions

### 5. Infrastructure (Gold Tier)

**Audit Logging** (`audit_logger.py`)
- Tracks every AI action
- JSON and text logs
- Security compliance
- Failed action tracking

**Error Recovery** (`error_recovery.py`)
- Retry logic with exponential backoff
- Graceful degradation
- Transient vs permanent error handling
- Service status tracking

**Watchdog Monitor** (`watchdog.py`)
- Monitors critical processes
- Auto-restarts crashed watchers
- Prevents restart loops
- Health reporting

---

## Data Flow

### Example: LinkedIn Post Detection → Approval → Action

1. **Detection (Watcher)**
   - LinkedIn Watcher detects new post with #AgenticAI hashtag
   - Creates `LinkedIn_post_20260310.md` in `/inbox/`

2. **Processing (Claude Code)**
   - User invokes `check-inbox` skill
   - Claude reads the task
   - Moves to `/Needs_Action/` (approved for review)

3. **Approval (Human-in-the-Loop)**
   - User reviews task
   - Decides action: engage, skip, or create content
   - Uses `approve-task` or `reject-task`

4. **Action (If Approved)**
   - Task moved to `/Approved/`
   - Claude executes appropriate action
   - Logs action to audit system

5. **Completion**
   - Task moved to `/Done/`
   - Dashboard updated
   - Audit log entry created

---

## Technology Stack

### Core Technologies
| Component | Technology | Version |
|-----------|------------|---------|
| AI Engine | Claude Code (Sonnet 4.5) | Latest |
| Knowledge Base | Obsidian | v1.10.6+ |
| Automation | Python | 3.13+ |
| Scheduling | Windows Task Scheduler | Built-in |
| Version Control | GitHub Desktop | Latest |

### Python Libraries
- `selenium` - Web automation (LinkedIn)
- `tweepy` - Twitter API integration
- `psutil` - Process monitoring
- `watchdog` - File system monitoring
- `smtplib` - Email sending (built-in)

### Development Tools
- Claude Code for AI reasoning
- VS Code for development
- Git for version control

---

## Security & Privacy

### Principles
1. **Local-First:** All data stored locally in Obsidian vault
2. **Human-in-the-Loop:** Sensitive actions require approval
3. **Audit Trail:** Every action logged
4. **Credential Safety:** .env files, never committed

### Security Measures
- Credentials in environment variables
- .env files in .gitignore
- Approval workflow for payments/posts
- Audit logging for all actions
- Rate limiting on external APIs

### Privacy
- No cloud storage of personal data
- API calls only when needed
- LinkedIn/Twitter credentials encrypted
- Email credentials via app passwords

---

## Deployment

### Local Deployment (Current)
1. Obsidian vault on local machine
2. Python scripts in project directory
3. Watchers scheduled via Task Scheduler
4. Claude Code runs in terminal

### Always-On Setup (Future - Platinum Tier)
1. Cloud VM for 24/7 operation
2. Synced Obsidian vault
3. Separate Cloud/Local responsibilities
4. Cloud drafts, Local approves/executes

---

## Performance Metrics

### System Stats (as of March 10, 2026)
- **Uptime:** 100% (monitored period)
- **Agent Skills:** 15
- **MCP Servers:** 3 (Email, SMS, Calendar)
- **Watchers:** 2 (LinkedIn, File System)
- **Tasks Processed:** 10+
- **Emails Sent:** 2
- **LinkedIn Posts:** 2
- **Tier Completion:** Gold Tier (9/11 features = 82%)

---

## Future Enhancements

### Platinum Tier (If Pursued)
- [ ] Cloud deployment (24/7 operation)
- [ ] Odoo accounting integration
- [ ] Facebook/Instagram integration
- [ ] Advanced A2A (Agent-to-Agent) communication
- [ ] More sophisticated approval workflows

### Continuous Improvement
- More watchers (WhatsApp, Email monitoring)
- Enhanced error recovery
- Better scheduling (cron-like syntax)
- Performance optimizations
- More MCP servers (Slack, Discord, etc.)

---

**This architecture enables a truly autonomous AI Employee that works 24/7 while maintaining human control over sensitive actions.**

---

*Generated: March 10, 2026*
*Gold Tier Achievement*
*Panaversity Hackathon 0*
