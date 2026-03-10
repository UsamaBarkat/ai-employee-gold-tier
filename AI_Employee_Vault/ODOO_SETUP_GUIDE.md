# Odoo Accounting Setup Guide

**Gold Tier Feature - ERP/Accounting Integration**

This guide walks you through setting up Odoo Community Edition for your AI Employee's accounting integration.

---

## Table of Contents
1. [What is Odoo?](#what-is-odoo)
2. [Installation Options](#installation-options)
3. [Quick Start (Docker)](#quick-start-docker)
4. [Manual Installation](#manual-installation)
5. [Initial Configuration](#initial-configuration)
6. [MCP Server Setup](#mcp-server-setup)
7. [Testing the Integration](#testing-the-integration)

---

## What is Odoo?

Odoo is an open-source ERP (Enterprise Resource Planning) system with a powerful accounting module. It's free, self-hosted, and perfect for the AI Employee to manage business finances.

**Why Odoo?**
- Free and open-source (Community Edition)
- Self-hosted (privacy-first)
- JSON-RPC API for integration
- Comprehensive accounting features
- Scales from personal to enterprise

---

## Installation Options

### Option 1: Docker (Recommended - Fastest)
- **Time:** 10 minutes
- **Difficulty:** Easy
- **Best for:** Quick setup, testing

### Option 2: Windows Installer
- **Time:** 30 minutes
- **Difficulty:** Medium
- **Best for:** Production use on Windows

### Option 3: Linux Package
- **Time:** 20 minutes
- **Difficulty:** Medium
- **Best for:** Linux servers, always-on deployment

---

## Quick Start (Docker)

### Prerequisites
- Docker Desktop installed ([download here](https://www.docker.com/products/docker-desktop/))

### Step 1: Pull and Run Odoo

```bash
# Pull Odoo image
docker pull odoo:latest

# Run Odoo container
docker run -d -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -e POSTGRES_DB=postgres --name db postgres:13

# Run Odoo
docker run -d -p 8069:8069 --name odoo --link db:db -t odoo
```

### Step 2: Access Odoo

1. Open browser: `http://localhost:8069`
2. Create database:
   - Database Name: `ai_employee_accounting`
   - Email: your_email@example.com
   - Password: (choose a strong password)
   - Language: English
   - Country: Your country

### Step 3: Install Accounting Module

1. After login, go to Apps
2. Remove "Apps" filter
3. Search for "Accounting"
4. Click "Install"
5. Wait for installation (2-3 minutes)

---

## Manual Installation (Windows)

### Step 1: Download Installer

Visit: https://www.odoo.com/page/download

Download: Odoo Community Edition (latest version)

### Step 2: Run Installer

1. Run the `.exe` installer
2. Choose installation directory
3. Set PostgreSQL password
4. Complete installation

### Step 3: Start Odoo Service

- Odoo should start automatically
- Access at: `http://localhost:8069`
- Follow Step 2 and 3 from Docker method above

---

## Initial Configuration

### 1. Company Setup

Go to: **Settings → General Settings → Companies**

Configure:
- Company Name
- Address
- Currency
- Tax ID
- Logo

### 2. Chart of Accounts

Go to: **Accounting → Configuration → Chart of Accounts**

Odoo provides default accounts. Customize if needed:
- Bank accounts
- Income accounts
- Expense accounts
- Asset accounts

### 3. Journals

Go to: **Accounting → Configuration → Journals**

Default journals:
- Customer Invoices
- Vendor Bills
- Bank
- Cash
- Miscellaneous

### 4. Fiscal Year

Go to: **Accounting → Configuration → Settings**

Set:
- Fiscal Year End: December 31 (or your fiscal year end)
- Lock Date: (optional - prevents backdating)

---

## MCP Server Setup

### Step 1: Configure Credentials

Edit: `E:\AI-300\My_Hackathons_Teacher\odoo_config.py`

```python
# Odoo Server Connection
ODOO_URL = "http://localhost:8069"
ODOO_DB = "ai_employee_accounting"  # Your database name
ODOO_USERNAME = "admin"  # Your Odoo username (email)
ODOO_PASSWORD = "your_password"  # Your Odoo password
```

### Step 2: Test Connection

```bash
cd E:\AI-300\My_Hackathons_Teacher
python odoo_mcp_server.py
```

Expected output:
```
[OK] Connected to Odoo at http://localhost:8069
[TEST] Getting account balance...
[TEST] Getting recent transactions...
[OK] Odoo MCP Server test complete!
```

### Step 3: Add Test Data (Optional)

In Odoo web interface:

**Create Sample Income:**
1. Accounting → Customers → Invoices
2. Create invoice
3. Post invoice
4. Register payment

**Create Sample Expense:**
1. Accounting → Vendors → Bills
2. Create bill
3. Post bill
4. Register payment

---

## Testing the Integration

### Test 1: Get Account Balance

```python
from odoo_mcp_server import OdooMCPServer

vault = r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault"
odoo = OdooMCPServer(vault)

balance = odoo.get_account_balance()
print(f"Total balance: ${balance:,.2f}")
```

### Test 2: Get Recent Transactions

```python
transactions = odoo.get_recent_transactions(days=30, limit=10)

for tx in transactions:
    print(f"{tx['date']} - {tx['name']}: ${tx['amount']:,.2f}")
```

### Test 3: Generate P&L Report

```python
report = odoo.generate_profit_loss_report(period_months=1)

print(f"Income: ${report['income']:,.2f}")
print(f"Expenses: ${report['expenses']:,.2f}")
print(f"Profit: ${report['profit']:,.2f}")

# Save to vault
odoo.save_report_to_vault(report, "Monthly_PL_Report")
```

### Test 4: Create Expense

```python
expense_id = odoo.create_expense(
    amount=50.00,
    description="Office supplies",
    category="hardware",
    partner_name="Office Depot"
)

if expense_id:
    print(f"Expense created: {expense_id}")
```

---

## Integration with CEO Briefing

Once Odoo is set up, the CEO Briefing will automatically include accounting data:

```markdown
## Accounting & Financial Health

### Monthly Performance
- Revenue: $5,000
- Expenses: $1,200
- Net Profit: $3,800 (76% margin)

### Status
Profitable - Trend: Stable

### Notable Transactions
- Largest expense: Software subscription ($200)
- Largest income: Client A payment ($2,500)
```

---

## Troubleshooting

### Connection Refused

**Problem:** `[WinError 10061] No connection could be made`

**Solutions:**
1. Check Odoo is running: `http://localhost:8069`
2. Verify Docker container: `docker ps`
3. Check firewall settings

### Authentication Failed

**Problem:** `Odoo authentication failed`

**Solutions:**
1. Verify credentials in `odoo_config.py`
2. Check database name matches
3. Try logging into Odoo web interface

### Module Not Found

**Problem:** `Cannot find account.move model`

**Solutions:**
1. Install Accounting module in Odoo
2. Go to Apps → Search "Accounting" → Install
3. Restart Python script

---

## Next Steps

### 1. Regular Use
- Odoo MCP runs in background
- CEO Briefing auto-generates accounting section
- AI categorizes transactions

### 2. Advanced Features
- Connect to bank feeds (if supported)
- Set up automated invoicing
- Configure expense categorization rules
- Enable multi-currency if needed

### 3. Always-On Deployment
- Deploy Odoo to cloud VM (Oracle Free Tier, AWS, etc.)
- Configure secure access (HTTPS, VPN)
- Set up automated backups

---

## Security Best Practices

### 1. Change Default Passwords
- Never use "admin/admin" in production
- Use strong, unique passwords

### 2. Restrict Access
- Only allow localhost connections for local setup
- Use VPN for remote access

### 3. Regular Backups
- Backup Odoo database weekly
- Export accounting data monthly
- Keep offline copies

### 4. Audit Logging
- All Odoo actions are logged by AI Employee
- Review `/logs/` folder regularly

---

## Resources

### Official Documentation
- Odoo Docs: https://www.odoo.com/documentation
- Accounting Guide: https://www.odoo.com/documentation/17.0/applications/finance/accounting.html
- API Reference: https://www.odoo.com/documentation/17.0/developer/reference/external_api.html

### Community
- Odoo Forum: https://www.odoo.com/forum
- GitHub: https://github.com/odoo/odoo

### Video Tutorials
- Odoo Accounting Basics: YouTube "Odoo Accounting Tutorial"
- API Integration: YouTube "Odoo JSON-RPC API"

---

## Summary Checklist

Before using Odoo with AI Employee:

- [ ] Odoo installed and running
- [ ] Database created
- [ ] Accounting module installed
- [ ] Company information configured
- [ ] Chart of accounts reviewed
- [ ] Test data added (optional)
- [ ] `odoo_config.py` updated with credentials
- [ ] Connection tested successfully
- [ ] First P&L report generated

---

**Once complete, your AI Employee will have full accounting capabilities!**

---

*Gold Tier Feature - Complete ERP Integration*
*Panaversity Hackathon 0*
