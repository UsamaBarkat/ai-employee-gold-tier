# Personal AI Employee Hackathon - Complete Details

## Hackathon Overview

**Title:** Personal AI Employee Hackathon 0: Building Autonomous FTEs in 2026

**Tagline:** Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

**Concept:** Build a "Digital FTE" (Full-Time Equivalent) - an AI agent powered by Claude Code and Obsidian that proactively manages personal and business affairs 24/7.

## Digital FTE Value Proposition

### Human FTE vs Digital FTE Comparison

| Feature | Human FTE | Digital FTE |
|---------|-----------|-------------|
| Availability | 40 hours/week | 168 hours/week (24/7) |
| Monthly Cost | $4,000 - $8,000+ | $500 - $2,000 |
| Ramp-up Time | 3-6 months | Instant (via SKILL.md) |
| Consistency | 85-95% accuracy | 99%+ consistency |
| Scaling | Linear (hire 10 for 10x work) | Exponential (instant duplication) |
| Cost per Task | $3.00 - $6.00 | $0.25 - $0.50 |
| Annual Hours | ~2,000 hours | ~8,760 hours |

**Key Insight:** 85-90% cost savings - Digital FTE works 9,000 hours/year vs human's 2,000 hours

## Architecture & Tech Stack

### Core Components

1. **The Brain:** Claude Code (reasoning engine)
   - Uses Ralph Wiggum Stop hook for continuous iteration until task complete

2. **The Memory/GUI:** Obsidian (local Markdown)
   - Dashboard and data storage
   - Privacy-focused, local-first approach

3. **The Senses (Watchers):** Lightweight Python scripts
   - Monitor Gmail, WhatsApp, filesystems
   - Trigger the AI agent when needed

4. **The Hands (MCP):** Model Context Protocol servers
   - Handle external actions (sending emails, clicking buttons, etc.)

### Key Innovation
Solves the "lazy agent" problem by using Watchers to wake the agent and Ralph Wiggum pattern to keep it working until done.

## Prerequisites & Setup

### Required Software

| Component | Requirement | Purpose |
|-----------|-------------|---------|
| Claude Code | Active subscription (or Free Gemini API with Claude Code Router) | Primary reasoning engine |
| Obsidian | v1.10.6+ (free) | Knowledge base & dashboard |
| Python | 3.13 or higher | Sentinel scripts & orchestration |
| Node.js | v24+ LTS | MCP servers & automation |
| GitHub Desktop | Latest stable | Version control for vault |

### Hardware Requirements

**Minimum:**
- 8GB RAM
- 4-core CPU
- 20GB free disk space

**Recommended:**
- 16GB RAM
- 8-core CPU
- SSD storage

**For always-on operation:**
- Dedicated mini-PC or cloud VM
- Stable internet (10+ Mbps recommended)

### Skill Level Expectations
- Comfortable with command-line interfaces (terminal/bash)
- Understanding of file systems and folder structures
- Familiarity with APIs (what they are, how to call them)
- No prior AI/ML experience required
- Able to use and prompt Claude Code
- Can convert AI functionality into Agent Skills

### Pre-Hackathon Checklist
- ✅ Install all required software
- ✅ Create Obsidian vault named "AI_Employee_Vault"
- ✅ Verify Claude Code: `claude --version`
- ⏳ Set up UV Python project
- ⏳ Join Wednesday Research Meeting

## Hackathon Tiers

### 🥉 Bronze Tier: Foundation (Minimum Viable Deliverable)
**Estimated Time:** 8-12 hours

**Requirements:**
- Obsidian vault with Dashboard.md and Company_Handbook.md
- One working Watcher script (Gmail OR file system monitoring)
- Claude Code successfully reading from and writing to vault
- Basic folder structure: /Inbox, /Needs_Action, /Done
- All AI functionality implemented as Agent Skills

### 🥈 Silver Tier: Functional Assistant
**Estimated Time:** 20-30 hours

**Requirements:**
- All Bronze requirements PLUS:
- Two or more Watcher scripts (Gmail + WhatsApp + LinkedIn)
- Automatically post on LinkedIn about business to generate sales
- Claude reasoning loop that creates Plan.md files
- One working MCP server for external action (e.g., sending emails)
- Human-in-the-loop approval workflow for sensitive actions
- Basic scheduling via cron or Task Scheduler
- All AI functionality implemented as Agent Skills

### 🥇 Gold Tier: Autonomous Employee
**Estimated Time:** 40+ hours

**Requirements:**
- All Silver requirements PLUS:
- Full cross-domain integration (Personal + Business)
- Accounting system in Odoo Community (self-hosted, local)
  - Integrate via MCP server using Odoo's JSON-RPC APIs (Odoo 19+)
- Facebook and Instagram integration (post messages, generate summaries)
- Twitter (X) integration (post messages, generate summaries)
- Multiple MCP servers for different action types
- Weekly Business and Accounting Audit with CEO Briefing generation
- Error recovery and graceful degradation
- Comprehensive audit logging
- Ralph Wiggum loop for autonomous multi-step task completion

## Standout Features

### "Monday Morning CEO Briefing"
AI autonomously audits:
- Bank transactions
- Task completion
- Revenue reports
- Bottleneck identification

Transforms AI from chatbot into proactive business partner.

### Proactive Management Domains
**Personal Affairs:**
- Gmail monitoring
- WhatsApp management
- Bank transaction tracking

**Business:**
- Social Media management
- Payment processing
- Project task tracking

## Research Meetings

**Schedule:** Every Wednesday at 10:00 PM

**Zoom Details:**
- Link: https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1
- Meeting ID: 871 8870 7642
- Passcode: 744832

**Alternative:**
- If Zoom is full, watch live or recording at: https://www.youtube.com/@panaversity

**Purpose:**
- Teaching each other how to build and enhance first AI Employee
- Collaborative learning
- Share progress and solutions

## Key Concepts

### Agent Engineering vs Prompt Engineering
This hackathon moves beyond simple prompt engineering into full "agent engineering" - building autonomous systems that reason, plan, and execute.

### Local-First Philosophy
- Privacy-focused
- Data stays on your machine
- No cloud dependencies for core functionality
- Obsidian as local knowledge base

### Human-in-the-Loop
- AI suggests actions
- Human approves sensitive operations
- Balance between automation and control

### Skills-Based Architecture
All AI functionality must be implemented as Agent Skills (SKILL.md files)

## Document Status
**Total Length:** ~28 pages
**Sections Received:**
- Overview and introduction
- Digital FTE concept
- Prerequisites and setup
- Tiered deliverables (Bronze, Silver, Gold)

**Still to Review:**
- Detailed implementation guides
- Watcher script examples
- MCP server setup
- Agent Skills tutorial
- Troubleshooting
- Submission guidelines
- Judging criteria
