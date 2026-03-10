"""
Odoo MCP Server for AI Employee
Gold Tier Feature - ERP/Accounting Integration via JSON-RPC
"""

import json
import xmlrpc.client
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any

from audit_logger import AuditLogger
import odoo_config as config


class OdooMCPServer:
    """Odoo ERP integration via JSON-RPC API"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.audit_logger = AuditLogger(str(vault_path))
        self.reports_dir = Path(config.ACCOUNTING_REPORTS_DIR)
        self.reports_dir.mkdir(exist_ok=True)

        # Initialize connection
        self.url = config.ODOO_URL
        self.db = config.ODOO_DB
        self.username = config.ODOO_USERNAME
        self.password = config.ODOO_PASSWORD

        self.uid = None
        self.models = None
        self.connected = False

        # Try to connect
        self.connect()

    def connect(self) -> bool:
        """Connect to Odoo server"""
        try:
            # Authenticate
            common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.uid = common.authenticate(
                self.db,
                self.username,
                self.password,
                {}
            )

            if self.uid:
                # Get models proxy
                self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
                self.connected = True

                print(f"[OK] Connected to Odoo at {self.url}")

                self.audit_logger.log_action(
                    action_type="odoo_connected",
                    actor="odoo_mcp",
                    target=self.url,
                    result="success"
                )

                return True
            else:
                print("[ERROR] Odoo authentication failed")
                return False

        except Exception as e:
            print(f"[ERROR] Cannot connect to Odoo: {e}")
            print(f"[INFO] Make sure Odoo is running at {self.url}")
            self.connected = False

            self.audit_logger.log_action(
                action_type="odoo_connection_failed",
                actor="odoo_mcp",
                parameters={"error": str(e)},
                result="failure"
            )

            return False

    def execute(self, model: str, method: str, *args, **kwargs) -> Any:
        """Execute Odoo model method"""
        if not self.connected:
            raise Exception("Not connected to Odoo")

        return self.models.execute_kw(
            self.db,
            self.uid,
            self.password,
            model,
            method,
            args,
            kwargs
        )

    # ==================== ACCOUNTING OPERATIONS ====================

    def get_account_balance(self, account_code: str = None) -> float:
        """
        Get account balance

        Args:
            account_code: Specific account code (e.g., '1000' for bank)
                         If None, returns total balance

        Returns:
            float: Account balance
        """
        try:
            # Search for account
            domain = []
            if account_code:
                domain = [('code', '=', account_code)]

            accounts = self.execute(
                'account.account',
                'search_read',
                domain,
                {'fields': ['name', 'code', 'balance']}
            )

            if accounts:
                total = sum(acc['balance'] for acc in accounts)
                return total
            else:
                print(f"[WARNING] No account found with code: {account_code}")
                return 0.0

        except Exception as e:
            print(f"[ERROR] Failed to get account balance: {e}")
            return 0.0

    def get_recent_transactions(self, days: int = 30, limit: int = 100) -> List[Dict]:
        """
        Get recent accounting transactions

        Args:
            days: Look back N days
            limit: Maximum transactions to return

        Returns:
            List of transaction dictionaries
        """
        try:
            date_from = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

            # Search for journal entries (account moves)
            moves = self.execute(
                'account.move',
                'search_read',
                [('date', '>=', date_from), ('state', '=', 'posted')],
                {
                    'fields': ['name', 'date', 'ref', 'amount_total', 'journal_id', 'partner_id'],
                    'limit': limit,
                    'order': 'date desc'
                }
            )

            transactions = []
            for move in moves:
                transactions.append({
                    'id': move['id'],
                    'name': move['name'],
                    'date': move['date'],
                    'reference': move.get('ref', ''),
                    'amount': move['amount_total'],
                    'journal': move['journal_id'][1] if move.get('journal_id') else 'Unknown',
                    'partner': move['partner_id'][1] if move.get('partner_id') else 'N/A'
                })

            return transactions

        except Exception as e:
            print(f"[ERROR] Failed to get transactions: {e}")
            return []

    def create_expense(
        self,
        amount: float,
        description: str,
        category: str = 'other',
        date: str = None,
        partner_name: str = None
    ) -> Optional[int]:
        """
        Create expense entry

        Args:
            amount: Expense amount (positive number)
            description: Description of expense
            category: Expense category (from config.EXPENSE_ACCOUNTS)
            date: Date in YYYY-MM-DD format (defaults to today)
            partner_name: Vendor/partner name

        Returns:
            int: Created expense ID, or None if failed
        """
        if amount > config.REQUIRE_APPROVAL_ABOVE:
            print(f"[WARNING] Expense ${amount} requires human approval (threshold: ${config.REQUIRE_APPROVAL_ABOVE})")
            return None

        try:
            if not date:
                date = datetime.now().strftime('%Y-%m-%d')

            # Find or create partner
            partner_id = None
            if partner_name:
                partners = self.execute(
                    'res.partner',
                    'search_read',
                    [('name', '=', partner_name)],
                    {'fields': ['id'], 'limit': 1}
                )

                if partners:
                    partner_id = partners[0]['id']
                else:
                    # Create new partner
                    partner_id = self.execute(
                        'res.partner',
                        'create',
                        {'name': partner_name}
                    )

            # Create journal entry (simplified - in production would need proper account setup)
            expense_data = {
                'date': date,
                'ref': description,
                'journal_id': 1,  # Typically expense journal (adjust as needed)
                'line_ids': [
                    (0, 0, {
                        'name': description,
                        'debit': amount,
                        'credit': 0,
                        'account_id': 1,  # Expense account (adjust as needed)
                        'partner_id': partner_id
                    }),
                    (0, 0, {
                        'name': description,
                        'debit': 0,
                        'credit': amount,
                        'account_id': 2,  # Bank account (adjust as needed)
                        'partner_id': partner_id
                    })
                ]
            }

            move_id = self.execute('account.move', 'create', expense_data)

            print(f"[OK] Created expense: ${amount} - {description}")

            self.audit_logger.log_action(
                action_type="odoo_expense_created",
                actor="odoo_mcp",
                target=description,
                parameters={"amount": amount, "category": category},
                approval_status="auto_approved",
                approved_by="system",
                result="success"
            )

            return move_id

        except Exception as e:
            print(f"[ERROR] Failed to create expense: {e}")

            self.audit_logger.log_action(
                action_type="odoo_expense_failed",
                actor="odoo_mcp",
                parameters={"error": str(e)},
                result="failure"
            )

            return None

    def generate_profit_loss_report(self, period_months: int = 1) -> Dict:
        """
        Generate Profit & Loss report

        Args:
            period_months: Report period in months

        Returns:
            Dict with income, expenses, and profit
        """
        try:
            date_from = (datetime.now() - timedelta(days=period_months * 30)).strftime('%Y-%m-%d')
            date_to = datetime.now().strftime('%Y-%m-%d')

            # Get income
            income_moves = self.execute(
                'account.move.line',
                'read_group',
                [('date', '>=', date_from), ('date', '<=', date_to), ('account_id.user_type_id.name', '=', 'Income')],
                ['credit'],
                []
            )

            total_income = sum(group['credit'] for group in income_moves)

            # Get expenses
            expense_moves = self.execute(
                'account.move.line',
                'read_group',
                [('date', '>=', date_from), ('date', '<=', date_to), ('account_id.user_type_id.name', '=', 'Expenses')],
                ['debit'],
                []
            )

            total_expenses = sum(group['debit'] for group in expense_moves)

            # Calculate profit
            profit = total_income - total_expenses

            report = {
                'period': f"{date_from} to {date_to}",
                'income': total_income,
                'expenses': total_expenses,
                'profit': profit,
                'profit_margin': (profit / total_income * 100) if total_income > 0 else 0,
                'generated_at': datetime.now().isoformat()
            }

            return report

        except Exception as e:
            print(f"[ERROR] Failed to generate P&L report: {e}")
            return {
                'period': 'N/A',
                'income': 0,
                'expenses': 0,
                'profit': 0,
                'profit_margin': 0,
                'error': str(e)
            }

    def save_report_to_vault(self, report: Dict, report_name: str):
        """Save accounting report to Obsidian vault"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{report_name}_{timestamp}.md"
        filepath = self.reports_dir / filename

        content = f"""# {report_name.replace('_', ' ').title()}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Period
{report.get('period', 'N/A')}

## Financial Summary

| Metric | Amount |
|--------|--------|
| Total Income | ${report.get('income', 0):,.2f} |
| Total Expenses | ${report.get('expenses', 0):,.2f} |
| **Net Profit** | **${report.get('profit', 0):,.2f}** |
| Profit Margin | {report.get('profit_margin', 0):.2f}% |

## Analysis

"""

        if report.get('profit', 0) > 0:
            content += f"- **Profitable Period:** Generated ${report['profit']:,.2f} in profit\\n"
        elif report.get('profit', 0) < 0:
            content += f"- **Loss Period:** ${abs(report['profit']):,.2f} loss\\n"
        else:
            content += "- **Break-even Period**\\n"

        content += f"""
## Details

```json
{json.dumps(report, indent=2)}
```

---
*Generated by Odoo MCP Server*
*AI Employee - Gold Tier Feature*
"""

        filepath.write_text(content, encoding='utf-8')
        print(f"[OK] Report saved: {filename}")

        return filepath


# Example usage and testing
if __name__ == "__main__":
    print("Testing Odoo MCP Server...")

    vault = r"E:\AI-300\My_Hackathons_Teacher\AI_Employee_Vault"
    odoo = OdooMCPServer(vault)

    if not odoo.connected:
        print("\n[INFO] Odoo not connected (this is expected if not installed)")
        print("\n[SETUP] To activate Odoo integration:")
        print("1. Install Odoo Community Edition")
        print("   - Download from: https://www.odoo.com/page/download")
        print("   - Or use Docker: docker run -d -p 8069:8069 --name odoo odoo:latest")
        print("2. Create database and configure accounting")
        print("3. Update odoo_config.py with credentials")
        print("4. Run: python odoo_mcp_server.py")
        print("\n[OK] MCP Server infrastructure ready!")
    else:
        # Test operations
        print("\n[TEST] Getting account balance...")
        balance = odoo.get_account_balance()
        print(f"Balance: ${balance:,.2f}")

        print("\n[TEST] Getting recent transactions...")
        transactions = odoo.get_recent_transactions(days=30, limit=5)
        print(f"Found {len(transactions)} transactions")

        print("\n[TEST] Generating P&L report...")
        report = odoo.generate_profit_loss_report(period_months=1)
        print(f"Income: ${report['income']:,.2f}")
        print(f"Expenses: ${report['expenses']:,.2f}")
        print(f"Profit: ${report['profit']:,.2f}")

        # Save report
        odoo.save_report_to_vault(report, "Monthly_PL_Report")

        print("\n[OK] Odoo MCP Server test complete!")
