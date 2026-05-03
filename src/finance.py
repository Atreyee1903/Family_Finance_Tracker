import pandas as pd
from src.data_manager import DataManager


class FinanceCalculator:
    """Handles financial calculations and summaries."""

    def __init__(self, data_manager: DataManager):
        self.dm = data_manager

    def get_total_income(self) -> float:
        """Calculate total income across all members."""
        df = self.dm.load_earnings()
        if len(df) == 0:
            return 0.0
        return float(df["amount"].sum())

    def get_total_expenses(self) -> float:
        """Calculate total expenses across all categories."""
        df = self.dm.load_expenses()
        if len(df) == 0:
            return 0.0
        return float(df["amount"].sum())

    def get_balance(self) -> float:
        """Calculate balance (income - expenses)."""
        return self.get_total_income() - self.get_total_expenses()

    def get_income_by_member(self) -> dict:
        """Get total income for each member."""
        earnings = self.dm.load_earnings()
        members = self.dm.load_members()

        if len(earnings) == 0 or len(members) == 0:
            return {}

        income_by_member = earnings.groupby("member_id")["amount"].sum().to_dict()
        
        # Map member IDs to names
        result = {}
        for member_id, amount in income_by_member.items():
            member_name = members[members["member_id"] == member_id]["name"].values
            if len(member_name) > 0:
                result[member_name[0]] = amount
        
        return result

    def get_expenses_by_member(self) -> dict:
        """Get total expenses for each member (who paid)."""
        expenses = self.dm.load_expenses()
        members = self.dm.load_members()

        if len(expenses) == 0 or len(members) == 0:
            return {}

        expenses_by_member = expenses.groupby("paid_by")["amount"].sum().to_dict()
        
        # Map member IDs to names
        result = {}
        for member_id, amount in expenses_by_member.items():
            member_name = members[members["member_id"] == member_id]["name"].values
            if len(member_name) > 0:
                result[member_name[0]] = amount
        
        return result

    def get_expenses_by_category(self) -> dict:
        """Get total expenses grouped by category."""
        df = self.dm.load_expenses()
        if len(df) == 0:
            return {}
        return df.groupby("category")["amount"].sum().to_dict()

    def get_highest_spending_category(self) -> str:
        """Get the category with highest spending."""
        expenses_by_category = self.get_expenses_by_category()
        if not expenses_by_category:
            return "N/A"
        return max(expenses_by_category, key=expenses_by_category.get)

    def get_savings_percentage(self) -> float:
        """Calculate savings as a percentage of income."""
        total_income = self.get_total_income()
        if total_income == 0:
            return 0.0
        balance = self.get_balance()
        return (balance / total_income) * 100

    def get_monthly_expenses(self) -> pd.DataFrame:
        """Get expenses grouped by month."""
        df = self.dm.load_expenses()
        if len(df) == 0:
            return pd.DataFrame(columns=["month", "amount"])

        # Convert date to datetime and extract month
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.to_period("M").astype(str)
        
        monthly = df.groupby("month")["amount"].sum().reset_index()
        monthly.columns = ["month", "amount"]
        
        return monthly

    def get_member_summary(self) -> pd.DataFrame:
        """Get summary of income and expenses per member."""
        members = self.dm.load_members()
        
        if len(members) == 0:
            return pd.DataFrame(columns=["Member", "Income", "Expenses"])

        income_by_member = self.get_income_by_member()
        expenses_by_member = self.get_expenses_by_member()
        
        summary_data = []
        for _, member in members.iterrows():
            name = member["name"]
            income = income_by_member.get(name, 0.0)
            expenses = expenses_by_member.get(name, 0.0)
            
            summary_data.append({
                "Member": name,
                "Income": income,
                "Expenses": expenses
            })
        
        return pd.DataFrame(summary_data)

    def get_total_income_by_date_range(self, start_date: str, end_date: str) -> float:
        """Get total income for a date range."""
        df = self.dm.get_income_by_date_range(start_date, end_date)
        if len(df) == 0:
            return 0.0
        return float(df["amount"].sum())

    def get_total_expenses_by_date_range(self, start_date: str, end_date: str) -> float:
        """Get total expenses for a date range."""
        df = self.dm.load_expenses()
        if len(df) == 0:
            return 0.0
        
        df["date"] = pd.to_datetime(df["date"])
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        df = df[(df["date"] >= start) & (df["date"] <= end)]
        if len(df) == 0:
            return 0.0
        return float(df["amount"].sum())

    def get_balance_by_date_range(self, start_date: str, end_date: str) -> float:
        """Get balance for a date range."""
        income = self.get_total_income_by_date_range(start_date, end_date)
        expenses = self.get_total_expenses_by_date_range(start_date, end_date)
        return income - expenses

    def get_monthly_comparison(self) -> pd.DataFrame:
        """Get monthly income vs expense comparison."""
        earnings = self.dm.load_earnings()
        expenses = self.dm.load_expenses()
        
        if len(earnings) == 0 and len(expenses) == 0:
            return pd.DataFrame(columns=["month", "income", "expenses"])
        
        # Process income by month
        if len(earnings) > 0:
            earnings["date"] = pd.to_datetime(earnings["date"])
            earnings["month"] = earnings["date"].dt.to_period("M").astype(str)
            income_monthly = earnings.groupby("month")["amount"].sum().reset_index()
            income_monthly.columns = ["month", "income"]
        else:
            income_monthly = pd.DataFrame(columns=["month", "income"])
        
        # Process expenses by month
        if len(expenses) > 0:
            expenses["date"] = pd.to_datetime(expenses["date"])
            expenses["month"] = expenses["date"].dt.to_period("M").astype(str)
            expenses_monthly = expenses.groupby("month")["amount"].sum().reset_index()
            expenses_monthly.columns = ["month", "expenses"]
        else:
            expenses_monthly = pd.DataFrame(columns=["month", "expenses"])
        
        # Merge on month
        if len(income_monthly) > 0 or len(expenses_monthly) > 0:
            result = income_monthly.merge(expenses_monthly, on="month", how="outer")
            result = result.fillna(0.0)
            return result
        
        return pd.DataFrame(columns=["month", "income", "expenses"])

    def get_top_earner(self) -> tuple:
        """Get top earner (name, amount)."""
        income_by_member = self.get_income_by_member()
        if not income_by_member:
            return ("N/A", 0.0)
        top_member = max(income_by_member, key=income_by_member.get)
        return (top_member, income_by_member[top_member])

    def get_top_spender(self) -> tuple:
        """Get top spender (name, amount)."""
        expenses_by_member = self.get_expenses_by_member()
        if not expenses_by_member:
            return ("N/A", 0.0)
        top_member = max(expenses_by_member, key=expenses_by_member.get)
        return (top_member, expenses_by_member[top_member])

    def get_highest_spending_category_with_amount(self) -> tuple:
        """Get highest spending category (name, amount)."""
        expenses_by_category = self.get_expenses_by_category()
        if not expenses_by_category:
            return ("N/A", 0.0)
        top_category = max(expenses_by_category, key=expenses_by_category.get)
        return (top_category, expenses_by_category[top_category])

    def get_best_month(self) -> tuple:
        """Get best month for savings (month, savings_amount)."""
        comparison = self.get_monthly_comparison()
        if len(comparison) == 0:
            return ("N/A", 0.0)
        
        comparison["savings"] = comparison["income"] - comparison["expenses"]
        best_idx = comparison["savings"].idxmax()
        best_month = comparison.loc[best_idx]
        
        return (best_month["month"], best_month["savings"])

    def get_status(self, start_date: str = None, end_date: str = None) -> tuple:
        """Get financial status (emoji, text) based on savings rate."""
        if start_date and end_date:
            income = self.get_total_income_by_date_range(start_date, end_date)
            balance = self.get_balance_by_date_range(start_date, end_date)
        else:
            income = self.get_total_income()
            balance = self.get_balance()
        
        if income == 0:
            return ("⚪", "No Data")
        
        savings_pct = (balance / income) * 100
        
        if savings_pct >= 20:
            return ("🟢", "Healthy (Saving Well)")
        elif savings_pct >= 0:
            return ("🟡", "Moderate")
        else:
            return ("🔴", "Overspending")
