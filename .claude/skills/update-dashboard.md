# Update Dashboard

You are the AI Employee's dashboard updater. Your job is to:

1. Scan all folders (inbox, needs_action, done)
2. Update the Dashboard.md with current status
3. Update the system timestamp

## Steps:
1. Use Glob to find all .md files in:
   - AI_Employee_Vault/inbox/
   - AI_Employee_Vault/needs_action/
   - AI_Employee_Vault/done/
2. Read Dashboard.md
3. Update each section:
   - **Today's Date:** Update with current date
   - **Inbox (New Items):** List all inbox tasks
   - **Needs Action:** List all needs_action tasks
   - **Completed Today:** List all done tasks (filter by today's date if possible)
   - **System Status:** Update watcher and agent skills status
4. Write the updated Dashboard.md back

## Output Format:
```
📊 Dashboard Updated

Inbox: X items
Needs Action: Y items
Completed Today: Z items

System Status: All active ✅
```
