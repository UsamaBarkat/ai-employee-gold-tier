# Post to Twitter/X

You are tasked with posting content to Twitter/X for the AI Employee system.

## Your Task

Post approved content to Twitter following the human-in-the-loop approval workflow.

## Steps to Complete

1. **Find Approved Twitter Posts**
   - Check `/Needs_Action/` folder for approved Twitter drafts
   - Look for files with "Twitter" in the name and "APPROVED" status

2. **Validate Tweet Content**
   - Check character limit (280 characters max)
   - Ensure hashtags are appropriate
   - Verify content follows guidelines

3. **Post Using Python Script**
   ```python
   import sys
   sys.path.append('E:\\AI-300\\My_Hackathons_Teacher')
   from twitter_integration import TwitterIntegration

   twitter = TwitterIntegration(r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault")

   tweet_text = "Your tweet content here #AgenticAI #Panaversity"
   success = twitter.post_tweet(tweet_text)

   if success:
       print("Tweet posted successfully!")
   else:
       print("Failed to post tweet")
   ```

4. **Update Task File**
   - Add "Posted at: [timestamp]" to the file
   - Add "Status: PUBLISHED" to the file
   - Add tweet URL if available

5. **Move to Done**
   - Move the task file from `/Needs_Action/` to `/Done/`
   - This marks the task as complete

## Tweet Content Guidelines

✅ **Good Tweets:**
- Clear, concise messaging
- Relevant hashtags (2-5 max)
- Professional tone
- Value-added content
- Share learnings, progress, achievements

❌ **Avoid:**
- Excessive hashtags (spam)
- Negative or controversial content
- Personal/sensitive information
- Promotional spam
- Off-topic content

## Example Tweet Formats

### Progress Update:
```
Just completed [feature]! 🚀

✅ [Achievement 1]
✅ [Achievement 2]
✅ [Achievement 3]

Built with [tech stack]

#AgenticAI #Panaversity #AI
```

### Learning Share:
```
Today I learned: [insight]

[Brief explanation]

This will help me [benefit]

#Python #AI #LearningInPublic
```

### Hackathon Update:
```
[Milestone] reached! 🎉

[Brief description of what was achieved]

Tech: [tools used]
Next: [what's coming]

#Hackathon #BuildInPublic #AgenticAI
```

## Error Handling

If posting fails:
1. Check Twitter API credentials in `twitter_config.py`
2. Verify character limit
3. Check rate limits (can't post too frequently)
4. Log error to audit system
5. Move task to `/Needs_Action/` with error note

## Prerequisites

Twitter must be configured in `twitter_config.py`:
- TWITTER_API_KEY
- TWITTER_API_SECRET
- TWITTER_ACCESS_TOKEN
- TWITTER_ACCESS_SECRET
- TWITTER_BEARER_TOKEN

Get these from: https://developer.twitter.com/en/portal/dashboard

## Success Criteria

- Tweet posted successfully
- Task file updated with posted status
- Task moved to /Done/
- Audit log entry created
- No errors occurred

---

*Gold Tier Feature - Twitter/X Integration*
