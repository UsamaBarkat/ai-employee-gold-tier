"""
Twitter/X Integration for AI Employee
Gold Tier Feature - Auto-post and monitor Twitter
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

try:
    import tweepy
    TWEEPY_AVAILABLE = True
except ImportError:
    TWEEPY_AVAILABLE = False
    print("WARNING: tweepy not installed. Run: pip install tweepy")

from audit_logger import AuditLogger
import twitter_config as config


class TwitterIntegration:
    """Twitter/X integration for posting and monitoring"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / 'inbox'
        self.processed_file = Path(config.PROCESSED_TWEETS_FILE)
        self.audit_logger = AuditLogger(str(vault_path))

        # Load processed tweets
        self.processed_tweets = self._load_processed()

        # Initialize Twitter API client if credentials available
        self.client = None
        if TWEEPY_AVAILABLE and config.TWITTER_BEARER_TOKEN:
            try:
                self.client = tweepy.Client(
                    bearer_token=config.TWITTER_BEARER_TOKEN,
                    consumer_key=config.TWITTER_API_KEY,
                    consumer_secret=config.TWITTER_API_SECRET,
                    access_token=config.TWITTER_ACCESS_TOKEN,
                    access_token_secret=config.TWITTER_ACCESS_SECRET
                )
                print("Twitter API client initialized successfully!")
            except Exception as e:
                print(f"Error initializing Twitter client: {e}")

    def _load_processed(self) -> set:
        """Load already processed tweet IDs"""
        if self.processed_file.exists():
            try:
                with open(self.processed_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('processed_ids', []))
            except (json.JSONDecodeError, FileNotFoundError):
                return set()
        return set()

    def _save_processed(self):
        """Save processed tweet IDs"""
        self.processed_file.parent.mkdir(exist_ok=True)
        with open(self.processed_file, 'w') as f:
            json.dump({
                'processed_ids': list(self.processed_tweets),
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)

    def post_tweet(self, text: str, in_reply_to: Optional[str] = None) -> bool:
        """
        Post a tweet

        Args:
            text: Tweet content (max 280 characters)
            in_reply_to: Tweet ID to reply to (optional)

        Returns:
            bool: Success status
        """
        if not self.client:
            print("ERROR: Twitter API client not initialized")
            self.audit_logger.log_action(
                action_type="twitter_post_failed",
                actor="twitter_integration",
                parameters={"reason": "client_not_initialized"},
                result="failure"
            )
            return False

        if len(text) > 280:
            print(f"ERROR: Tweet too long ({len(text)} chars, max 280)")
            self.audit_logger.log_action(
                action_type="twitter_post_failed",
                actor="twitter_integration",
                parameters={"reason": "too_long", "length": len(text)},
                result="failure"
            )
            return False

        try:
            if in_reply_to:
                response = self.client.create_tweet(
                    text=text,
                    in_reply_to_tweet_id=in_reply_to
                )
            else:
                response = self.client.create_tweet(text=text)

            tweet_id = response.data['id']

            print(f"Tweet posted successfully! ID: {tweet_id}")

            self.audit_logger.log_action(
                action_type="twitter_post",
                actor="twitter_integration",
                target=f"https://twitter.com/i/web/status/{tweet_id}",
                parameters={"text": text[:100]},
                approval_status="approved",
                approved_by="system",
                result="success"
            )

            return True

        except Exception as e:
            print(f"Error posting tweet: {e}")
            self.audit_logger.log_action(
                action_type="twitter_post_failed",
                actor="twitter_integration",
                parameters={"error": str(e)},
                result="failure"
            )
            return False

    def monitor_mentions(self) -> List[Dict]:
        """Monitor mentions of tracked users/hashtags"""
        if not self.client:
            print("Twitter API client not initialized - skipping monitoring")
            return []

        new_tweets = []

        try:
            # Search for tweets with tracked hashtags
            for hashtag in config.TRACK_HASHTAGS:
                query = f"{hashtag} -is:retweet"

                tweets = self.client.search_recent_tweets(
                    query=query,
                    max_results=10,
                    tweet_fields=['created_at', 'author_id', 'text']
                )

                if tweets.data:
                    for tweet in tweets.data:
                        if tweet.id not in self.processed_tweets:
                            new_tweets.append({
                                'id': tweet.id,
                                'text': tweet.text,
                                'created_at': str(tweet.created_at),
                                'hashtag': hashtag
                            })
                            self.processed_tweets.add(tweet.id)

        except Exception as e:
            print(f"Error monitoring Twitter: {e}")
            self.audit_logger.log_action(
                action_type="twitter_monitor_error",
                actor="twitter_integration",
                parameters={"error": str(e)},
                result="failure"
            )

        return new_tweets

    def create_task_from_tweet(self, tweet: Dict):
        """Create inbox task from interesting tweet"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Twitter_{tweet['hashtag'].replace('#', '')}_{timestamp}.md"
        filepath = self.inbox / filename

        content = f"""# Twitter Activity - {tweet['hashtag']}

## Type
Twitter - Relevant post detected

## Details
- **Hashtag:** {tweet['hashtag']}
- **Detected:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Tweet ID:** {tweet['id']}
- **Created:** {tweet['created_at']}

## Tweet Content
{tweet['text']}

## Suggested Actions
- [ ] Review tweet content
- [ ] Consider engaging (like/reply/retweet)
- [ ] Monitor conversation
- [ ] Add to content ideas if relevant

## Status
- [ ] Review
- [ ] Take action
- [ ] Mark complete

## Generated
{datetime.now().isoformat()}
"""

        filepath.write_text(content, encoding='utf-8')

        print(f"Created task: {filename}")

        self.audit_logger.log_action(
            action_type="twitter_task_created",
            actor="twitter_integration",
            target=filename,
            parameters={"hashtag": tweet['hashtag']},
            result="success"
        )


def main():
    """Main monitoring loop"""
    print("=" * 60)
    print("Twitter/X Integration - AI Employee")
    print("=" * 60)
    print(f"Monitoring hashtags: {', '.join(config.TRACK_HASHTAGS)}")
    print(f"Check interval: {config.CHECK_INTERVAL} seconds")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    twitter = TwitterIntegration(config.VAULT_PATH)

    if not twitter.client:
        print("\n⚠️  WARNING: Twitter API not configured!")
        print("Please update twitter_config.py with your API credentials")
        print("Get credentials from: https://developer.twitter.com/")
        return

    try:
        iteration = 0
        while True:
            iteration += 1
            print(f"\n[Check #{iteration}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Monitor for new tweets
            new_tweets = twitter.monitor_mentions()

            if new_tweets:
                print(f"Found {len(new_tweets)} new relevant tweets!")
                for tweet in new_tweets:
                    twitter.create_task_from_tweet(tweet)
            else:
                print("No new relevant tweets")

            # Save processed IDs
            twitter._save_processed()

            # Wait before next check
            time.sleep(config.CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n\nTwitter monitoring stopped.")
        twitter._save_processed()


if __name__ == "__main__":
    main()
