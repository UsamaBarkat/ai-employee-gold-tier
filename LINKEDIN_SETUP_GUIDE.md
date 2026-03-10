# LinkedIn Watcher Setup Guide

## ✅ What We've Built

Your LinkedIn Watcher will monitor:
1. **Posts from people you follow** (max 5/day)
2. **Posts from Panaversity teachers** (Zia Khan, Ameen Alam, etc.)
3. **Comments on your posts**
4. **Connection requests**

---

## 🔧 Setup Steps

### Step 1: Add Your LinkedIn Credentials ⚠️ IMPORTANT

Open `linkedin_config.py` and add your LinkedIn login:

```python
# LinkedIn credentials
LINKEDIN_EMAIL = "your-email@example.com"  # Replace with YOUR email
LINKEDIN_PASSWORD = "your-password-here"    # Replace with YOUR password
```

**Security Note:**
- This file stores your password locally (not shared anywhere)
- Keep this file private - don't share it or commit to GitHub!
- We'll add better security later (encryption)

---

### Step 2: Make Sure Chrome Browser is Installed

The watcher uses Chrome browser to access LinkedIn.

- **Check if you have Chrome:** Open Chrome browser
- **Don't have Chrome?** Download from: https://www.google.com/chrome/

---

### Step 3: Test the Watcher

Run a test to make sure everything works:

```bash
python linkedin_watcher.py
```

When it asks for mode:
- Choose **1** (Test run) for your first time
- This will run ONE check and show you what it finds

---

## 📋 What the Watcher Does

### Connection Requests
```
Goes to: https://www.linkedin.com/mynetwork/invitation-manager/
Checks: New connection requests
Creates task: "Connection Request from [Name]"
```

### Feed Posts
```
Goes to: https://www.linkedin.com/feed/
Checks: Posts with #AgenticAI, #AI, #Panaversity
From: People you follow + Panaversity teachers
Creates task: "New post from [Author]"
Limit: Max 5 posts per day
```

### Your Post Comments
```
Goes to: Your recent activity
Checks: New comments on your posts
Creates task: "Reply to [Person]'s comment"
```

---

## 🎯 Configuration Options

You can customize in `linkedin_config.py`:

### Change Daily Post Limit
```python
"max_posts_per_day": 10,  # Increase to 10 posts
```

### Add More Teachers
```python
"track_specific_users": [
    "Zia Khan",
    "Ameen Alam",
    "Sir Qasim",  # Add more names here
],
```

### Add More Hashtags
```python
"track_hashtags": [
    "#AgenticAI",
    "#Panaversity",
    "#AI",
    "#Python",      # Add more hashtags
    "#Hackathon",
],
```

### Change Check Interval
```python
CHECK_INTERVAL = 300  # 300 seconds = 5 minutes
# Change to 600 for 10 minutes
# Change to 1800 for 30 minutes
```

---

## 🚀 Running Modes

### Mode 1: Test Run (Recommended First)
```bash
python linkedin_watcher.py
# Choose: 1

# This will:
- Run ONE check only
- Show you what it finds
- Keep browser open so you can see
- Good for testing!
```

### Mode 2: Continuous Monitoring
```bash
python linkedin_watcher.py
# Choose: 2

# This will:
- Run checks every 5 minutes (configurable)
- Run forever until you stop it (Ctrl+C)
- Browser runs in background
- This is for real use!
```

---

## 📁 Where Tasks Are Saved

All LinkedIn tasks go to:
```
AI_Employee_Vault/inbox/LinkedIn_*.md
```

Example filenames:
- `LinkedIn_connection_request_20260303_140530.md`
- `LinkedIn_linkedin_post_20260303_140600.md`

---

## 🔍 How to Check If It's Working

### After running test mode:

1. **Check inbox folder:**
   ```bash
   dir AI_Employee_Vault\inbox
   ```

2. **Look for LinkedIn files:**
   - Should see `LinkedIn_*.md` files

3. **Open a task file:**
   - Should contain details about the LinkedIn activity

4. **Use your Agent Skills:**
   ```
   /check-inbox     # See all tasks
   /update-dashboard   # Update Dashboard
   ```

---

## ⚠️ Troubleshooting

### Problem: "Login failed"
**Solution:**
- Check email/password in `linkedin_config.py`
- LinkedIn may require verification - log in manually first in Chrome

### Problem: "ChromeDriver not found"
**Solution:**
- Make sure Chrome browser is installed
- The script auto-downloads ChromeDriver

### Problem: "No tasks created"
**Solution:**
- Maybe no new activity on LinkedIn (normal!)
- Try posting something, then run watcher
- Check if you follow people who post with your hashtags

### Problem: Browser opens but nothing happens
**Solution:**
- LinkedIn may have changed their website
- Check console for error messages
- May need to update selectors (we'll help!)

---

## 🔐 Security Best Practices

### NOW (Quick Start):
- Password in `linkedin_config.py`
- File stays on your computer only
- Don't share the file

### LATER (Better Security):
- Use environment variables
- Encrypt credentials
- Use OAuth (if available)

---

## 📊 Expected Results

### Daily Activity (typical):
- **Connection requests:** 0-3 per day
- **Relevant posts:** 2-5 per day (you set max 5)
- **Comments on your posts:** 0-10 (depends on your posting)

**Total tasks:** ~5-15 per day (manageable!)

---

## 🎓 Learning Notes

### What you're learning:
- ✅ Web scraping with Selenium
- ✅ Browser automation
- ✅ API-like data extraction
- ✅ Task automation
- ✅ File-based workflows

### Skills gained:
- Python automation
- LinkedIn platform understanding
- Data extraction
- Task management systems

---

## 🚨 Important LinkedIn Notes

1. **Don't over-scrape:**
   - Keep 5-minute intervals minimum
   - Don't run multiple instances
   - LinkedIn may block suspicious activity

2. **Respect LinkedIn Terms:**
   - This is for personal use only
   - Not for commercial scraping
   - Educational/hackathon purposes

3. **If LinkedIn blocks you:**
   - Log in manually to verify it's you
   - Increase CHECK_INTERVAL (e.g., 30 minutes)
   - Reduce activity temporarily

---

## ✅ Next Steps After Setup

1. **Test the watcher** (Mode 1)
2. **Check inbox for tasks**
3. **Run continuously** (Mode 2)
4. **Set up Task Scheduler** (automate startup)
5. **Add Human-in-the-loop approval** (Silver Tier feature)
6. **Add auto-post feature** (Silver Tier feature)

---

## 📞 Need Help?

If you get stuck:
1. Check error messages carefully
2. Ask Claude Code for help (me!)
3. Share the error message
4. We'll debug together!

---

**Ready to test?**

1. Add your LinkedIn credentials to `linkedin_config.py`
2. Run `python linkedin_watcher.py`
3. Choose Mode 1 (Test run)
4. Watch the magic happen! ✨
