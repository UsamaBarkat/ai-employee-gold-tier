# LinkedIn Watcher Configuration
# Customized for Usama - Student Learning AI

# What to monitor
WATCH_CONFIG = {
    # Track posts from people you follow
    "watch_feed_posts": True,
    "max_posts_per_day": 5,

    # Track comments on your posts
    "watch_my_post_comments": True,

    # Track connection requests
    "watch_connection_requests": True,

    # Specific people to track (Panaversity teachers)
    "track_specific_users": [
        "Zia Khan",
        "Ameen Alam",
        # Add more teachers here as needed
    ],

    # Hashtags to track (from people you follow only)
    "track_hashtags": [
        "#AgenticAI",
        "#Panaversity",
        "#AI",
        "#ArtificialIntelligence",
    ],

    # Filter settings
    "only_from_following": True,  # Only people you follow
    "min_likes_for_post": 20,     # Quality filter (adjustable)
}

# Where to save tasks
VAULT_PATH = r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault"
INBOX_PATH = r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault\inbox"

# How often to check (in seconds)
CHECK_INTERVAL = 300  # 5 minutes (adjustable)

# LinkedIn credentials (REPLACE WITH YOUR OWN)
LINKEDIN_EMAIL = "your_linkedin_email@example.com"  # Your LinkedIn email
LINKEDIN_PASSWORD = "your_linkedin_password"  # Your LinkedIn password

# Your LinkedIn profile
LINKEDIN_PROFILE = "usama-nizamani-2170a1395"  # Your profile username
