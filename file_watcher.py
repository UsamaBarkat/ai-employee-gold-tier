"""
File System Watcher for AI Employee
Monitors Watch_Folder and creates tasks in Obsidian vault when new files appear
"""

import time
import os
from datetime import datetime
from pathlib import Path

# Configuration
WATCH_FOLDER = r"E:\AI-300\My_Hackathons_Teacher\Watch_Folder"
INBOX_FOLDER = r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault\Inbox"

# Track processed files
processed_files = set()

def create_task_in_inbox(filename):
    """Create a new task file in the Inbox folder"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    task_name = f"Process_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    task_path = os.path.join(INBOX_FOLDER, task_name)

    # Create task content
    task_content = f"""# Task: Process New File

## File Information
- **Filename:** {filename}
- **Detected:** {timestamp}
- **Location:** Watch_Folder

## Status
- [ ] Review file
- [ ] Take appropriate action
- [ ] Move to Done when complete

## Notes
Add your notes here...
"""

    # Write task to Inbox
    with open(task_path, 'w', encoding='utf-8') as f:
        f.write(task_content)

    print(f"✅ Created task: {task_name}")

def watch_folder():
    """Main watcher loop"""
    print(f"🔍 Watching folder: {WATCH_FOLDER}")
    print("Drop files into Watch_Folder to create tasks...")
    print("Press Ctrl+C to stop\n")

    while True:
        try:
            # Get current files in watch folder
            current_files = set(os.listdir(WATCH_FOLDER))

            # Find new files
            new_files = current_files - processed_files

            # Process new files
            for filename in new_files:
                file_path = os.path.join(WATCH_FOLDER, filename)

                # Skip directories
                if os.path.isfile(file_path):
                    print(f"📁 New file detected: {filename}")
                    create_task_in_inbox(filename)
                    processed_files.add(filename)

            # Wait before checking again
            time.sleep(2)  # Check every 2 seconds

        except KeyboardInterrupt:
            print("\n\n👋 Watcher stopped by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    # Create folders if they don't exist
    os.makedirs(WATCH_FOLDER, exist_ok=True)
    os.makedirs(INBOX_FOLDER, exist_ok=True)

    # Start watching
    watch_folder()
