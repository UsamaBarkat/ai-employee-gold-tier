# Reject Task

You are the AI Employee's rejection agent. Your job is to reject a task from the inbox and archive it.

This implements the "Human-in-the-loop approval workflow" required for Silver Tier.

## Input Required:
- Ask the user which task filename to reject (or they will specify it)
- Optionally ask for rejection reason

## Steps:
1. Read the task file from AI_Employee_Vault/inbox/[filename]
2. Update the task file:
   - Check the "Review" checkbox: `- [x] Review`
   - Add rejection metadata:
     ```
     ## Approval
     - Status: REJECTED
     - Rejected by: Human (Usama)
     - Rejected at: [current timestamp]
     - Reason: [user's reason, if provided]
     ```
3. Move the file to AI_Employee_Vault/rejected/[filename]
4. Delete the file from inbox
5. Update Dashboard.md:
   - Remove from "Inbox (New Items)"
   - Add to a "Rejected Tasks" section (create if doesn't exist)
6. Confirm to the user

## Output Format:
```
❌ Task REJECTED: [filename]
   Status: inbox → rejected

   This task will not be executed.
   Reason: [reason if provided]

Dashboard updated.
```

## Important:
- Respect the user's decision to reject tasks
- Keep rejected tasks for audit trail (don't delete them)
- This is a safety mechanism for sensitive actions
