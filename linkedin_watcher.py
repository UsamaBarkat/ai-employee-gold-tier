"""
LinkedIn Watcher - Silver Tier Feature
Monitors LinkedIn for:
1. Posts from people you follow (max 5/day)
2. Posts from Panaversity teachers
3. Comments on your posts
4. Connection requests

Usage: python linkedin_watcher.py [--test]

Author: Usama (Panaversity Student)
Hackathon: Personal AI Employee Hackathon 0
"""

import time
import json
import os
from datetime import datetime
from pathlib import Path

# Try importing required libraries
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("[ERROR] Selenium not installed. Run: pip install selenium webdriver-manager")
    exit(1)

# Import config
try:
    from linkedin_config import *
except ImportError:
    print("[ERROR] linkedin_config.py not found!")
    exit(1)


class LinkedInWatcher:
    """Monitors LinkedIn for configured activities"""

    def __init__(self):
        self.vault_path = Path(VAULT_PATH)
        self.inbox_path = Path(INBOX_PATH)
        self.driver = None
        self.logged_in = False
        self.posts_today = 0
        self.last_check_date = None

        # Track what we've already processed (to avoid duplicates)
        self.processed_items_file = self.vault_path / "linkedin_processed.json"
        self.processed_items = self.load_processed_items()

    def load_processed_items(self):
        """Load list of already processed items"""
        if self.processed_items_file.exists():
            with open(self.processed_items_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "posts": [],
            "comments": [],
            "connections": []
        }

    def save_processed_items(self):
        """Save processed items to avoid duplicates"""
        with open(self.processed_items_file, 'w', encoding='utf-8') as f:
            json.dump(self.processed_items, f, indent=2)

    def setup_browser(self):
        """Initialize Chrome browser with options"""
        print("[SETUP] Setting up browser...")

        chrome_options = Options()
        # Run in background (headless mode - no window)
        # chrome_options.add_argument("--headless")  # Uncomment for background mode
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        # Keep session data (stay logged in)
        user_data_dir = Path.home() / ".linkedin_watcher_session"
        chrome_options.add_argument(f"user-data-dir={user_data_dir}")

        try:
            # Auto-install ChromeDriver using webdriver-manager
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("[SUCCESS] Browser ready!")
            return True
        except Exception as e:
            print(f"[ERROR] Error setting up browser: {e}")
            print("[INFO] Make sure Chrome browser is installed!")
            return False

    def login(self):
        """Login to LinkedIn"""
        if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
            print("[WARNING] LinkedIn credentials not set in linkedin_config.py")
            print("[INFO] Please add your email and password to the config file")
            return False

        print("[LOGIN] Logging into LinkedIn...")

        try:
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(2)

            # Check if already logged in
            if "feed" in self.driver.current_url:
                print("[SUCCESS] Already logged in!")
                self.logged_in = True
                return True

            # Enter email
            email_field = self.driver.find_element(By.ID, "username")
            email_field.send_keys(LINKEDIN_EMAIL)

            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(LINKEDIN_PASSWORD)

            # Click login
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()

            # Wait for login
            time.sleep(5)

            # Check if login successful
            if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                print("[SUCCESS] Login successful!")
                self.logged_in = True
                return True
            else:
                print("[ERROR] Login failed. Please check credentials.")
                return False

        except Exception as e:
            print(f"[ERROR] Login error: {e}")
            return False

    def check_connection_requests(self):
        """Check for new connection requests"""
        print("[CHECK] Checking connection requests...")

        try:
            self.driver.get("https://www.linkedin.com/mynetwork/invitation-manager/")
            time.sleep(3)

            # Find invitation cards
            invitations = self.driver.find_elements(By.CSS_SELECTOR, ".invitation-card")

            new_requests = 0
            for invitation in invitations[:10]:  # Check first 10
                try:
                    # Get name
                    name_element = invitation.find_element(By.CSS_SELECTOR, ".invitation-card__name")
                    name = name_element.text.strip()

                    # Get headline/title
                    try:
                        headline_element = invitation.find_element(By.CSS_SELECTOR, ".invitation-card__occupation")
                        headline = headline_element.text.strip()
                    except:
                        headline = "No headline"

                    # Create unique ID
                    connection_id = f"connection_{name}_{headline}"

                    # Skip if already processed
                    if connection_id in self.processed_items["connections"]:
                        continue

                    # Create task
                    self.create_task(
                        task_type="connection_request",
                        title=f"Connection Request from {name}",
                        content={
                            "name": name,
                            "headline": headline,
                            "link": "https://www.linkedin.com/mynetwork/invitation-manager/"
                        }
                    )

                    # Mark as processed
                    self.processed_items["connections"].append(connection_id)
                    new_requests += 1

                except Exception as e:
                    continue

            if new_requests > 0:
                print(f"[SUCCESS] Found {new_requests} new connection request(s)")
            else:
                print("[INFO] No new connection requests")

            return new_requests

        except Exception as e:
            print(f"[ERROR] Error checking connections: {e}")
            return 0

    def check_own_posts(self):
        """Check your own recent posts for tracked hashtags"""
        print("[CHECK] Checking your recent posts...")

        try:
            # Go to your profile's recent activity
            profile_url = f"https://www.linkedin.com/in/{LINKEDIN_PROFILE}/recent-activity/all/"
            self.driver.get(profile_url)
            print(f"[DEBUG] Loading: {profile_url}")

            # Wait for content
            time.sleep(5)

            # Scroll to load posts
            for i in range(2):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            # Try to find your posts
            selectors = [
                ".profile-creator-shared-feed-update__container",
                ".feed-shared-update-v2",
                "li.profile-creator-shared-feed-update__container"
            ]

            posts = []
            for selector in selectors:
                posts = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if posts:
                    print(f"[DEBUG] Found {len(posts)} of your posts using: {selector}")
                    break

            if not posts:
                print("[DEBUG] No posts found on your profile")
                return 0

            new_posts = 0
            for post in posts[:5]:  # Check your last 5 posts
                try:
                    # Try to click "see more" button if it exists
                    try:
                        see_more = post.find_element(By.CSS_SELECTOR, ".feed-shared-inline-show-more-text__see-more-less-toggle, button[aria-label*='more']")
                        see_more.click()
                        time.sleep(1)  # Wait longer for content to expand
                        print("[DEBUG] Clicked 'see more' button")
                    except:
                        pass  # No "see more" button

                    # Get post text AFTER clicking "see more" (FULL TEXT - don't truncate!)
                    post_text_element = post.find_element(By.CSS_SELECTOR, ".feed-shared-text, .break-words")
                    post_text_full = post_text_element.text.strip()
                    post_text_preview = post_text_full[:200]  # Preview for saving

                    try:
                        print(f"[DEBUG] Checking your post: {post_text_full[:50].encode('ascii', 'ignore').decode()}...")
                        print(f"[DEBUG] Full text length: {len(post_text_full)} chars")
                        print(f"[DEBUG] Text contains '#': {('#' in post_text_full)}")
                    except:
                        print(f"[DEBUG] Checking your post...")

                    # Check if contains tracked hashtags (check FULL text!)
                    has_hashtag = any(tag.lower() in post_text_full.lower()
                                     for tag in WATCH_CONFIG["track_hashtags"])

                    print(f"[DEBUG] Has tracked hashtag: {has_hashtag}")
                    if not has_hashtag and '#' in post_text_full:
                        # Show what hashtags are actually in the post
                        import re
                        found_hashtags = re.findall(r'#\w+', post_text_full)
                        print(f"[DEBUG] Found these hashtags: {found_hashtags}")

                    if not has_hashtag:
                        continue

                    # Create unique ID
                    post_id = f"own_post_{post_text_full[:50]}"

                    # Skip if already processed
                    if post_id in self.processed_items["posts"]:
                        print(f"[DEBUG] Already processed this post")
                        continue

                    # Create task for your own post
                    self.create_task(
                        task_type="linkedin_own_post",
                        title=f"Your LinkedIn post with tracked hashtags",
                        content={
                            "author": "You (Usama)",
                            "text": post_text_preview,  # Save first 200 chars for readability
                            "full_text": post_text_full,  # Save full text too
                            "hashtags": [tag for tag in WATCH_CONFIG["track_hashtags"]
                                        if tag.lower() in post_text_full.lower()]
                        }
                    )

                    # Mark as processed
                    self.processed_items["posts"].append(post_id)
                    new_posts += 1

                except Exception as e:
                    print(f"[DEBUG] Error processing post: {e}")
                    continue

            if new_posts > 0:
                print(f"[SUCCESS] Found {new_posts} of your post(s) with tracked hashtags!")
            else:
                print("[INFO] No new posts with tracked hashtags")

            return new_posts

        except Exception as e:
            print(f"[ERROR] Error checking your posts: {e}")
            return 0

    def check_feed_posts(self):
        """Check feed for posts from people you follow"""
        print("[CHECK] Checking feed posts...")

        # Reset daily counter if new day
        today = datetime.now().date()
        if self.last_check_date != today:
            self.posts_today = 0
            self.last_check_date = today

        # Check if reached daily limit
        if self.posts_today >= WATCH_CONFIG["max_posts_per_day"]:
            print(f"[INFO] Daily limit reached ({WATCH_CONFIG['max_posts_per_day']} posts)")
            return 0

        try:
            self.driver.get("https://www.linkedin.com/feed/")
            print("[DEBUG] Waiting for feed to load...")

            # Wait for feed container to be present
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "main"))
                )
                print("[DEBUG] Main container loaded")
            except TimeoutException:
                print("[ERROR] Feed container didn't load")
                return 0

            time.sleep(5)  # Additional wait for content

            # Scroll to load posts (scroll multiple times to load more)
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            # Try multiple ways to find posts
            selectors = [
                ".feed-shared-update-v2",
                "[data-id^='urn:li:activity']",
                "div[data-urn]",
                ".scaffold-finite-scroll__content > div",
                "div.feed-shared-update-v2__content"
            ]

            posts = []
            for selector in selectors:
                posts = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if posts:
                    print(f"[DEBUG] Found {len(posts)} posts using selector: {selector}")
                    break

            if not posts:
                print("[DEBUG] No posts found with any selector!")
                # DEBUG: Save page source
                with open("linkedin_feed_debug.html", "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
                print("[DEBUG] Saved page source to linkedin_feed_debug.html")

            new_posts = 0
            for post in posts[:20]:  # Check first 20 posts
                if self.posts_today >= WATCH_CONFIG["max_posts_per_day"]:
                    break

                try:
                    # Get post text
                    post_text_element = post.find_element(By.CSS_SELECTOR, ".feed-shared-text")
                    post_text = post_text_element.text.strip()[:200]  # First 200 chars

                    # Get author name
                    try:
                        author_element = post.find_element(By.CSS_SELECTOR, ".feed-shared-actor__name")
                        author = author_element.text.strip()
                    except:
                        author = "Unknown"

                    print(f"[DEBUG] Checking post by {author}: {post_text[:50]}...")

                    # Check if post contains tracked hashtags
                    has_hashtag = any(tag.lower() in post_text.lower()
                                     for tag in WATCH_CONFIG["track_hashtags"])

                    # Check if from specific user
                    is_specific_user = any(user.lower() in author.lower()
                                          for user in WATCH_CONFIG["track_specific_users"])

                    print(f"[DEBUG] Has hashtag: {has_hashtag}, Is specific user: {is_specific_user}")

                    # Only create task if relevant (has hashtag OR from specific user)
                    # Note: This INCLUDES your own posts if they have the hashtags!
                    if not (has_hashtag or is_specific_user):
                        continue

                    # Create unique ID
                    post_id = f"post_{author}_{post_text[:50]}"

                    # Skip if already processed
                    if post_id in self.processed_items["posts"]:
                        continue

                    # Create task
                    self.create_task(
                        task_type="linkedin_post",
                        title=f"New post from {author}",
                        content={
                            "author": author,
                            "text": post_text,
                            "hashtags": [tag for tag in WATCH_CONFIG["track_hashtags"]
                                        if tag.lower() in post_text.lower()]
                        }
                    )

                    # Mark as processed
                    self.processed_items["posts"].append(post_id)
                    self.posts_today += 1
                    new_posts += 1

                except Exception as e:
                    continue

            if new_posts > 0:
                print(f"[SUCCESS] Found {new_posts} new relevant post(s)")
            else:
                print("[INFO] No new relevant posts")

            return new_posts

        except Exception as e:
            print(f"[ERROR] Error checking feed: {e}")
            return 0

    def check_my_post_comments(self):
        """Check for comments on your posts"""
        print("[INFO] Checking comments on your posts...")

        try:
            # Go to your profile posts
            self.driver.get("https://www.linkedin.com/in/me/recent-activity/all/")
            time.sleep(3)

            # This is a simplified version
            # Full implementation would check each post for new comments
            print("[INFO] Comment checking requires individual post URLs")
            print("[TIP] We'll implement full version after basic features work")

            return 0

        except Exception as e:
            print(f"[ERROR] Error checking comments: {e}")
            return 0

    def create_task(self, task_type, title, content):
        """Create a task file in the inbox"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"LinkedIn_{task_type}_{timestamp}.md"
        filepath = self.inbox_path / filename

        task_content = f"""# {title}

## Type
LinkedIn - {task_type.replace('_', ' ').title()}

## Details
"""

        for key, value in content.items():
            if isinstance(value, list):
                task_content += f"- **{key.title()}:** {', '.join(value)}\n"
            else:
                task_content += f"- **{key.title()}:** {value}\n"

        task_content += f"""

## Status
- [ ] Review
- [ ] Take action
- [ ] Mark complete

## Detected
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Notes
Add your notes here...
"""

        # Write task file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(task_content)

        print(f"[SUCCESS] Created task: {filename}")

    def run_check(self):
        """Run one check cycle"""
        print("\n" + "="*60)
        print(f"[CHECK] LinkedIn Watcher - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

        if not self.logged_in:
            if not self.login():
                return False

        total_new = 0

        # Check connection requests
        if WATCH_CONFIG["watch_connection_requests"]:
            total_new += self.check_connection_requests()

        # Check YOUR OWN recent posts first (more reliable!)
        total_new += self.check_own_posts()

        # Check feed posts
        if WATCH_CONFIG["watch_feed_posts"]:
            total_new += self.check_feed_posts()

        # Check comments on your posts
        if WATCH_CONFIG["watch_my_post_comments"]:
            total_new += self.check_my_post_comments()

        # Save processed items
        self.save_processed_items()

        print(f"\n[SUMMARY] {total_new} new task(s) created")
        print("="*60)

        return True

    def start(self):
        """Start the watcher (continuous monitoring)"""
        print("[START] Starting LinkedIn Watcher...")
        print(f"[INFO] Check interval: {CHECK_INTERVAL} seconds")
        print("Press Ctrl+C to stop\n")

        if not self.setup_browser():
            return

        try:
            while True:
                self.run_check()
                print(f"[WAIT] Sleeping for {CHECK_INTERVAL} seconds...")
                time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n[STOP] Stopping LinkedIn Watcher...")
        finally:
            if self.driver:
                self.driver.quit()
            print("[SUCCESS] Watcher stopped")

    def test_run(self, auto_close=False):
        """Run one test check (for testing setup)"""
        print("[TEST] Running test check...")

        if not self.setup_browser():
            return False

        try:
            success = self.run_check()
            return success
        finally:
            if self.driver:
                if not auto_close:
                    input("\nPress Enter to close browser...")
                self.driver.quit()


if __name__ == "__main__":
    import sys

    print("=" * 58)
    print("       LinkedIn Watcher - Silver Tier Feature")
    print("                 Personal AI Employee")
    print("=" * 58)

    watcher = LinkedInWatcher()

    # Check for command line argument
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            print("\nRunning in TEST MODE (one check only)\n")
            watcher.test_run(auto_close=False)  # Don't auto-close so user can see
        elif sys.argv[1] == "--auto" or sys.argv[1] == "--continuous":
            print("\nRunning in CONTINUOUS MODE (automated)\n")
            print("[INFO] Watcher will run continuously and check every 5 minutes")
            print("[INFO] Press Ctrl+C to stop\n")
            watcher.start()
        else:
            print(f"\nUnknown flag: {sys.argv[1]}")
            print("Usage: python linkedin_watcher.py [--test | --auto]")
    else:
        # Ask user: test or continuous mode
        print("Choose mode:")
        print("1. Test run (one check only)")
        print("2. Continuous monitoring")
        try:
            choice = input("\nEnter choice (1 or 2): ").strip()
            if choice == "1":
                watcher.test_run()
            else:
                watcher.start()
        except EOFError:
            print("\nNo input detected. Use --test or --auto flag.")
            print("Example: python linkedin_watcher.py --auto")
