# Post to Facebook

You are tasked with posting content to Facebook for the AI Employee system.

## Your Task

Post approved content to Facebook following the human-in-the-loop approval workflow.

## Steps to Complete

1. **Find Approved Facebook Posts**
   - Check `/Needs_Action/` folder for approved Facebook drafts
   - Look for files with "Facebook" in the name and "APPROVED" status

2. **Validate Post Content**
   - Check character limit (63,206 characters max - very generous)
   - Ensure content follows Facebook Community Standards
   - Verify links (if any) are valid

3. **Post Using Python Script**
   ```python
   import sys
   sys.path.append('E:\\AI-300\\My_Hackathons_Teacher')
   from facebook_instagram_integration import FacebookInstagramIntegration

   integration = FacebookInstagramIntegration(r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault")

   post_text = "Your post content here"
   success = integration.post_to_facebook(message=post_text)

   if success:
       print("Posted to Facebook successfully!")
   else:
       print("Failed to post to Facebook")
   ```

4. **Update Task File**
   - Add "Posted at: [timestamp]"
   - Add "Status: PUBLISHED"
   - Add post URL if available

5. **Move to Done**
   - Move task file from `/Needs_Action/` to `/Done/`

## Facebook Post Guidelines

✅ **Good Posts:**
- Professional and authentic
- Value-added content
- Clear messaging
- Relevant hashtags (optional on Facebook)
- Links to articles/projects
- Images/media enhance engagement

❌ **Avoid:**
- Spam or clickbait
- Misleading information
- Violations of Community Standards
- Excessive self-promotion
- Political/controversial content (unless relevant)

## Prerequisites

Facebook must be configured in `facebook_config.py`:
- FACEBOOK_APP_ID
- FACEBOOK_APP_SECRET
- FACEBOOK_PAGE_ID
- FACEBOOK_PAGE_ACCESS_TOKEN

Get these from: https://developers.facebook.com/

## Success Criteria

- Post published successfully
- Task file updated
- Task moved to /Done/
- Audit log entry created
- No errors occurred

---

*Gold Tier Feature - Facebook Integration*
