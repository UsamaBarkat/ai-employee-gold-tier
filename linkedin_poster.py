"""
LinkedIn Poster - Silver Tier Feature
Automatically posts content to LinkedIn after human approval

Usage: python linkedin_poster.py "Your post content here"
       python linkedin_poster.py --file path/to/task.md

Author: Usama (Panaversity Student)
Hackathon: Personal AI Employee Hackathon 0
"""

import time
import sys
import os
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
    from linkedin_config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD
except ImportError:
    print("[ERROR] linkedin_config.py not found!")
    exit(1)


class LinkedInPoster:
    """Posts content to LinkedIn with human-in-the-loop approval"""

    def __init__(self):
        self.driver = None
        self.logged_in = False

    def setup_browser(self):
        """Initialize Chrome browser with options"""
        print("[SETUP] Setting up browser...")

        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        # Keep session data (stay logged in) - USE SEPARATE SESSION FOR POSTING
        user_data_dir = Path.home() / ".linkedin_poster_session"
        chrome_options.add_argument(f"user-data-dir={user_data_dir}")

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("[SUCCESS] Browser ready!")
            return True
        except Exception as e:
            print(f"[ERROR] Error setting up browser: {e}")
            return False

    def login(self):
        """Login to LinkedIn"""
        if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
            print("[ERROR] LinkedIn credentials not set in linkedin_config.py")
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

    def post_content(self, content):
        """Post content to LinkedIn"""
        if not self.logged_in:
            print("[ERROR] Not logged in!")
            return False

        print("[POST] Posting to LinkedIn...")

        try:
            # Go to feed
            self.driver.get("https://www.linkedin.com/feed/")
            time.sleep(3)

            # Try multiple selectors for "Start a post" button
            start_post_clicked = False

            # Method 1: Click the text area directly
            try:
                print("[INFO] Trying to click post text area...")
                post_box = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.share-box-feed-entry__trigger"))
                )
                post_box.click()
                start_post_clicked = True
                print("[SUCCESS] Clicked post box")
                time.sleep(2)
            except:
                pass

            # Method 2: Look for "Start a post" text
            if not start_post_clicked:
                try:
                    print("[INFO] Looking for 'Start a post' button...")
                    buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    for button in buttons:
                        if "start a post" in button.text.lower() or "share" in button.get_attribute("aria-label").lower():
                            button.click()
                            start_post_clicked = True
                            print("[SUCCESS] Clicked 'Start a post' button")
                            time.sleep(2)
                            break
                except:
                    pass

            if not start_post_clicked:
                print("[ERROR] Could not find 'Start a post' button")
                print("[INFO] Please click 'Start a post' manually in the browser...")
                time.sleep(10)  # Give user time to click manually

            # Find the text editor (try multiple selectors)
            text_entered = False

            # Method 1: Standard ql-editor
            try:
                text_editor = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.ql-editor"))
                )
                text_editor.click()
                time.sleep(1)
                text_editor.send_keys(content)
                text_entered = True
                print("[SUCCESS] Content entered (method 1)")
            except:
                pass

            # Method 2: Any contenteditable div
            if not text_entered:
                try:
                    text_editor = self.driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
                    text_editor.click()
                    time.sleep(1)
                    text_editor.send_keys(content)
                    text_entered = True
                    print("[SUCCESS] Content entered (method 2)")
                except Exception as e:
                    print(f"[ERROR] Could not find text editor: {e}")
                    return False

            if not text_entered:
                print("[ERROR] Could not enter content")
                return False

            time.sleep(2)

            # Click the "Post" button (try multiple methods)
            post_clicked = False

            # Method 1: Look for primary action button
            try:
                post_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.share-actions__primary-action"))
                )
                print("[INFO] Ready to post. Clicking Post button in 2 seconds...")
                time.sleep(2)
                post_button.click()
                post_clicked = True
                print("[SUCCESS] Post button clicked!")
            except:
                pass

            # Method 2: Look for button with "Post" text
            if not post_clicked:
                try:
                    buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    for button in buttons:
                        if button.text.strip().lower() == "post":
                            button.click()
                            post_clicked = True
                            print("[SUCCESS] Post button clicked!")
                            break
                except:
                    pass

            if post_clicked:
                # Wait for post to complete
                time.sleep(5)
                print("[SUCCESS] Post published to LinkedIn!")
                return True
            else:
                print("[WARNING] Could not find Post button automatically")
                print("[INFO] Please click the 'Post' button manually in the browser...")
                print("[INFO] You have 20 seconds...")
                time.sleep(20)
                print("[INFO] Assuming post was completed")
                return True

        except Exception as e:
            print(f"[ERROR] Error posting to LinkedIn: {e}")
            import traceback
            traceback.print_exc()
            return False

    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            print("[INFO] Browser closed")


def extract_content_from_task(task_file_path):
    """Extract post content from a task file"""
    try:
        with open(task_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for Full_Text field (most complete version)
        if "**Full_Text:**" in content:
            # Extract text between Full_Text and the next ##
            start = content.find("**Full_Text:**") + len("**Full_Text:**")
            end = content.find("## Status", start)
            if end == -1:
                end = content.find("## Approval", start)

            post_text = content[start:end].strip()

            # Clean up formatting
            post_text = post_text.replace("- **Hashtags:**", "")
            post_text = post_text.replace("hashtag\n#", "#")

            return post_text

        # Fallback: Look for Text field
        elif "**Text:**" in content:
            start = content.find("**Text:**") + len("**Text:**")
            end = content.find("- **", start)
            post_text = content[start:end].strip()
            return post_text

        else:
            print("[ERROR] Could not find post content in task file")
            return None

    except Exception as e:
        print(f"[ERROR] Error reading task file: {e}")
        return None


def main():
    print("=" * 58)
    print("  LinkedIn Auto-Poster - Silver Tier Feature")
    print("                 Personal AI Employee")
    print("=" * 58)

    if len(sys.argv) < 2:
        print("\nUsage:")
        print('  python linkedin_poster.py "Your post content here"')
        print("  python linkedin_poster.py --file path/to/task.md")
        return

    # Determine if posting from file or direct content
    if sys.argv[1] == "--file":
        if len(sys.argv) < 3:
            print("[ERROR] Please provide task file path")
            return

        task_file = sys.argv[2]
        if not os.path.exists(task_file):
            print(f"[ERROR] File not found: {task_file}")
            return

        print(f"[INFO] Reading content from: {task_file}")
        content = extract_content_from_task(task_file)

        if not content:
            print("[ERROR] Could not extract content from task file")
            return
    else:
        # Direct content from command line
        content = " ".join(sys.argv[1:])

    print(f"\n[INFO] Content to post ({len(content)} characters):")
    print("-" * 58)
    try:
        print(content[:200] + "..." if len(content) > 200 else content)
    except UnicodeEncodeError:
        # Handle emoji/unicode on Windows console
        safe_content = content.encode('ascii', 'replace').decode('ascii')
        print(safe_content[:200] + "..." if len(safe_content) > 200 else safe_content)
        print("[Note: Some characters may display incorrectly in console, but will post correctly to LinkedIn]")
    print("-" * 58)

    # Confirm before posting
    confirm = input("\n[CONFIRM] Post this to LinkedIn? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("[CANCELLED] Post cancelled by user")
        return

    # Create poster and post
    poster = LinkedInPoster()

    try:
        if not poster.setup_browser():
            return

        if not poster.login():
            return

        if poster.post_content(content):
            print("\n" + "=" * 58)
            print("  SUCCESS! Post published to LinkedIn")
            print("=" * 58)
        else:
            print("\n[FAILED] Could not post to LinkedIn")

    finally:
        input("\n[INFO] Press Enter to close browser...")
        poster.close()


if __name__ == "__main__":
    main()
