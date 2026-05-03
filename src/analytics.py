import matplotlib.pyplot as plt
import pandas as pd
from src.finance import FinanceCalculator


class AnalyticsGenerator:
    """Generates visualizations and analytics."""

    def __init__(self, finance_calculator: FinanceCalculator):
        self.fc = finance_calculator

    def create_category_pie_chart(self):
        """Create a pie chart of expenses by category."""
        expenses_by_category = self.fc.get_expenses_by_category()
        
        if not expenses_by_category:
            return None

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(
            expenses_by_category.values(),
            labels=expenses_by_category.keys(),
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Expenses by Category")
        
        return fig

    def create_monthly_trend_chart(self):
        """Create a bar chart of monthly spending trend."""
        monthly_data = self.fc.get_monthly_expenses()
        
        if len(monthly_data) == 0:
            return None

        fig, ax = plt.subplots(figsize=(8, 3))
        ax.bar(monthly_data["month"], monthly_data["amount"], color="steelblue")
        ax.set_title("Monthly Spending Trend")
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount")
        ax.tick_params(axis="x", rotation=45)
        
        fig.tight_layout()
        return fig

    def create_income_vs_expense_chart(self):
        """Create a comparison chart of income vs expenses by month."""
        comparison = self.fc.get_monthly_comparison()
        
        if len(comparison) == 0:
            return None
        
        fig, ax = plt.subplots(figsize=(8, 3))
        
        x = range(len(comparison))
        width = 0.35
        
        ax.bar(
            [i - width/2 for i in x],
            comparison["income"],
            width,
            label="Income",
            color="#70AD47",
            alpha=0.8,
            edgecolor="#4F7A3A"
        )
        ax.bar(
            [i + width/2 for i in x],
            comparison["expenses"],
            width,
            label="Expenses",
            color="#ED7D31",
            alpha=0.8,
            edgecolor="#C65911"
        )
        
        ax.set_title("Income vs Expense Trend", fontsize=14, fontweight="bold", pad=20)
        ax.set_xlabel("Month", fontsize=11)
        ax.set_ylabel("Amount (₹)", fontsize=11)
        ax.set_xticks(x)
        ax.set_xticklabels(comparison["month"], rotation=45)
        ax.legend(fontsize=10)
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        
        fig.tight_layout()
        return fig

    def create_member_comparison_chart(self):
        """Create a comparison chart of income vs expenses by member."""
        summary = self.fc.get_member_summary()
        
        if len(summary) == 0:
            return None

        fig, ax = plt.subplots(figsize=(8, 3))
        
        x = range(len(summary))
        width = 0.35
        
        ax.bar(
            [i - width/2 for i in x],
            summary["Income"],
            width,
            label="Income",
            color="green"
        )
        ax.bar(
            [i + width/2 for i in x],
            summary["Expenses"],
            width,
            label="Expenses",
            color="red"
        )
        
        ax.set_title("Income vs Expenses by Member")
        ax.set_xlabel("Member")
        ax.set_ylabel("Amount")
        ax.set_xticks(x)
        ax.set_xticklabels(summary["Member"])
        ax.legend()
        
        fig.tight_layout()
        return fig

    def get_insights(self) -> dict:
        """Generate text insights about finances."""
        insights = {}
        
        # Highest spending category
        highest_category = self.fc.get_highest_spending_category()
        insights["highest_category"] = highest_category
        
        # Total savings
        balance = self.fc.get_balance()
        insights["total_savings"] = balance
        
        # Savings percentage
        savings_pct = self.fc.get_savings_percentage()
        insights["savings_percentage"] = savings_pct
        
        # Total income and expenses
        insights["total_income"] = self.fc.get_total_income()
        insights["total_expenses"] = self.fc.get_total_expenses()
        
        return insights
