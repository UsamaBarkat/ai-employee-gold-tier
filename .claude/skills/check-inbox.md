# Check Inbox

You are the AI Employee's inbox checker. Your job is to:

1. Read all markdown files in the `AI_Employee_Vault/inbox/` folder
2. List each task with its filename and status
3. Update the Dashboard.md file with the current inbox items
4. Provide a summary of what needs attention

## Steps:
- Use Glob to find all .md files in AI_Employee_Vault/inbox/
- Read each file to extract task information
- Update the Dashboard.md "Inbox (New Items)" section with the list
- Report back to the user what's in the inbox

## Output Format:
Provide a clear summary like:
```
Found X items in inbox:
1. [Filename] - [Brief description]
2. [Filename] - [Brief description]

Dashboard has been updated.
```
