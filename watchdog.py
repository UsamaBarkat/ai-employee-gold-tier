"""
Watchdog Process - Monitor and Restart Crashed Watchers
Gold Tier Feature - Keeps AI Employee alive 24/7
"""

import subprocess
import time
import psutil
from pathlib import Path
from datetime import datetime
from audit_logger import AuditLogger

class WatchdogMonitor:
    """Monitor critical processes and restart them if they crash"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.audit_logger = AuditLogger(str(vault_path))

        # Define critical processes to monitor
        self.processes = {
            'linkedin_watcher': {
                'script': 'linkedin_watcher.py',
                'args': ['--auto'],
                'restart_delay': 10,  # Wait 10 seconds before restart
                'max_restarts_per_hour': 6,  # Prevent restart loops
                'restart_history': []
            },
            'file_watcher': {
                'script': 'file_watcher.py',
                'args': [],
                'restart_delay': 5,
                'max_restarts_per_hour': 10,
                'restart_history': []
            }
        }

        self.running_processes = {}
        self.check_interval = 60  # Check every 60 seconds

    def is_process_running(self, process_name: str) -> bool:
        """Check if a process is running"""
        if process_name not in self.running_processes:
            return False

        proc = self.running_processes[process_name]

        try:
            # Check if process exists and is running
            if proc.poll() is None:
                return True
            else:
                return False
        except:
            return False

    def start_process(self, process_name: str) -> bool:
        """Start a monitored process"""
        config = self.processes[process_name]
        script_path = Path(__file__).parent / config['script']

        if not script_path.exists():
            print(f"ERROR: Script not found: {script_path}")
            self.audit_logger.log_action(
                action_type="watchdog_start_failed",
                actor="watchdog",
                target=process_name,
                parameters={"reason": "script_not_found"},
                result="failure"
            )
            return False

        try:
            # Start the process
            cmd = ['python', str(script_path)] + config['args']
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, 'CREATE_NEW_CONSOLE') else 0
            )

            self.running_processes[process_name] = proc

            print(f"[{datetime.now().strftime('%H:%M:%S')}] Started {process_name} (PID: {proc.pid})")

            self.audit_logger.log_action(
                action_type="watchdog_start",
                actor="watchdog",
                target=process_name,
                parameters={"pid": proc.pid},
                result="success",
                details=f"Process started successfully"
            )

            return True

        except Exception as e:
            print(f"ERROR starting {process_name}: {e}")
            self.audit_logger.log_action(
                action_type="watchdog_start_failed",
                actor="watchdog",
                target=process_name,
                parameters={"error": str(e)},
                result="failure"
            )
            return False

    def can_restart(self, process_name: str) -> bool:
        """Check if process can be restarted (prevent restart loops)"""
        config = self.processes[process_name]
        history = config['restart_history']

        # Clean old history (older than 1 hour)
        one_hour_ago = time.time() - 3600
        config['restart_history'] = [t for t in history if t > one_hour_ago]

        # Check if we've hit restart limit
        if len(config['restart_history']) >= config['max_restarts_per_hour']:
            return False

        return True

    def restart_process(self, process_name: str) -> bool:
        """Restart a crashed process"""
        if not self.can_restart(process_name):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                  f"⚠️  {process_name} hit restart limit - MANUAL INTERVENTION REQUIRED")

            self.audit_logger.log_action(
                action_type="watchdog_restart_limit",
                actor="watchdog",
                target=process_name,
                result="failure",
                details="Too many restarts - possible crash loop"
            )

            return False

        config = self.processes[process_name]

        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
              f"🔄 Restarting {process_name} in {config['restart_delay']}s...")

        time.sleep(config['restart_delay'])

        # Record restart
        config['restart_history'].append(time.time())

        # Start process
        success = self.start_process(process_name)

        if success:
            self.audit_logger.log_action(
                action_type="watchdog_restart",
                actor="watchdog",
                target=process_name,
                result="success",
                details=f"Process restarted successfully (restart #{len(config['restart_history'])} in last hour)"
            )
        else:
            self.audit_logger.log_action(
                action_type="watchdog_restart_failed",
                actor="watchdog",
                target=process_name,
                result="failure"
            )

        return success

    def check_and_restart(self):
        """Check all processes and restart any that crashed"""
        for process_name in self.processes.keys():
            if not self.is_process_running(process_name):
                print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                      f"⚠️  {process_name} is NOT running!")

                self.restart_process(process_name)
            else:
                proc = self.running_processes[process_name]
                print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                      f"✅ {process_name} is running (PID: {proc.pid})")

    def run(self):
        """Main watchdog loop"""
        print("=" * 60)
        print("AI Employee Watchdog Monitor Started")
        print("=" * 60)
        print(f"Monitoring {len(self.processes)} processes")
        print(f"Check interval: {self.check_interval} seconds")
        print("Press Ctrl+C to stop")
        print("=" * 60)

        self.audit_logger.log_action(
            action_type="watchdog_started",
            actor="watchdog",
            target="system",
            result="success",
            details=f"Monitoring {len(self.processes)} processes"
        )

        # Start all processes initially
        for process_name in self.processes.keys():
            self.start_process(process_name)

        # Monitor loop
        try:
            while True:
                time.sleep(self.check_interval)
                self.check_and_restart()

        except KeyboardInterrupt:
            print("\n" + "=" * 60)
            print("Shutting down Watchdog Monitor...")
            print("=" * 60)

            self.audit_logger.log_action(
                action_type="watchdog_stopped",
                actor="watchdog",
                target="system",
                result="success",
                details="Watchdog stopped by user"
            )

            # Optionally stop all monitored processes
            for process_name, proc in self.running_processes.items():
                if proc.poll() is None:
                    print(f"Stopping {process_name}...")
                    proc.terminate()

    def status(self):
        """Print current status of all monitored processes"""
        print("=" * 60)
        print("Watchdog Status Report")
        print("=" * 60)

        for process_name, config in self.processes.items():
            running = self.is_process_running(process_name)
            status_icon = "✅" if running else "❌"

            print(f"{status_icon} {process_name}")

            if running:
                proc = self.running_processes[process_name]
                print(f"   PID: {proc.pid}")

            restarts = len([t for t in config['restart_history'] if t > time.time() - 3600])
            print(f"   Restarts (last hour): {restarts}/{config['max_restarts_per_hour']}")
            print()


if __name__ == "__main__":
    import sys

    vault_path = r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault"
    watchdog = WatchdogMonitor(vault_path)

    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        # Just show status
        watchdog.status()
    else:
        # Run monitoring
        watchdog.run()
