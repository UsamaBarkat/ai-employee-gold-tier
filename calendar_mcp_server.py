"""
Calendar/Reminder MCP Server for AI Employee
Gold Tier Feature - Manage calendar events and reminders
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from audit_logger import AuditLogger

class CalendarServer:
    """Simple calendar and reminder system"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.calendar_dir = self.vault_path / 'calendar'
        self.calendar_dir.mkdir(exist_ok=True)

        self.events_file = self.calendar_dir / 'events.json'
        self.reminders_file = self.calendar_dir / 'reminders.json'

        self.audit_logger = AuditLogger(str(vault_path))

        # Load existing events and reminders
        self.events = self._load_json(self.events_file)
        self.reminders = self._load_json(self.reminders_file)

    def _load_json(self, filepath: Path) -> list:
        """Load JSON file"""
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def _save_json(self, filepath: Path, data: list):
        """Save JSON file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_event(
        self,
        title: str,
        date: str,
        time: str = None,
        duration_minutes: int = 60,
        description: str = "",
        location: str = "",
        reminder_minutes_before: int = None
    ) -> Dict:
        """
        Add calendar event

        Args:
            title: Event title
            date: Date in YYYY-MM-DD format
            time: Time in HH:MM format (optional)
            duration_minutes: Event duration
            description: Event details
            location: Event location (URL or physical)
            reminder_minutes_before: Set reminder N minutes before

        Returns:
            Dict: Created event
        """
        event_id = f"evt_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        event = {
            'id': event_id,
            'title': title,
            'date': date,
            'time': time,
            'duration_minutes': duration_minutes,
            'description': description,
            'location': location,
            'created_at': datetime.now().isoformat(),
            'status': 'scheduled'
        }

        self.events.append(event)
        self._save_json(self.events_file, self.events)

        # Create reminder if requested
        if reminder_minutes_before:
            self.add_reminder(
                title=f"Reminder: {title}",
                datetime_str=f"{date} {time if time else '09:00'}",
                advance_minutes=reminder_minutes_before,
                related_event_id=event_id
            )

        print(f"Event created: {title} on {date}")

        self.audit_logger.log_action(
            action_type="calendar_event_created",
            actor="calendar_server",
            target=title,
            parameters={
                'date': date,
                'time': time,
                'event_id': event_id
            },
            result="success"
        )

        return event

    def add_reminder(
        self,
        title: str,
        datetime_str: str,
        advance_minutes: int = 0,
        priority: str = "normal",
        related_event_id: str = None
    ) -> Dict:
        """
        Add reminder

        Args:
            title: Reminder title
            datetime_str: When to remind (YYYY-MM-DD HH:MM)
            advance_minutes: Remind N minutes before datetime
            priority: low, normal, high
            related_event_id: Link to event (optional)

        Returns:
            Dict: Created reminder
        """
        reminder_id = f"rem_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Calculate actual reminder time
        target_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        reminder_time = target_time - timedelta(minutes=advance_minutes)

        reminder = {
            'id': reminder_id,
            'title': title,
            'reminder_time': reminder_time.isoformat(),
            'target_time': target_time.isoformat(),
            'advance_minutes': advance_minutes,
            'priority': priority,
            'related_event_id': related_event_id,
            'created_at': datetime.now().isoformat(),
            'status': 'pending',
            'triggered': False
        }

        self.reminders.append(reminder)
        self._save_json(self.reminders_file, self.reminders)

        print(f"Reminder created: {title} at {reminder_time.strftime('%Y-%m-%d %H:%M')}")

        self.audit_logger.log_action(
            action_type="reminder_created",
            actor="calendar_server",
            target=title,
            parameters={
                'reminder_time': reminder_time.isoformat(),
                'priority': priority
            },
            result="success"
        )

        return reminder

    def get_upcoming_events(self, days_ahead: int = 7) -> List[Dict]:
        """Get events in next N days"""
        today = datetime.now().date()
        end_date = today + timedelta(days=days_ahead)

        upcoming = []
        for event in self.events:
            if event['status'] != 'cancelled':
                event_date = datetime.strptime(event['date'], "%Y-%m-%d").date()
                if today <= event_date <= end_date:
                    upcoming.append(event)

        # Sort by date
        upcoming.sort(key=lambda e: (e['date'], e['time'] or '00:00'))

        return upcoming

    def get_pending_reminders(self) -> List[Dict]:
        """Get reminders that should trigger"""
        now = datetime.now()
        pending = []

        for reminder in self.reminders:
            if reminder['status'] == 'pending' and not reminder['triggered']:
                reminder_time = datetime.fromisoformat(reminder['reminder_time'])
                if reminder_time <= now:
                    pending.append(reminder)

        return pending

    def trigger_reminder(self, reminder_id: str):
        """Mark reminder as triggered"""
        for reminder in self.reminders:
            if reminder['id'] == reminder_id:
                reminder['triggered'] = True
                reminder['triggered_at'] = datetime.now().isoformat()
                self._save_json(self.reminders_file, self.reminders)

                self.audit_logger.log_action(
                    action_type="reminder_triggered",
                    actor="calendar_server",
                    target=reminder['title'],
                    result="success"
                )
                break

    def check_reminders(self):
        """Check and display pending reminders"""
        pending = self.get_pending_reminders()

        if pending:
            print(f"\n{'='*60}")
            print(f"REMINDERS ({len(pending)} pending)")
            print(f"{'='*60}")

            for reminder in pending:
                priority_icon = {
                    'low': '  ',
                    'normal': ' ',
                    'high': ' '
                }.get(reminder['priority'], ' ')

                print(f"{priority_icon} {reminder['title']}")
                print(f"   Target time: {reminder['target_time']}")

                if reminder['related_event_id']:
                    # Find related event
                    for event in self.events:
                        if event['id'] == reminder['related_event_id']:
                            print(f"   Event: {event['title']}")
                            if event['location']:
                                print(f"   Location: {event['location']}")
                            break

                print()

                # Mark as triggered
                self.trigger_reminder(reminder['id'])

            print(f"{'='*60}\n")

        return pending


# Example usage
if __name__ == "__main__":
    vault = r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault"
    calendar = CalendarServer(vault)

    print("Testing Calendar/Reminder Server...\n")

    # Add test event
    event = calendar.add_event(
        title="Wednesday Research Meeting",
        date="2026-03-12",
        time="22:00",
        duration_minutes=90,
        description="Panaversity Hackathon Weekly Meeting",
        location="https://us06web.zoom.us/j/87188707642",
        reminder_minutes_before=60  # Remind 1 hour before
    )

    # Add standalone reminder
    reminder = calendar.add_reminder(
        title="Check LinkedIn notifications",
        datetime_str="2026-03-11 10:00",
        advance_minutes=0,
        priority="normal"
    )

    # Check upcoming events
    print("\nUpcoming events (next 7 days):")
    upcoming = calendar.get_upcoming_events(days_ahead=7)
    for evt in upcoming:
        print(f"  - {evt['date']} {evt['time']}: {evt['title']}")

    # Check pending reminders
    print("\nChecking for pending reminders...")
    calendar.check_reminders()

    print("\nCalendar/Reminder server test complete!")
