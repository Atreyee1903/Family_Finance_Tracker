import pandas as pd
import os
from pathlib import Path


class DataManager:
    """Handles all CSV file operations for the finance tracker."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.members_file = os.path.join(data_dir, "members.csv")
        self.earnings_file = os.path.join(data_dir, "earnings.csv")
        self.expenses_file = os.path.join(data_dir, "expenses.csv")
        
        # Create data directory if it doesn't exist
        Path(data_dir).mkdir(exist_ok=True)
        
        # Initialize CSV files if they don't exist
        self._initialize_files()

    def _initialize_files(self):
        """Create CSV files with headers if they don't exist."""
        if not os.path.exists(self.members_file):
            df = pd.DataFrame(columns=["member_id", "name"])
            df.to_csv(self.members_file, index=False)

        if not os.path.exists(self.earnings_file):
            df = pd.DataFrame(columns=["member_id", "amount", "date"])
            df.to_csv(self.earnings_file, index=False)

        if not os.path.exists(self.expenses_file):
            df = pd.DataFrame(columns=["category", "amount", "date", "paid_by"])
            df.to_csv(self.expenses_file, index=False)

    def load_members(self) -> pd.DataFrame:
        """Load members from CSV file."""
        try:
            df = pd.read_csv(self.members_file)
            if len(df) == 0:
                return pd.DataFrame(columns=["member_id", "name"])
            return df
        except Exception as e:
            print(f"Error loading members: {e}")
            return pd.DataFrame(columns=["member_id", "name"])

    def load_earnings(self) -> pd.DataFrame:
        """Load earnings from CSV file."""
        try:
            df = pd.read_csv(self.earnings_file)
            if len(df) == 0:
                return pd.DataFrame(columns=["member_id", "amount", "date"])
            return df
        except Exception as e:
            print(f"Error loading earnings: {e}")
            return pd.DataFrame(columns=["member_id", "amount", "date"])

    def load_expenses(self) -> pd.DataFrame:
        """Load expenses from CSV file."""
        try:
            df = pd.read_csv(self.expenses_file)
            if len(df) == 0:
                return pd.DataFrame(columns=["category", "amount", "date", "paid_by"])
            return df
        except Exception as e:
            print(f"Error loading expenses: {e}")
            return pd.DataFrame(columns=["category", "amount", "date", "paid_by"])

    def add_member(self, name: str) -> bool:
        """Add a new member to the members CSV."""
        if not name or name.strip() == "":
            return False

        df = self.load_members()
        
        # Check for duplicate names
        if name.lower() in df["name"].str.lower().values:
            return False

        # Get next ID
        next_id = int(df["member_id"].max()) + 1 if len(df) > 0 else 1
        
        # Add new member
        new_member = pd.DataFrame({"member_id": [next_id], "name": [name]})
        df = pd.concat([df, new_member], ignore_index=True)
        
        df.to_csv(self.members_file, index=False)
        return True

    def add_earning(self, member_id: int, amount: float, date: str) -> bool:
        """Add a new earning record."""
        if amount <= 0:
            return False

        df = self.load_earnings()
        
        new_earning = pd.DataFrame({
            "member_id": [member_id],
            "amount": [amount],
            "date": [date]
        })
        df = pd.concat([df, new_earning], ignore_index=True)
        
        df.to_csv(self.earnings_file, index=False)
        return True

    def add_expense(self, category: str, amount: float, date: str, paid_by: int) -> bool:
        """Add a new expense record."""
        if amount <= 0:
            return False

        df = self.load_expenses()
        
        new_expense = pd.DataFrame({
            "category": [category],
            "amount": [amount],
            "date": [date],
            "paid_by": [paid_by]
        })
        df = pd.concat([df, new_expense], ignore_index=True)
        
        df.to_csv(self.expenses_file, index=False)
        return True

    def get_member_names(self) -> list:
        """Get list of member names for dropdowns."""
        df = self.load_members()
        if len(df) == 0:
            return []
        return df.sort_values("member_id")["name"].tolist()

    def get_member_id(self, name: str) -> int:
        """Get member ID by name."""
        df = self.load_members()
        result = df[df["name"] == name]
        if len(result) == 0:
            return None
        return int(result.iloc[0]["member_id"])

    def member_exists(self, member_id: int) -> bool:
        """Check if a member exists."""
        df = self.load_members()
        return member_id in df["member_id"].values

    def delete_member(self, member_id: int) -> bool:
        """Delete a member from the members CSV."""
        df = self.load_members()
        df = df[df["member_id"] != member_id]
        df.to_csv(self.members_file, index=False)
        return True

    def has_member_transactions(self, member_id: int) -> bool:
        """Check if a member has any income or expense records."""
        earnings = self.load_earnings()
        expenses = self.load_expenses()
        
        has_earnings = member_id in earnings["member_id"].values
        has_expenses = member_id in expenses["paid_by"].values
        
        return has_earnings or has_expenses

    def get_member_income(self, member_id: int) -> float:
        """Get total income for a member."""
        df = self.load_earnings()
        member_earnings = df[df["member_id"] == member_id]
        if len(member_earnings) == 0:
            return 0.0
        return float(member_earnings["amount"].sum())

    def get_member_expenses(self, member_id: int) -> float:
        """Get total expenses for a member."""
        df = self.load_expenses()
        member_expenses = df[df["paid_by"] == member_id]
        if len(member_expenses) == 0:
            return 0.0
        return float(member_expenses["amount"].sum())

    def get_income_by_date_range(self, start_date: str, end_date: str, member_id: int = None) -> pd.DataFrame:
        """Get income for a specific date range, optionally filtered by member."""
        df = self.load_earnings()
        if len(df) == 0:
            return pd.DataFrame(columns=["member_id", "amount", "date"])
        
        df["date"] = pd.to_datetime(df["date"])
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        df = df[(df["date"] >= start) & (df["date"] <= end)]
        
        if member_id is not None:
            df = df[df["member_id"] == member_id]
        
        return df

    def get_income_this_month(self) -> float:
        """Get total income for current month."""
        from datetime import datetime
        today = datetime.today()
        start_of_month = today.replace(day=1).strftime("%Y-%m-%d")
        end_of_month = today.strftime("%Y-%m-%d")
        
        df = self.get_income_by_date_range(start_of_month, end_of_month)
        if len(df) == 0:
            return 0.0
        return float(df["amount"].sum())

    def get_income_today(self) -> float:
        """Get total income for today."""
        from datetime import datetime
        today = datetime.today().strftime("%Y-%m-%d")
        
        df = self.get_income_by_date_range(today, today)
        if len(df) == 0:
            return 0.0
        return float(df["amount"].sum())

    def get_total_income(self) -> float:
        """Get total income across all records."""
        df = self.load_earnings()
        if len(df) == 0:
            return 0.0
        return float(df["amount"].sum())

    def get_monthly_income_trend(self) -> pd.DataFrame:
        """Get income grouped by month."""
        df = self.load_earnings()
        if len(df) == 0:
            return pd.DataFrame(columns=["month", "amount"])
        
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.to_period("M").astype(str)
        
        monthly = df.groupby("month")["amount"].sum().reset_index()
        monthly.columns = ["month", "amount"]
        
        return monthly

    def get_total_expenses(self) -> float:
        """Get total expenses across all records."""
        df = self.load_expenses()
        if len(df) == 0:
            return 0.0
        return float(df["amount"].sum())

    def get_expenses_this_month(self) -> float:
        """Get total expenses for current month."""
        from datetime import datetime
        today = datetime.today()
        start_of_month = today.replace(day=1).strftime("%Y-%m-%d")
        end_of_month = today.strftime("%Y-%m-%d")
        
        df = self.load_expenses()
        if len(df) == 0:
            return 0.0
        
        df["date"] = pd.to_datetime(df["date"])
        start = pd.to_datetime(start_of_month)
        end = pd.to_datetime(end_of_month)
        
        df = df[(df["date"] >= start) & (df["date"] <= end)]
        if len(df) == 0:
            return 0.0
        return float(df["amount"].sum())

    def get_expenses_today(self) -> float:
        """Get total expenses for today."""
        from datetime import datetime
        today = datetime.today().strftime("%Y-%m-%d")
        
        df = self.load_expenses()
        if len(df) == 0:
            return 0.0
        
        df["date"] = pd.to_datetime(df["date"])
        today_dt = pd.to_datetime(today)
        
        df = df[df["date"] == today_dt]
        if len(df) == 0:
            return 0.0
        return float(df["amount"].sum())

    def get_monthly_expense_trend(self) -> pd.DataFrame:
        """Get expenses grouped by month."""
        df = self.load_expenses()
        if len(df) == 0:
            return pd.DataFrame(columns=["month", "amount"])
        
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.to_period("M").astype(str)
        
        monthly = df.groupby("month")["amount"].sum().reset_index()
        monthly.columns = ["month", "amount"]
        
        return monthly
