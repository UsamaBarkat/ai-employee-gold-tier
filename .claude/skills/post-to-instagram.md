# Post to Instagram

You are tasked with posting content to Instagram for the AI Employee system.

## Your Task

Post approved content to Instagram following the human-in-the-loop approval workflow.

## Important: Instagram Requirements

⚠️ **Instagram REQUIRES an image!**
- Cannot post text-only to Instagram
- Image must be publicly accessible URL
- Recommended formats: JPG, PNG
- Minimum resolution: 600x600px
- Maximum file size: 8MB

## Steps to Complete

1. **Find Approved Instagram Posts**
   - Check `/Needs_Action/` folder for approved Instagram drafts
   - Verify post includes image URL or path

2. **Validate Post Content**
   - **Image:** Required, must exist and be accessible
   - **Caption:** Max 2,200 characters
   - **Hashtags:** Max 30 per post
   - Ensure content follows Instagram Community Guidelines

3. **Post Using Python Script**
   ```python
   import sys
   sys.path.append('E:\\AI-300\\My_Hackathons_Teacher')
   from facebook_instagram_integration import FacebookInstagramIntegration

   integration = FacebookInstagramIntegration(r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault")

   # Instagram requires a publicly accessible image URL
   image_url = "https://example.com/image.jpg"  # Must be public URL
   caption = "Your caption here"
   hashtags = ["AgenticAI", "Panaversity", "AI"]

   success = integration.post_to_instagram(
       image_path=image_url,
       caption=caption,
       hashtags=hashtags
   )

   if success:
       print("Posted to Instagram successfully!")
   else:
       print("Failed to post to Instagram")
   ```

4. **Update Task File**
   - Add "Posted at: [timestamp]"
   - Add "Status: PUBLISHED"
   - Add post URL if available

5. **Move to Done**
   - Move task file from `/Needs_Action/` to `/Done/`

## Instagram Post Guidelines

✅ **Good Posts:**
- High-quality visuals
- Engaging captions
- 3-5 relevant hashtags (up to 30 allowed)
- Authentic voice
- Value to followers
- Clear call-to-action

❌ **Avoid:**
- Low-quality/pixelated images
- Excessive hashtags (looks spammy)
- Misleading content
- Violation of Community Guidelines
- Copyright-infringing images

## Hashtag Strategy

**Required for AI Employee:**
- #AgenticAI
- #Panaversity

**Additional (choose 3-5):**
- #AI
- #Python
- #BuildInPublic
- #Hackathon
- #Automation
- #MachineLearning
- #TechJourney

## Prerequisites

Instagram must be configured in `facebook_config.py`:
- INSTAGRAM_BUSINESS_ACCOUNT_ID
- FACEBOOK_PAGE_ID (Instagram must be linked)
- FACEBOOK_PAGE_ACCESS_TOKEN

**Setup Requirements:**
1. Instagram Business or Creator Account
2. Linked to a Facebook Page
3. Facebook Developer App with Instagram permissions
4. Access tokens with proper scopes

Get credentials from: https://developers.facebook.com/

## Error Handling

Common issues:
- **"Image required"** → Instagram won't post without image
- **"Invalid image URL"** → Image must be publicly accessible
- **"Rate limit"** → Wait before retrying (Instagram limits: ~25 posts/day)
- **"No business account"** → Convert to Business/Creator account first

## Success Criteria

- Image posted successfully
- Caption included
- Hashtags applied
- Task file updated
- Task moved to /Done/
- Audit log entry created

---

*Gold Tier Feature - Instagram Integration*
