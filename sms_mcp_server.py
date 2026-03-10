"""
SMS/Notification MCP Server for AI Employee
Gold Tier Feature - Send SMS notifications (via email-to-SMS or Twilio)
"""

import smtplib
import json
from datetime import datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from audit_logger import AuditLogger

class SMSServer:
    """Simple SMS/Notification server using email-to-SMS gateways"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.audit_logger = AuditLogger(str(vault_path))
        self.logs_dir = self.vault_path / 'logs'
        self.logs_dir.mkdir(exist_ok=True)

        # Email-to-SMS gateways for major carriers
        self.carriers = {
            'verizon': '@vtext.com',
            'att': '@txt.att.net',
            'tmobile': '@tmomail.net',
            'sprint': '@messaging.sprintpcs.com',
            'boost': '@sms.myboostmobile.com',
            'cricket': '@mms.cricketwireless.net',
        }

    def send_sms_via_email(
        self,
        phone_number: str,
        carrier: str,
        message: str,
        smtp_email: str,
        smtp_password: str
    ) -> bool:
        """
        Send SMS via email-to-SMS gateway

        Args:
            phone_number: 10-digit phone number (e.g., "1234567890")
            carrier: Carrier name (verizon, att, tmobile, etc.)
            message: SMS message (keep under 160 chars for SMS)
            smtp_email: Gmail address for sending
            smtp_password: Gmail app password

        Returns:
            bool: Success status
        """
        if carrier.lower() not in self.carriers:
            print(f"ERROR: Unknown carrier '{carrier}'")
            print(f"Supported carriers: {', '.join(self.carriers.keys())}")
            self.audit_logger.log_action(
                action_type="sms_send_failed",
                actor="sms_server",
                target=phone_number,
                parameters={"reason": "unknown_carrier", "carrier": carrier},
                result="failure"
            )
            return False

        # Create email-to-SMS address
        sms_gateway = phone_number + self.carriers[carrier.lower()]

        # Truncate message if too long
        if len(message) > 160:
            message = message[:157] + "..."
            print("WARNING: Message truncated to 160 characters")

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = smtp_email
            msg['To'] = sms_gateway
            msg['Subject'] = ""  # SMS don't show subjects

            msg.attach(MIMEText(message, 'plain'))

            # Send via Gmail SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
            server.quit()

            print(f"SMS sent to {phone_number} via {carrier}")

            # Log success
            self.audit_logger.log_action(
                action_type="sms_send",
                actor="sms_server",
                target=f"{phone_number} ({carrier})",
                parameters={"message_length": len(message)},
                approval_status="approved",
                approved_by="system",
                result="success"
            )

            # Save to SMS log
            self._log_sms(phone_number, carrier, message, "sent")

            return True

        except Exception as e:
            print(f"Error sending SMS: {e}")
            self.audit_logger.log_action(
                action_type="sms_send_failed",
                actor="sms_server",
                target=phone_number,
                parameters={"error": str(e)},
                result="failure"
            )
            return False

    def send_notification(
        self,
        message: str,
        priority: str = "normal",
        smtp_email: str = None,
        smtp_password: str = None,
        phone_number: str = None,
        carrier: str = None
    ) -> bool:
        """
        Send a notification (SMS if configured, otherwise just log)

        Args:
            message: Notification message
            priority: low, normal, high, critical
            smtp_email, smtp_password: Email credentials (optional)
            phone_number, carrier: SMS details (optional)

        Returns:
            bool: Success status
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Format message with priority
        if priority in ['high', 'critical']:
            formatted_msg = f"[{priority.upper()}] {message}"
        else:
            formatted_msg = message

        # Try to send SMS if credentials provided
        if all([smtp_email, smtp_password, phone_number, carrier]):
            success = self.send_sms_via_email(
                phone_number, carrier, formatted_msg,
                smtp_email, smtp_password
            )
            if success:
                return True

        # Fallback: Log the notification
        print(f"[{timestamp}] NOTIFICATION ({priority}): {message}")

        self.audit_logger.log_action(
            action_type="notification",
            actor="sms_server",
            parameters={
                "message": message,
                "priority": priority,
                "method": "logged"
            },
            result="success"
        )

        self._log_notification(message, priority)
        return True

    def _log_sms(self, phone: str, carrier: str, message: str, status: str):
        """Log SMS to JSON file"""
        log_file = self.logs_dir / f"sms_log_{datetime.now().strftime('%Y%m')}.json"

        logs = []
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

        logs.append({
            'timestamp': datetime.now().isoformat(),
            'phone': phone,
            'carrier': carrier,
            'message': message,
            'status': status
        })

        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)

    def _log_notification(self, message: str, priority: str):
        """Log notification to file"""
        log_file = self.logs_dir / f"notifications_{datetime.now().strftime('%Y%m')}.json"

        logs = []
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

        logs.append({
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'priority': priority
        })

        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)


# Example usage
if __name__ == "__main__":
    vault = r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault"
    sms_server = SMSServer(vault)

    # Test notification (just logging)
    print("Testing notification system...")
    sms_server.send_notification(
        "Test notification from AI Employee",
        priority="normal"
    )

    # Test SMS (requires credentials - commented out for safety)
    # sms_server.send_sms_via_email(
    #     phone_number="1234567890",
    #     carrier="verizon",
    #     message="Test SMS from AI Employee!",
    #     smtp_email="your_email@gmail.com",
    #     smtp_password="your_app_password"
    # )

    print("\nSMS/Notification server test complete!")
    print("\nSupported carriers:")
    for carrier in sms_server.carriers.keys():
        print(f"  - {carrier}")
