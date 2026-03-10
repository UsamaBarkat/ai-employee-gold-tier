"""
Odoo Accounting Configuration for AI Employee
Gold Tier Feature - ERP/Accounting Integration Settings
"""

# Odoo Server Connection
ODOO_URL = "http://localhost:8069"  # Default Odoo URL (change if hosted elsewhere)
ODOO_DB = "ai_employee_accounting"  # Your Odoo database name
ODOO_USERNAME = "admin"  # Odoo admin username
ODOO_PASSWORD = "admin"  # Odoo admin password (CHANGE THIS!)

# API Settings
ODOO_API_VERSION = "2.0"  # JSON-RPC version

# Accounting Settings
DEFAULT_CURRENCY = "USD"
DEFAULT_TAX_RATE = 0.0  # 0% default (configure based on your location)

# Chart of Accounts (customize for your business)
EXPENSE_ACCOUNTS = {
    'software': 'Software Subscriptions',
    'hosting': 'Hosting & Infrastructure',
    'marketing': 'Marketing & Advertising',
    'education': 'Education & Training',
    'hardware': 'Hardware & Equipment',
    'other': 'Other Expenses'
}

INCOME_ACCOUNTS = {
    'services': 'Service Revenue',
    'products': 'Product Sales',
    'consulting': 'Consulting Revenue',
    'other': 'Other Income'
}

# Reporting Settings
FISCAL_YEAR_START = "01-01"  # MM-DD format
REPORTING_CURRENCY = "USD"

# Integration Settings
ENABLE_AUTO_CATEGORIZATION = True  # AI categorizes transactions
REQUIRE_APPROVAL_ABOVE = 1000.00  # Require human approval for transactions > $1000
SYNC_INTERVAL = 3600  # Sync every hour (seconds)

# Vault path
VAULT_PATH = r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault"

# Accounting reports folder
ACCOUNTING_REPORTS_DIR = f"{VAULT_PATH}/accounting_reports"
