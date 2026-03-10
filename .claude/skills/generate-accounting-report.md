# Generate Accounting Report

You are tasked with generating accounting reports from Odoo for the CEO Briefing system.

## Your Task

Generate Profit & Loss (P&L) reports from Odoo accounting system.

## Prerequisites

- Odoo Community Edition installed and running
- `odoo_config.py` configured with credentials
- Accounting module set up in Odoo

## Steps to Complete

1. **Connect to Odoo**
   ```python
   import sys
   sys.path.append('E:\\AI-300\\My_Hackathons_Teacher')
   from odoo_mcp_server import OdooMCPServer

   vault = r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault"
   odoo = OdooMCPServer(vault)

   if not odoo.connected:
       print("ERROR: Cannot connect to Odoo")
       print("Make sure Odoo is running and configured")
       # Exit or handle error
   ```

2. **Generate P&L Report**
   ```python
   # Generate report for last month
   report = odoo.generate_profit_loss_report(period_months=1)

   print(f"Income: ${report['income']:,.2f}")
   print(f"Expenses: ${report['expenses']:,.2f}")
   print(f"Profit: ${report['profit']:,.2f}")
   print(f"Margin: {report['profit_margin']:.2f}%")
   ```

3. **Save Report to Vault**
   ```python
   odoo.save_report_to_vault(report, "Monthly_PL_Report")
   ```

4. **Update CEO Briefing**
   - Read the latest CEO Briefing
   - Add accounting section with:
     - Monthly revenue
     - Monthly expenses
     - Net profit/loss
     - Profit margin trend
     - Notable transactions

## Report Structure

The generated report should include:

### Financial Summary
- Total Income
- Total Expenses
- Net Profit
- Profit Margin %

### Analysis
- Profitability status
- Month-over-month trends
- Notable changes
- Recommendations

### Recent Transactions
- Top 5 expenses
- Top 5 income sources
- Any unusual transactions

## Integration with CEO Briefing

When generating CEO Briefing, include:

```markdown
## Accounting & Financial Health

### Monthly Performance
- Revenue: $X,XXX
- Expenses: $X,XXX
- Net Profit: $X,XXX (XX% margin)

### Status
[Profitable/Break-even/Loss] - [Trend: Up/Down/Stable]

### Notable Transactions
- [Largest expense]: $XXX
- [Largest income]: $XXX

### Recommendations
- [AI-generated recommendation based on data]
```

## Error Handling

If Odoo is not available:
- Log error to audit system
- Add note to CEO Briefing: "Accounting data unavailable"
- Continue with other briefing sections

## Success Criteria

- P&L report generated successfully
- Report saved to `/accounting_reports/` folder
- Data integrated into CEO Briefing
- Audit log entry created

---

*Gold Tier Feature - Odoo Accounting Integration*
