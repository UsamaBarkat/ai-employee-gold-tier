"""
Comprehensive Audit Logging System for AI Employee
Gold Tier Feature - Tracks all AI actions for security and compliance
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class AuditLogger:
    """Centralized audit logging for all AI Employee actions"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.logs_dir = self.vault_path / 'logs'
        self.logs_dir.mkdir(exist_ok=True)

        # Set up file logging
        self.logger = logging.getLogger('AIEmployeeAudit')
        self.logger.setLevel(logging.INFO)

        # Create handler if not already exists
        if not self.logger.handlers:
            handler = logging.FileHandler(
                self.logs_dir / f'audit_{datetime.now().strftime("%Y-%m")}.log',
                encoding='utf-8'
            )
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_action(
        self,
        action_type: str,
        actor: str,
        target: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        approval_status: Optional[str] = None,
        approved_by: Optional[str] = None,
        result: str = "pending",
        details: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Log an AI Employee action

        Args:
            action_type: Type of action (email_send, linkedin_post, task_complete, etc.)
            actor: Who performed the action (claude_code, watcher, human, etc.)
            target: Target of the action (email address, file path, etc.)
            parameters: Dict of action parameters
            approval_status: approved, rejected, auto_approved, or None
            approved_by: human or system
            result: success, failure, pending
            details: Additional context

        Returns:
            Dict with full log entry
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "actor": actor,
            "target": target,
            "parameters": parameters or {},
            "approval_status": approval_status,
            "approved_by": approved_by,
            "result": result,
            "details": details
        }

        # Write to structured JSON log
        json_log_file = self.logs_dir / f'{datetime.now().strftime("%Y-%m-%d")}_audit.json'

        # Read existing logs
        logs = []
        if json_log_file.exists():
            try:
                with open(json_log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

        # Append new log
        logs.append(log_entry)

        # Write back
        with open(json_log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

        # Also log to text file
        log_message = (
            f"[{action_type}] {actor} -> {target or 'N/A'} "
            f"| Status: {result} | Approval: {approval_status or 'N/A'}"
        )

        if result == "failure":
            self.logger.error(log_message)
        elif result == "success":
            self.logger.info(log_message)
        else:
            self.logger.warning(log_message)

        return log_entry

    def get_recent_logs(self, limit: int = 50) -> list:
        """Get recent audit logs"""
        today = datetime.now().strftime("%Y-%m-%d")
        json_log_file = self.logs_dir / f'{today}_audit.json'

        if not json_log_file.exists():
            return []

        try:
            with open(json_log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
                return logs[-limit:]  # Return last N logs
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def get_logs_by_type(self, action_type: str, days: int = 7) -> list:
        """Get logs filtered by action type"""
        all_logs = []

        # Check last N days
        for i in range(days):
            date = datetime.now()
            date = date.replace(day=date.day - i)
            date_str = date.strftime("%Y-%m-%d")
            json_log_file = self.logs_dir / f'{date_str}_audit.json'

            if json_log_file.exists():
                try:
                    with open(json_log_file, 'r', encoding='utf-8') as f:
                        logs = json.load(f)
                        filtered = [log for log in logs if log['action_type'] == action_type]
                        all_logs.extend(filtered)
                except (json.JSONDecodeError, FileNotFoundError):
                    continue

        return all_logs

    def get_failed_actions(self, days: int = 7) -> list:
        """Get all failed actions in last N days"""
        all_logs = []

        for i in range(days):
            date = datetime.now()
            date = date.replace(day=date.day - i)
            date_str = date.strftime("%Y-%m-%d")
            json_log_file = self.logs_dir / f'{date_str}_audit.json'

            if json_log_file.exists():
                try:
                    with open(json_log_file, 'r', encoding='utf-8') as f:
                        logs = json.load(f)
                        failed = [log for log in logs if log['result'] == 'failure']
                        all_logs.extend(failed)
                except (json.JSONDecodeError, FileNotFoundError):
                    continue

        return all_logs


# Convenience function for quick logging
def log_ai_action(
    vault_path: str,
    action_type: str,
    actor: str = "claude_code",
    **kwargs
) -> Dict[str, Any]:
    """Quick function to log an action"""
    logger = AuditLogger(vault_path)
    return logger.log_action(action_type, actor, **kwargs)


# Example usage
if __name__ == "__main__":
    # Test the audit logger
    vault = r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault"

    logger = AuditLogger(vault)

    # Log some test actions
    logger.log_action(
        action_type="email_send",
        actor="claude_code",
        target="test@example.com",
        parameters={"subject": "Test Email"},
        approval_status="approved",
        approved_by="human",
        result="success"
    )

    logger.log_action(
        action_type="linkedin_post",
        actor="linkedin_watcher",
        target="https://linkedin.com/post/123",
        parameters={"hashtags": ["#AgenticAI", "#Panaversity"]},
        approval_status="approved",
        approved_by="human",
        result="success"
    )

    logger.log_action(
        action_type="task_complete",
        actor="claude_code",
        target="inbox_task_123.md",
        result="success"
    )

    print("Test logs created successfully!")
    print(f"\nRecent logs: {len(logger.get_recent_logs())}")
