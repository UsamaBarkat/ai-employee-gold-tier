# Email MCP Server Setup Guide

## What is MCP?

**Model Context Protocol (MCP)** is a standardized way for AI systems to perform external actions.

Think of it like this:
- **Watchers** = AI's eyes (read/monitor)
- **MCP Servers** = AI's hands (do actions)

## Your Email MCP Server

**Purpose:** Allows your AI Employee to send emails automatically

**Use Cases:**
- Send reports/summaries
- Email notifications
- Automated responses
- Business communications

---

## How It Works

```
AI detects need to send email
       ↓
Creates email draft task → inbox/
       ↓
YOU APPROVE the email (human-in-the-loop)
       ↓
Task moves to needs_action/
       ↓
AI calls Email MCP Server
       ↓
Email sent via Gmail SMTP! ✅
```

---

## Setup Steps (COMPLETED ✅)

### 1. Email MCP Server Script
- **File:** `email_mcp_server.py`
- **Purpose:** Python script that sends emails via Gmail
- **Status:** ✅ Created and tested

### 2. Configuration
- **File:** `email_config.json`
- **Contains:** Your Gmail credentials (App Password)
- **Status:** ✅ Configured

### 3. Agent Skill
- **File:** `.claude/skills/send-email.md`
- **Purpose:** Claude Code skill to trigger email sending
- **Status:** ✅ Created

### 4. Testing
- **Test Email:** Sent successfully! ✅
- **Recipient:** usamanizamani09@gmail.com
- **Result:** Email delivered

---

## How to Use

### Option 1: Direct Command
```bash
python email_mcp_server.py --to "recipient@email.com" --subject "Subject" --body "Message"
```

### Option 2: Via Agent Skill
Just ask Claude Code:
```
"Send an email to john@example.com about the project update"
```

Claude will:
1. Ask for subject and body
2. Show you a preview
3. Ask for confirmation
4. Send the email!

---

## Email Log

All sent emails are automatically logged to:
`AI_Employee_Vault/logs/email_log_[date].json`

Each log entry contains:
- Timestamp
- Recipient
- Subject
- Body preview
- Success/failure status

---

## Security Notes

✅ **Secure:**
- Uses Gmail App Password (not your main password)
- Email credentials stored locally only
- No credentials in code

⚠️ **Keep Safe:**
- Don't share `email_config.json`
- Don't commit it to GitHub
- Rotate App Password periodically

---

## Troubleshooting

### Authentication Failed
**Problem:** "Authentication failed" error
**Solution:**
1. Make sure you're using App Password (16 characters)
2. Visit: https://myaccount.google.com/apppasswords
3. Create new app password
4. Update `email_config.json`

### SMTP Connection Error
**Problem:** Can't connect to Gmail SMTP
**Solution:**
1. Check internet connection
2. Verify `smtp_server`: "smtp.gmail.com"
3. Verify `smtp_port`: 587

### Email Not Delivered
**Problem:** Email sent but not received
**Solution:**
1. Check recipient email address
2. Check spam folder
3. Verify Gmail account is active

---

## Integration with Other Features

### With LinkedIn Watcher
- LinkedIn Watcher detects activity
- AI creates summary email
- You approve
- Email sent automatically!

### With File Watcher
- File Watcher detects new file
- AI processes it
- Sends email notification
- You stay updated!

### With Plan.md Generation
- AI creates a plan
- Emails plan summary to you
- You review on-the-go!

---

## Silver Tier Requirement ✅

**Requirement:** "One working MCP server for external action (e.g., sending emails)"

**Status:** ✅ COMPLETE

**What we built:**
- ✅ Email MCP Server (Python script)
- ✅ Gmail SMTP integration
- ✅ Configuration system
- ✅ Agent Skill integration
- ✅ Logging & error handling
- ✅ Human-in-the-loop workflow
- ✅ Successfully tested

---

## Next Steps (Optional Enhancements)

Want to make it even better? You could add:
- HTML email templates
- Attachment support
- CC/BCC functionality (already supported!)
- Email templates library
- Scheduled emails
- Email response parsing

But for the hackathon, **what you have is PERFECT!** ✅

---

**Created:** 2026-03-04
**Status:** Production Ready
**Silver Tier:** COMPLETE! 🎉
