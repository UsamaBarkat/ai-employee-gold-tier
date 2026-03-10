"""
Email MCP Server - Silver Tier Feature
Enables AI Employee to send emails as an external action

This is a Model Context Protocol (MCP) server implementation for email sending.
Integrates with the human-in-the-loop approval workflow.

Usage: python email_mcp_server.py --to recipient@email.com --subject "Subject" --body "Message"

Author: Usama (Panaversity Student)
Hackathon: Personal AI Employee Hackathon 0
"""

import smtplib
import sys
import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

class EmailMCPServer:
    """MCP Server for sending emails via Gmail SMTP"""

    def __init__(self):
        self.config_file = Path(__file__).parent / "email_config.json"
        self.load_config()

    def load_config(self):
        """Load email configuration from config file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.smtp_server = config.get("smtp_server", "smtp.gmail.com")
                self.smtp_port = config.get("smtp_port", 587)
                self.sender_email = config.get("sender_email", "")
                self.sender_password = config.get("sender_password", "")
                self.sender_name = config.get("sender_name", "AI Employee")
        else:
            print("[WARNING] email_config.json not found. Creating template...")
            self.create_config_template()
            print("[INFO] Please update email_config.json with your credentials")
            sys.exit(1)

    def create_config_template(self):
        """Create a template configuration file"""
        template = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "your-email@gmail.com",
            "sender_password": "your-app-password-here",
            "sender_name": "AI Employee"
        }
        with open(self.config_file, 'w') as f:
            json.dump(template, f, indent=2)

    def send_email(self, to_email, subject, body, cc=None, bcc=None):
        """
        Send an email via Gmail SMTP

        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            body (str): Email body (plain text)
            cc (str, optional): CC email addresses (comma-separated)
            bcc (str, optional): BCC email addresses (comma-separated)

        Returns:
            bool: True if sent successfully, False otherwise
        """
        print("=" * 60)
        print("  EMAIL MCP SERVER - Sending Email")
        print("=" * 60)
        print(f"[INFO] From: {self.sender_name} <{self.sender_email}>")
        print(f"[INFO] To: {to_email}")
        print(f"[INFO] Subject: {subject}")
        print(f"[INFO] Body length: {len(body)} characters")
        print("-" * 60)

        if not self.sender_email or not self.sender_password:
            print("[ERROR] Email credentials not configured!")
            print("[INFO] Please update email_config.json with your Gmail credentials")
            return False

        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = f"{self.sender_name} <{self.sender_email}>"
            message["To"] = to_email
            message["Subject"] = subject

            if cc:
                message["Cc"] = cc
            if bcc:
                message["Bcc"] = bcc

            # Add body
            message.attach(MIMEText(body, "plain"))

            # Connect to Gmail SMTP server
            print("[SMTP] Connecting to Gmail SMTP server...")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Secure connection

            print("[SMTP] Logging in...")
            server.login(self.sender_email, self.sender_password)

            # Send email
            print("[SMTP] Sending email...")
            recipients = [to_email]
            if cc:
                recipients.extend(cc.split(','))
            if bcc:
                recipients.extend(bcc.split(','))

            server.sendmail(self.sender_email, recipients, message.as_string())

            # Close connection
            server.quit()

            print("[SUCCESS] Email sent successfully!")
            print("=" * 60)

            # Log the action
            self.log_email(to_email, subject, body, success=True)

            return True

        except smtplib.SMTPAuthenticationError:
            print("[ERROR] Authentication failed!")
            print("[INFO] Make sure you're using a Gmail App Password, not your regular password")
            print("[INFO] Visit: https://myaccount.google.com/apppasswords")
            self.log_email(to_email, subject, body, success=False, error="Authentication failed")
            return False

        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")
            self.log_email(to_email, subject, body, success=False, error=str(e))
            return False

    def log_email(self, to_email, subject, body, success=True, error=None):
        """Log email sending action"""
        log_dir = Path(__file__).parent / "AI_Employee_Vault" / "logs"
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"email_log_{datetime.now().strftime('%Y%m%d')}.json"

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "to": to_email,
            "subject": subject,
            "body_preview": body[:100] + "..." if len(body) > 100 else body,
            "success": success,
            "error": error
        }

        # Append to log file
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)

        logs.append(log_entry)

        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)


def main():
    """Main entry point for Email MCP Server"""

    if len(sys.argv) < 2:
        print("Email MCP Server")
        print("=" * 60)
        print("\nUsage:")
        print('  python email_mcp_server.py --to "recipient@email.com" --subject "Subject" --body "Message"')
        print("\nOptional:")
        print('  --cc "cc@email.com"')
        print('  --bcc "bcc@email.com"')
        print("\nSetup:")
        print("  1. Create email_config.json with your Gmail credentials")
        print("  2. Use Gmail App Password (not regular password)")
        print("  3. Visit: https://myaccount.google.com/apppasswords")
        return

    # Parse command line arguments
    args = {}
    i = 1
    while i < len(sys.argv):
        if sys.argv[i].startswith('--'):
            key = sys.argv[i][2:]
            if i + 1 < len(sys.argv):
                args[key] = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        else:
            i += 1

    # Validate required arguments
    if 'to' not in args or 'subject' not in args or 'body' not in args:
        print("[ERROR] Missing required arguments!")
        print("Required: --to, --subject, --body")
        return

    # Create MCP server and send email
    mcp = EmailMCPServer()
    success = mcp.send_email(
        to_email=args['to'],
        subject=args['subject'],
        body=args['body'],
        cc=args.get('cc'),
        bcc=args.get('bcc')
    )

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
