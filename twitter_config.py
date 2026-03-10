"""
Twitter/X Configuration for AI Employee
Gold Tier Feature - Twitter Integration Settings
"""

# Twitter/X Account Credentials
# Get these from: https://developer.twitter.com/en/portal/dashboard

TWITTER_EMAIL = "your_twitter_email@example.com"  # Your Twitter login email
TWITTER_USERNAME = "@YourUsername"  # Your Twitter handle
TWITTER_PASSWORD = "your_twitter_password"  # Your Twitter password

# Alternative: Twitter API v2 Credentials (More reliable, requires developer account)
# Get from: https://developer.twitter.com/en/portal/projects-and-apps
TWITTER_API_KEY = ""  # API Key
TWITTER_API_SECRET = ""  # API Key Secret
TWITTER_ACCESS_TOKEN = ""  # Access Token
TWITTER_ACCESS_SECRET = ""  # Access Token Secret
TWITTER_BEARER_TOKEN = ""  # Bearer Token

# Monitoring Settings
TRACK_HASHTAGS = [
    "#AgenticAI",
    "#Panaversity",
    "#AI",
    "#ArtificialIntelligence",
    "#Python",
    "#ClaudeCode"
]

TRACK_USERS = [
    "@panaversity",  # Replace with actual accounts to monitor
    # Add more Twitter accounts to monitor
]

# How often to check Twitter (seconds)
CHECK_INTERVAL = 300  # 5 minutes

# Maximum posts to fetch per check
MAX_POSTS_PER_CHECK = 10

# Vault path
VAULT_PATH = r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault"

# Tracking file
PROCESSED_TWEETS_FILE = f"{VAULT_PATH}/twitter_processed.json"
