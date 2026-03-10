"""
Error Recovery and Retry Logic for AI Employee
Gold Tier Feature - Makes watchers and MCP servers resilient
"""

import time
import logging
from functools import wraps
from typing import Callable, Any, Optional
from audit_logger import AuditLogger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ErrorRecovery')


class TransientError(Exception):
    """Errors that can be retried (network timeouts, API rate limits, etc.)"""
    pass


class PermanentError(Exception):
    """Errors that should not be retried (authentication, data corruption, etc.)"""
    pass


def with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_backoff: bool = True,
    vault_path: Optional[str] = None
):
    """
    Decorator for automatic retry with exponential backoff

    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Initial delay between retries (seconds)
        max_delay: Maximum delay between retries (seconds)
        exponential_backoff: Use exponential backoff (2^attempt * base_delay)
        vault_path: Path to vault for audit logging

    Usage:
        @with_retry(max_attempts=3, base_delay=2)
        def my_function():
            # Your code here
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            audit_logger = None
            if vault_path:
                audit_logger = AuditLogger(vault_path)

            last_exception = None

            for attempt in range(max_attempts):
                try:
                    result = func(*args, **kwargs)

                    # Log success if there were previous failures
                    if attempt > 0 and audit_logger:
                        audit_logger.log_action(
                            action_type="retry_success",
                            actor="error_recovery",
                            target=func.__name__,
                            parameters={"attempt": attempt + 1},
                            result="success",
                            details=f"Succeeded after {attempt} retries"
                        )

                    return result

                except PermanentError as e:
                    # Don't retry permanent errors
                    logger.error(f"{func.__name__}: Permanent error - {e}")
                    if audit_logger:
                        audit_logger.log_action(
                            action_type="permanent_error",
                            actor="error_recovery",
                            target=func.__name__,
                            parameters={"error": str(e)},
                            result="failure",
                            details="Permanent error - not retrying"
                        )
                    raise

                except (TransientError, Exception) as e:
                    last_exception = e

                    if attempt == max_attempts - 1:
                        # Last attempt failed
                        logger.error(
                            f"{func.__name__}: All {max_attempts} attempts failed - {e}"
                        )
                        if audit_logger:
                            audit_logger.log_action(
                                action_type="retry_exhausted",
                                actor="error_recovery",
                                target=func.__name__,
                                parameters={
                                    "max_attempts": max_attempts,
                                    "error": str(e)
                                },
                                result="failure",
                                details=f"All retry attempts exhausted"
                            )
                        raise

                    # Calculate delay
                    if exponential_backoff:
                        delay = min(base_delay * (2 ** attempt), max_delay)
                    else:
                        delay = base_delay

                    logger.warning(
                        f"{func.__name__}: Attempt {attempt + 1}/{max_attempts} "
                        f"failed - {e}. Retrying in {delay:.1f}s..."
                    )

                    if audit_logger:
                        audit_logger.log_action(
                            action_type="retry_attempt",
                            actor="error_recovery",
                            target=func.__name__,
                            parameters={
                                "attempt": attempt + 1,
                                "delay": delay,
                                "error": str(e)
                            },
                            result="pending"
                        )

                    time.sleep(delay)

            # Should never reach here, but just in case
            raise last_exception

        return wrapper
    return decorator


class GracefulDegradation:
    """Handle service degradation gracefully"""

    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.audit_logger = AuditLogger(vault_path)
        self.service_status = {}

    def mark_service_down(self, service_name: str, reason: str):
        """Mark a service as down"""
        self.service_status[service_name] = {
            'status': 'down',
            'reason': reason,
            'timestamp': time.time()
        }

        logger.warning(f"Service {service_name} marked as DOWN: {reason}")

        self.audit_logger.log_action(
            action_type="service_down",
            actor="graceful_degradation",
            target=service_name,
            parameters={"reason": reason},
            result="failure",
            details=f"Service degraded: {reason}"
        )

    def mark_service_up(self, service_name: str):
        """Mark a service as up"""
        was_down = service_name in self.service_status
        self.service_status[service_name] = {
            'status': 'up',
            'timestamp': time.time()
        }

        if was_down:
            logger.info(f"Service {service_name} RECOVERED")
            self.audit_logger.log_action(
                action_type="service_recovered",
                actor="graceful_degradation",
                target=service_name,
                result="success",
                details="Service recovered successfully"
            )

    def is_service_available(self, service_name: str) -> bool:
        """Check if service is available"""
        if service_name not in self.service_status:
            return True  # Assume up if never checked

        return self.service_status[service_name]['status'] == 'up'

    def get_fallback_action(self, service_name: str) -> str:
        """Get recommended fallback action for service"""
        fallbacks = {
            'gmail_api': 'Queue emails locally, process when service restores',
            'linkedin_api': 'Save posts to pending folder for later publishing',
            'banking_api': 'Never retry automatically, require fresh approval',
            'claude_code': 'Watchers continue collecting, queue grows',
            'obsidian': 'Write to temporary folder, sync when available'
        }

        return fallbacks.get(service_name, 'Log issue and alert human')


# Example usage and testing
if __name__ == "__main__":
    vault = r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault"

    # Test 1: Retry with transient error
    @with_retry(max_attempts=3, base_delay=1, vault_path=vault)
    def flaky_function():
        """Simulates a flaky API call"""
        import random
        if random.random() < 0.7:  # 70% chance of failure
            raise TransientError("Network timeout")
        return "Success!"

    # Test 2: Permanent error (no retry)
    @with_retry(max_attempts=3, vault_path=vault)
    def auth_function():
        """Simulates authentication failure"""
        raise PermanentError("Invalid credentials")

    # Test graceful degradation
    degradation = GracefulDegradation(vault)

    print("Testing Error Recovery System...")
    print("\n1. Testing retry with transient errors:")
    try:
        result = flaky_function()
        print(f"   Result: {result}")
    except TransientError as e:
        print(f"   Failed after all retries: {e}")

    print("\n2. Testing graceful degradation:")
    degradation.mark_service_down("gmail_api", "Rate limit exceeded")
    print(f"   Gmail available: {degradation.is_service_available('gmail_api')}")
    print(f"   Fallback: {degradation.get_fallback_action('gmail_api')}")

    degradation.mark_service_up("gmail_api")
    print(f"   Gmail recovered: {degradation.is_service_available('gmail_api')}")

    print("\n3. Testing permanent error (no retry):")
    try:
        auth_function()
    except PermanentError as e:
        print(f"   Caught permanent error (correctly not retried): {e}")

    print("\nError Recovery System test complete!")
