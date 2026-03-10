"""
Facebook/Instagram Integration for AI Employee
Gold Tier Feature - Auto-post and monitor Facebook & Instagram
"""

import json
import time
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

from audit_logger import AuditLogger
import facebook_config as config


class FacebookInstagramIntegration:
    """Facebook and Instagram integration for posting and monitoring"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / 'inbox'
        self.processed_file = Path(config.PROCESSED_POSTS_FILE)
        self.audit_logger = AuditLogger(str(vault_path))

        # Load processed posts
        self.processed_posts = self._load_processed()

        # Base URL for Facebook Graph API
        self.base_url = f"https://graph.facebook.com/{config.API_VERSION}"

        # Check if credentials are configured
        self.facebook_enabled = bool(config.FACEBOOK_ACCESS_TOKEN)
        self.instagram_enabled = bool(config.INSTAGRAM_BUSINESS_ACCOUNT_ID)

        if self.facebook_enabled:
            print("[OK] Facebook integration: ENABLED")
        else:
            print("[!] Facebook integration: NOT CONFIGURED")

        if self.instagram_enabled:
            print("[OK] Instagram integration: ENABLED")
        else:
            print("[!] Instagram integration: NOT CONFIGURED")

    def _load_processed(self) -> set:
        """Load already processed post IDs"""
        if self.processed_file.exists():
            try:
                with open(self.processed_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('processed_ids', []))
            except (json.JSONDecodeError, FileNotFoundError):
                return set()
        return set()

    def _save_processed(self):
        """Save processed post IDs"""
        self.processed_file.parent.mkdir(exist_ok=True)
        with open(self.processed_file, 'w') as f:
            json.dump({
                'processed_ids': list(self.processed_posts),
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)

    # ==================== FACEBOOK POSTING ====================

    def post_to_facebook(
        self,
        message: str,
        link: Optional[str] = None,
        image_path: Optional[str] = None
    ) -> bool:
        """
        Post to Facebook Page

        Args:
            message: Post text content
            link: Optional URL to share
            image_path: Optional path to image file

        Returns:
            bool: Success status
        """
        if not self.facebook_enabled or not config.ENABLE_FACEBOOK_POSTING:
            print("ERROR: Facebook posting not enabled")
            return False

        if len(message) > config.FACEBOOK_POST_MAX_LENGTH:
            print(f"ERROR: Post too long ({len(message)} chars)")
            return False

        try:
            # Post to Facebook Page
            url = f"{self.base_url}/{config.FACEBOOK_PAGE_ID}/feed"

            params = {
                'message': message,
                'access_token': config.FACEBOOK_PAGE_ACCESS_TOKEN
            }

            if link:
                params['link'] = link

            # If image provided, use photos endpoint instead
            if image_path:
                url = f"{self.base_url}/{config.FACEBOOK_PAGE_ID}/photos"
                with open(image_path, 'rb') as img:
                    files = {'source': img}
                    response = requests.post(url, data=params, files=files)
            else:
                response = requests.post(url, data=params)

            response.raise_for_status()
            result = response.json()

            post_id = result.get('id', 'unknown')
            post_url = f"https://facebook.com/{post_id}"

            print(f"[OK] Facebook post published! ID: {post_id}")

            self.audit_logger.log_action(
                action_type="facebook_post",
                actor="facebook_integration",
                target=post_url,
                parameters={"message_length": len(message)},
                approval_status="approved",
                approved_by="system",
                result="success"
            )

            return True

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error posting to Facebook: {e}")
            self.audit_logger.log_action(
                action_type="facebook_post_failed",
                actor="facebook_integration",
                parameters={"error": str(e)},
                result="failure"
            )
            return False

    # ==================== INSTAGRAM POSTING ====================

    def post_to_instagram(
        self,
        image_path: str,
        caption: str = "",
        hashtags: List[str] = None
    ) -> bool:
        """
        Post to Instagram (requires image)

        Args:
            image_path: Path to image file (REQUIRED for Instagram)
            caption: Post caption
            hashtags: List of hashtags (without # symbol)

        Returns:
            bool: Success status
        """
        if not self.instagram_enabled or not config.ENABLE_INSTAGRAM_POSTING:
            print("ERROR: Instagram posting not enabled")
            return False

        # Instagram requires an image
        if not image_path or not Path(image_path).exists():
            print("ERROR: Instagram requires an image file")
            return False

        # Build caption with hashtags
        full_caption = caption

        if hashtags:
            # Limit hashtags
            hashtags = hashtags[:config.INSTAGRAM_HASHTAG_MAX]
            hashtag_str = " ".join([f"#{tag}" for tag in hashtags])
            full_caption = f"{caption}\n\n{hashtag_str}"

        # Check caption length
        if len(full_caption) > config.INSTAGRAM_CAPTION_MAX_LENGTH:
            print(f"WARNING: Caption too long, truncating...")
            full_caption = full_caption[:config.INSTAGRAM_CAPTION_MAX_LENGTH - 3] + "..."

        try:
            # Step 1: Create media container
            create_url = f"{self.base_url}/{config.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media"

            # Upload image and get URL (you need to host the image somewhere accessible)
            # For simplicity, assuming image_path is already a URL
            # In production, you'd upload to a CDN or Facebook's hosting

            create_params = {
                'image_url': image_path,  # Must be publicly accessible URL
                'caption': full_caption,
                'access_token': config.FACEBOOK_PAGE_ACCESS_TOKEN
            }

            create_response = requests.post(create_url, data=create_params)
            create_response.raise_for_status()
            creation_id = create_response.json()['id']

            print(f"[OK] Instagram media created: {creation_id}")

            # Step 2: Publish the media container
            publish_url = f"{self.base_url}/{config.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish"

            publish_params = {
                'creation_id': creation_id,
                'access_token': config.FACEBOOK_PAGE_ACCESS_TOKEN
            }

            publish_response = requests.post(publish_url, data=publish_params)
            publish_response.raise_for_status()
            post_id = publish_response.json()['id']

            print(f"[OK] Instagram post published! ID: {post_id}")

            self.audit_logger.log_action(
                action_type="instagram_post",
                actor="instagram_integration",
                target=f"https://instagram.com/p/{post_id}",
                parameters={
                    "caption_length": len(full_caption),
                    "hashtags_count": len(hashtags) if hashtags else 0
                },
                approval_status="approved",
                approved_by="system",
                result="success"
            )

            return True

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error posting to Instagram: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")

            self.audit_logger.log_action(
                action_type="instagram_post_failed",
                actor="instagram_integration",
                parameters={"error": str(e)},
                result="failure"
            )
            return False

    # ==================== MONITORING ====================

    def monitor_facebook_page(self) -> List[Dict]:
        """Monitor Facebook Page posts"""
        if not self.facebook_enabled:
            return []

        new_posts = []

        try:
            # Get recent posts from Facebook Page
            url = f"{self.base_url}/{config.FACEBOOK_PAGE_ID}/posts"
            params = {
                'access_token': config.FACEBOOK_PAGE_ACCESS_TOKEN,
                'fields': 'id,message,created_time,permalink_url',
                'limit': config.MAX_POSTS_PER_CHECK
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            for post in data.get('data', []):
                post_id = post['id']

                if post_id not in self.processed_posts:
                    message = post.get('message', '')

                    # Check if contains tracked hashtags
                    has_tracked_hashtag = any(
                        f"#{tag}" in message or tag in message
                        for tag in config.TRACK_HASHTAGS
                    )

                    if has_tracked_hashtag:
                        new_posts.append({
                            'id': post_id,
                            'message': message,
                            'created_time': post['created_time'],
                            'url': post.get('permalink_url', ''),
                            'platform': 'facebook'
                        })
                        self.processed_posts.add(post_id)

        except Exception as e:
            print(f"Error monitoring Facebook: {e}")

        return new_posts

    def monitor_instagram_account(self) -> List[Dict]:
        """Monitor Instagram Business Account posts"""
        if not self.instagram_enabled:
            return []

        new_posts = []

        try:
            # Get recent posts from Instagram Business Account
            url = f"{self.base_url}/{config.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media"
            params = {
                'access_token': config.FACEBOOK_PAGE_ACCESS_TOKEN,
                'fields': 'id,caption,timestamp,permalink',
                'limit': config.MAX_POSTS_PER_CHECK
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            for post in data.get('data', []):
                post_id = post['id']

                if post_id not in self.processed_posts:
                    caption = post.get('caption', '')

                    # Check if contains tracked hashtags
                    has_tracked_hashtag = any(
                        f"#{tag}" in caption or tag in caption
                        for tag in config.TRACK_HASHTAGS
                    )

                    if has_tracked_hashtag:
                        new_posts.append({
                            'id': post_id,
                            'caption': caption,
                            'timestamp': post['timestamp'],
                            'url': post.get('permalink', ''),
                            'platform': 'instagram'
                        })
                        self.processed_posts.add(post_id)

        except Exception as e:
            print(f"Error monitoring Instagram: {e}")

        return new_posts

    def create_task_from_post(self, post: Dict):
        """Create inbox task from social media post"""
        platform = post['platform'].capitalize()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{platform}_post_{timestamp}.md"
        filepath = self.inbox / filename

        content_field = 'caption' if platform == 'Instagram' else 'message'
        content = post.get(content_field, '')

        content_md = f"""# {platform} Activity - Relevant Post

## Type
{platform} - Post with tracked hashtag

## Details
- **Platform:** {platform}
- **Detected:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Post ID:** {post['id']}
- **URL:** {post.get('url', 'N/A')}

## Post Content
{content}

## Suggested Actions
- [ ] Review post content
- [ ] Consider engaging (like/comment/share)
- [ ] Monitor conversation
- [ ] Add to content ideas if relevant

## Status
- [ ] Review
- [ ] Take action
- [ ] Mark complete

## Generated
{datetime.now().isoformat()}
"""

        filepath.write_text(content_md, encoding='utf-8')
        print(f"[OK] Created task: {filename}")

        self.audit_logger.log_action(
            action_type=f"{platform.lower()}_task_created",
            actor=f"{platform.lower()}_integration",
            target=filename,
            parameters={"platform": platform},
            result="success"
        )

    def generate_summary(self) -> Dict:
        """Generate summary of Facebook/Instagram activity"""
        return {
            'facebook_enabled': self.facebook_enabled,
            'instagram_enabled': self.instagram_enabled,
            'total_processed': len(self.processed_posts),
            'last_updated': datetime.now().isoformat()
        }


def main():
    """Main monitoring loop"""
    print("=" * 60)
    print("Facebook/Instagram Integration - AI Employee")
    print("=" * 60)

    integration = FacebookInstagramIntegration(config.VAULT_PATH)

    if not integration.facebook_enabled and not integration.instagram_enabled:
        print("\n[WARNING] Neither Facebook nor Instagram configured!")
        print("Please update facebook_config.py with your credentials")
        print("\nSetup Guide:")
        print("1. Go to: https://developers.facebook.com/")
        print("2. Create a Facebook App")
        print("3. Get Access Tokens")
        print("4. Link Instagram Business Account")
        print("5. Update facebook_config.py")
        return

    print(f"\nMonitoring hashtags: {', '.join(config.TRACK_HASHTAGS)}")
    print(f"Check interval: {config.CHECK_INTERVAL} seconds")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    try:
        iteration = 0
        while True:
            iteration += 1
            print(f"\n[Check #{iteration}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            new_posts = []

            # Monitor Facebook
            if integration.facebook_enabled:
                fb_posts = integration.monitor_facebook_page()
                new_posts.extend(fb_posts)
                print(f"[Facebook] {len(fb_posts)} new relevant posts")

            # Monitor Instagram
            if integration.instagram_enabled:
                ig_posts = integration.monitor_instagram_account()
                new_posts.extend(ig_posts)
                print(f"[Instagram] {len(ig_posts)} new relevant posts")

            # Create tasks for new posts
            if new_posts:
                print(f"[OK] Total new posts: {len(new_posts)}")
                for post in new_posts:
                    integration.create_task_from_post(post)
            else:
                print("[OK] No new relevant posts")

            # Save processed IDs
            integration._save_processed()

            # Wait before next check
            time.sleep(config.CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n\nFacebook/Instagram monitoring stopped.")
        integration._save_processed()

        # Print summary
        summary = integration.generate_summary()
        print(f"\nSummary:")
        print(f"  - Total posts processed: {summary['total_processed']}")


if __name__ == "__main__":
    # Test with dummy data (since we don't have API credentials)
    print("Testing Facebook/Instagram Integration...")

    vault = r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault"
    integration = FacebookInstagramIntegration(vault)

    print("\n[OK] Integration system ready!")
    print("\n[SETUP] To activate:")
    print("1. Get Facebook Developer credentials")
    print("2. Link Instagram Business Account")
    print("3. Update facebook_config.py")
    print("4. Run: python facebook_instagram_integration.py")
