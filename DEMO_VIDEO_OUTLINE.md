# Demo Video Outline - AI Employee Hackathon

**Target Length:** 5-10 minutes
**Format:** Screen recording + voiceover
**Tool:** OBS Studio (free) or Windows Game Bar (Win+G)

---

## Video Structure

### 1. Introduction (1 minute)

**Show:** Title slide or README on screen

**Say:**
> "Hi! I'm Usama Nizamani. I built a Personal AI Employee for the Panaversity Hackathon - achieving 100% Gold Tier completion.
> This AI Employee works 24/7, monitoring LinkedIn, processing tasks, and generating strategic business insights - all while keeping me in control through human-in-the-loop workflows.
> Let me show you what it can do."

---

### 2. System Overview (1 minute)

**Show:** Dashboard.md in Obsidian

**Say:**
> "This is the Dashboard - the AI Employee's control center.
> You can see the system status: 2 watchers running, 19 Agent Skills configured, 5 MCP servers active.
> We've completed all 3 tiers: Bronze, Silver, and Gold - 21 features total."

**Point out:**
- Watchers section
- Agent Skills count
- MCP Servers
- Project Progress (100% Gold)

---

### 3. LinkedIn Watcher in Action (2 minutes)

**Show:**
1. LinkedIn Watcher running (command window)
2. AI_Employee_Vault/inbox/ folder
3. A task file created by watcher

**Say:**
> "The LinkedIn Watcher monitors my LinkedIn every 5 minutes automatically.
> [Show watcher output]
> When it detects a post with tracked hashtags like #AgenticAI or #Panaversity, it creates a task file in the inbox.
> [Show inbox folder and open a task file]
> Here's a task it created - you can see the post content, timestamp, and suggested actions.
> This runs 24/7 via Windows Task Scheduler."

**Show:** Task Scheduler (optional - if time)

---

### 4. Human-in-the-Loop Workflow (2 minutes)

**Show:** Agent Skills in action

**Say:**
> "Now let me show the human-in-the-loop workflow - this is what makes it safe.
> I'll use Claude Code to process this task."

**Demo:**
1. Run `/check-inbox` skill → shows pending tasks
2. Run `/process-task` → moves task to needs_action
3. Show Pending_Approval folder
4. Explain: "For sensitive actions like posting, I approve first"
5. Move file to Approved folder
6. Explain: "Now the AI can act"

**Say:**
> "This approval workflow ensures the AI never does anything without my permission.
> It's autonomous but controlled."

---

### 5. CEO Briefing - Strategic Intelligence (2 minutes)

**Show:**
1. Business_Goals.md
2. Generate CEO Briefing (or show existing one)
3. CEO_Briefing_2026-03-10.md

**Say:**
> "Here's my favorite feature - the CEO Briefing system.
> [Show Business_Goals.md]
> I set my strategic objectives here.
> [Show briefing generation or existing briefing]
> The AI analyzes completed tasks, system performance, and generates a weekly executive summary.
> It identifies bottlenecks, suggests improvements, and tracks progress toward goals.
> This transforms the AI from a task executor to a strategic business partner."

**Point out:**
- Executive Summary
- Goals Progress
- Proactive Suggestions

---

### 6. Infrastructure & Capabilities (1-2 minutes)

**Show:** Quick overview of:
1. Audit logs folder
2. Error recovery code (briefly)
3. Watchdog script
4. MCP servers

**Say:**
> "What makes this production-ready is the infrastructure.
> [Show logs] Every action is audited for security.
> [Show error_recovery.py] Automatic retry logic handles failures.
> [Show watchdog.py] Watchdog monitoring auto-restarts crashed processes.
> [Show MCP servers] And 5 MCP servers provide hands - email, SMS, calendar, accounting, social media."

---

### 7. Architecture (30 seconds)

**Show:** ARCHITECTURE.md diagram or draw simple flow

**Say:**
> "The architecture is clean: Watchers perceive, Obsidian stores, Claude Code reasons, MCP servers act.
> Human-in-the-loop sits in the middle for control.
> Everything local-first for privacy."

---

### 8. Closing (30 seconds)

**Show:** README or Dashboard

**Say:**
> "In 7 days and 50 hours, I went from beginner to building a production-ready AI Employee.
> 100% Gold Tier complete: 21 features, 19 Agent Skills, 5 MCP servers.
> It monitors LinkedIn 24/7, generates strategic insights, and keeps me in control.
> All code and documentation is in the GitHub repo.
> Thank you for watching!"

**End screen:**
- GitHub link
- LinkedIn profile
- "100% Gold Tier Complete"

---

## Recording Tips

### Before Recording:
1. ✅ Close unnecessary windows
2. ✅ Clean up desktop
3. ✅ Test screen recorder
4. ✅ Prepare examples (have task files ready)
5. ✅ Practice once (don't memorize, just flow)

### During Recording:
- Speak clearly and at moderate pace
- Show, don't just tell
- Keep cursor movements smooth
- Pause briefly between sections

### After Recording:
- Review for audio quality
- Check if everything is visible
- Add title cards (optional)
- Upload to YouTube (unlisted is fine)

---

## Screen Recording Tools

### Option 1: OBS Studio (Free, Best Quality)
- Download: https://obsproject.com/
- Click "Start Recording"
- Record desktop + audio
- Stop when done
- Find video in Videos folder

### Option 2: Windows Game Bar (Built-in)
- Press Win+G
- Click record button
- Record
- Stop
- Find in Captures folder

### Option 3: ShareX (Free, Easy)
- Download: https://getsharex.com/
- Screen recording mode
- Record desktop + audio

---

## Upload to YouTube

1. Go to YouTube Studio
2. Click "Create" → "Upload video"
3. Select your video file
4. Title: "Personal AI Employee - Gold Tier Complete - Panaversity Hackathon"
5. Description: Brief overview + GitHub link
6. Visibility: **Unlisted** (judges can view, not public)
7. Copy video link for submission form

---

## Estimated Time

- Setup & practice: 15 min
- Recording: 10 min (might need 2-3 takes)
- Upload: 5 min
- **Total: 30 minutes**

---

**You got this! Keep it simple, show the highlights, be yourself.** 🎬

Good luck! 🚀
