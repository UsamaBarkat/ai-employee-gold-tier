# View Audit Logs

You are tasked with viewing and analyzing the AI Employee audit logs.

## Your Task

Review the comprehensive audit logs to understand system activity, identify issues, and ensure security compliance.

## What to Do

1. **Read Recent Audit Logs**
   - Check the `/logs/` folder in the vault
   - Look for files named `YYYY-MM-DD_audit.json`
   - Read the most recent log file

2. **Analyze Log Entries**
   Each log entry contains:
   - `timestamp`: When the action occurred
   - `action_type`: Type of action (email_send, linkedin_post, task_complete, etc.)
   - `actor`: Who performed it (claude_code, watcher, human)
   - `target`: Target of the action
   - `parameters`: Action details
   - `approval_status`: approved, rejected, auto_approved, or null
   - `approved_by`: human or system
   - `result`: success, failure, or pending
   - `details`: Additional context

3. **Generate Summary Report**

Create a report with:

### Action Summary (Last 24 Hours)
- Total actions: [N]
- Successful: [N]
- Failed: [N]
- Pending: [N]

### Breakdown by Type
| Action Type | Count | Success Rate |
|-------------|-------|--------------|
| email_send | N | X% |
| linkedin_post | N | X% |
| task_complete | N | X% |

### Failed Actions (Requires Attention)
- [List any failed actions with details]

### Approval Status
- Auto-approved: [N]
- Human-approved: [N]
- Rejected: [N]

### Security Notes
- Any unusual patterns?
- Any suspicious activities?
- Any actions requiring follow-up?

## Success Criteria

- Provide clear summary of system activity
- Highlight any failures or issues
- Note any security concerns
- Give actionable recommendations

## Output Format

Present findings in a clear, structured format. If there are issues, prioritize them by severity.

---

*Gold Tier Feature - Comprehensive Audit Logging*
