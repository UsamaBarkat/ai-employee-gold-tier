"""
Facebook/Instagram Configuration for AI Employee
Gold Tier Feature - Social Media Integration Settings
"""

# Facebook App Credentials
# Get these from: https://developers.facebook.com/apps/

FACEBOOK_APP_ID = ""  # Your Facebook App ID
FACEBOOK_APP_SECRET = ""  # Your Facebook App Secret
FACEBOOK_ACCESS_TOKEN = ""  # User Access Token (long-lived recommended)

# Instagram Business Account
# Note: Instagram API requires a Business or Creator account linked to a Facebook Page
INSTAGRAM_BUSINESS_ACCOUNT_ID = ""  # Your Instagram Business Account ID

# Facebook Page (Required for Instagram posting)
FACEBOOK_PAGE_ID = ""  # Your Facebook Page ID
FACEBOOK_PAGE_ACCESS_TOKEN = ""  # Page Access Token

# API Version
API_VERSION = "v18.0"  # Facebook Graph API version

# Monitoring Settings
TRACK_HASHTAGS = [
    "AgenticAI",
    "Panaversity",
    "AI",
    "ArtificialIntelligence",
    "Python",
    "Hackathon"
]

# How often to check (seconds)
CHECK_INTERVAL = 600  # 10 minutes (Facebook rate limits are strict)

# Maximum posts to fetch per check
MAX_POSTS_PER_CHECK = 10

# Vault path
VAULT_PATH = r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault"

# Tracking file
PROCESSED_POSTS_FILE = f"{VAULT_PATH}/facebook_processed.json"

# Post Settings
DEFAULT_POST_VISIBILITY = "public"  # public, friends, only_me
ENABLE_INSTAGRAM_POSTING = True
ENABLE_FACEBOOK_POSTING = True

# Character limits
FACEBOOK_POST_MAX_LENGTH = 63206  # Facebook has very high limit
INSTAGRAM_CAPTION_MAX_LENGTH = 2200  # Instagram caption limit
INSTAGRAM_HASHTAG_MAX = 30  # Maximum hashtags per Instagram post
