import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from src.data_manager import DataManager


EXPENSE_CATEGORIES = [
    "Food",
    "Rent",
    "Bills",
    "Transport",
    "Entertainment",
    "Other"
]


def render_add_expense(dm: DataManager):
    """Render the Add Expense component with full analysis."""
    
    # Main Title
    st.title("💸 Track Expenses")
    
    members = dm.get_member_names()
    
    if not members:
        st.warning("⚠️ No members available. Please add a member first in the 'Add Member' section.")
        return
    
    # ============== 1. ADD EXPENSE FORM ==============
    st.subheader("➕ Record New Expense")
    
    col1, col2, col3, col4, col5 = st.columns([1.2, 1, 1, 1.2, 1])
    
    with col1:
        category = st.selectbox("Category", EXPENSE_CATEGORIES, key="expense_category_select")
    
    with col2:
        amount = st.number_input("Amount (₹)", min_value=0.01, step=50.0, key="expense_amount_input")
    
    with col3:
        paid_by = st.selectbox("Paid By", members, key="expense_paid_by_select")
    
    with col4:
        date = st.date_input("Date", datetime.today(), key="expense_date_input")
    
    with col5:
        add_button = st.button("Add Expense", key="add_expense_btn", use_container_width=True)
    
    if add_button:
        if amount <= 0:
            st.error("❌ Amount must be greater than 0")
        else:
            member_id = dm.get_member_id(paid_by)
            if dm.add_expense(category, amount, str(date), member_id):
                st.success(f"✅ Expense of ₹{amount:.2f} ({category}) added by {paid_by}")
                st.rerun()
            else:
                st.error("❌ Failed to add expense")
    
    st.divider()
    
    # ============== 2. DATE FILTERS + QUICK BUTTONS ==============
    st.subheader("📅 Filters")
    
    # Quick filter buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("Last 7 Days", key="btn_exp_7days", use_container_width=True):
            st.session_state.expense_start_date = datetime.today() - timedelta(days=7)
            st.session_state.expense_end_date = datetime.today()
    
    with col2:
        if st.button("This Month", key="btn_exp_thismonth", use_container_width=True):
            st.session_state.expense_start_date = datetime.today().replace(day=1)
            st.session_state.expense_end_date = datetime.today()
    
    with col3:
        if st.button("All Time", key="btn_exp_alltime", use_container_width=True):
            st.session_state.expense_start_date = datetime.today() - timedelta(days=365*5)
            st.session_state.expense_end_date = datetime.today()
    
    with col4:
        if st.button("🔄 Reset", key="btn_reset_expense", use_container_width=True):
            st.session_state.expense_start_date = datetime.today() - timedelta(days=30)
            st.session_state.expense_end_date = datetime.today()
            st.rerun()
    
    st.write("")  # Spacing
    
    col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 1.5])
    
    with col1:
        start_date = st.date_input(
            "From Date",
            value=st.session_state.get("expense_start_date", datetime.today() - timedelta(days=30)),
            key="expense_start_date"
        )
    
    with col2:
        end_date = st.date_input(
            "To Date",
            value=st.session_state.get("expense_end_date", datetime.today()),
            key="expense_end_date"
        )
    
    with col3:
        filter_member = st.selectbox(
            "Member (Optional)",
            ["All Members"] + members,
            key="expense_filter_member"
        )
    
    with col4:
        filter_category = st.selectbox(
            "Category (Optional)",
            ["All Categories"] + EXPENSE_CATEGORIES,
            key="expense_filter_category"
        )
    
    # Get filtered data
    all_expenses = dm.load_expenses()
    
    if len(all_expenses) > 0:
        all_expenses["date"] = pd.to_datetime(all_expenses["date"])
        start = pd.to_datetime(str(start_date))
        end = pd.to_datetime(str(end_date))
        
        filtered_expenses = all_expenses[(all_expenses["date"] >= start) & (all_expenses["date"] <= end)].copy()
        
        if filter_member != "All Members":
            member_id_filter = dm.get_member_id(filter_member)
            filtered_expenses = filtered_expenses[filtered_expenses["paid_by"] == member_id_filter]
        
        if filter_category != "All Categories":
            filtered_expenses = filtered_expenses[filtered_expenses["category"] == filter_category]
    else:
        filtered_expenses = pd.DataFrame(columns=["category", "amount", "date", "paid_by"])
    
    st.divider()
    
    # ============== 3. EXPENSE SUMMARY ==============
    st.subheader("📊 Expense Summary")
    
    total_expenses = dm.get_total_expenses()
    expenses_this_month = dm.get_expenses_this_month()
    expenses_today = dm.get_expenses_today()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💸 Total Expenses", f"₹{total_expenses:,.2f}")
    with col2:
        st.metric("📅 This Month", f"₹{expenses_this_month:,.2f}")
    with col3:
        st.metric("📆 Today", f"₹{expenses_today:,.2f}")
    
    st.divider()
    
    # ============== 4 & 5. CATEGORY PIE + MONTHLY TREND (SIDE BY SIDE) ==============
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("### 🥧 Category-wise Spending")
        if len(filtered_expenses) > 0:
            category_spending = filtered_expenses.groupby("category")["amount"].sum().sort_values(ascending=False)
            
            fig, ax = plt.subplots(figsize=(6, 4))
            colors = ["#4472C4", "#ED7D31", "#A5A5A5", "#FFC000", "#5B9BD5", "#70AD47"]
            wedges, texts, autotexts = ax.pie(
                category_spending.values,
                labels=category_spending.index,
                autopct=lambda pct: f"₹{pct/100*category_spending.sum():,.0f}\n({pct:.1f}%)",
                startangle=90,
                colors=colors[:len(category_spending)]
            )
            
            # Format text
            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_fontweight("bold")
                autotext.set_fontsize(8)
            
            for text in texts:
                text.set_fontsize(9)
                text.set_fontweight("bold")
            
            ax.set_title("Spending Distribution", fontsize=11, fontweight="bold", pad=15)
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
        else:
            st.info("📭 No expense data available")
    
    with col_chart2:
        st.markdown("### 📈 Monthly Expense Trend")
        monthly_trend = dm.get_monthly_expense_trend()
        
        if len(monthly_trend) > 0:
            fig, ax = plt.subplots(figsize=(8, 3))
            ax.bar(monthly_trend["month"], monthly_trend["amount"], color="#ED7D31", alpha=0.8, edgecolor="#C65911", linewidth=1)
            ax.set_title("Monthly Trend", fontsize=11, fontweight="bold", pad=15)
            ax.set_xlabel("Month", fontsize=9)
            ax.set_ylabel("Amount (₹)", fontsize=9)
            ax.tick_params(axis="x", rotation=45, labelsize=8)
            ax.grid(axis="y", alpha=0.3, linestyle="--")
            
            # Add value labels on bars
            for i, v in enumerate(monthly_trend["amount"]):
                ax.text(i, v + max(monthly_trend["amount"]) * 0.02, f"₹{v:,.0f}", ha="center", va="bottom", fontsize=7, fontweight="bold")
            
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
        else:
            st.info("📭 No expense data available")
    
    st.divider()
    
    # ============== 6. EXPENSE HISTORY TABLE (COLLAPSIBLE) ==============
    with st.expander("📋 Expense History"):
        if len(filtered_expenses) > 0:
            # Merge with member names
            expenses_display = filtered_expenses.copy()
            members_df = dm.load_members()
            expenses_display = expenses_display.merge(
                members_df[["member_id", "name"]],
                left_on="paid_by",
                right_on="member_id",
                how="left"
            )
            
            # Format for display
            expenses_display = expenses_display[["category", "amount", "date", "name"]].copy()
            expenses_display.columns = ["Category", "Amount (₹)", "Date", "Paid By"]
            expenses_display = expenses_display.sort_values("Date", ascending=False)
            
            # Format currency and dates
            expenses_display["Amount (₹)"] = expenses_display["Amount (₹)"].apply(lambda x: f"₹{x:,.2f}")
            expenses_display["Date"] = pd.to_datetime(expenses_display["Date"]).dt.strftime("%Y-%m-%d")
            
            st.dataframe(
                expenses_display,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("📭 No expense records in the selected filters. Try adjusting your filters!")
    
    st.divider()
    
    # ============== 7. INSIGHTS ==============
    st.subheader("💡 Insights")
    
    if len(all_expenses) > 0:
        # Highest spending category
        highest_category = all_expenses.groupby("category")["amount"].sum().idxmax()
        highest_category_amount = all_expenses.groupby("category")["amount"].sum().max()
        
        # Top spender
        top_spender_id = all_expenses.groupby("paid_by")["amount"].sum().idxmax()
        top_spender_name = dm.load_members()[dm.load_members()["member_id"] == top_spender_id]["name"].values[0]
        top_spender_amount = all_expenses.groupby("paid_by")["amount"].sum().max()
        
        # Average monthly expense
        all_expenses_with_dates = all_expenses.copy()
        all_expenses_with_dates["date"] = pd.to_datetime(all_expenses_with_dates["date"])
        monthly_trend_all = all_expenses_with_dates.groupby(all_expenses_with_dates["date"].dt.to_period("M"))["amount"].sum()
        avg_monthly = monthly_trend_all.mean() if len(monthly_trend_all) > 0 else 0
        
        # Check if expense > income
        total_income = dm.get_total_income()
        total_expense = dm.get_total_expenses()
        overspending_warning = ""
        if total_expense > total_income and total_income > 0:
            overspend_pct = ((total_expense - total_income) / total_income) * 100
            overspending_warning = f"\n\n🔴 **OVERSPENDING ALERT:** Expenses exceed income by ₹{total_expense - total_income:,.2f} ({overspend_pct:.1f}%)"
        
        # Calculate percentages for insights
        highest_category_pct = (highest_category_amount / total_expense * 100) if total_expense > 0 else 0
        top_spender_pct = (top_spender_amount / total_expense * 100) if total_expense > 0 else 0
        
        st.write(
            f"🔥 **Highest Spending Category:** {highest_category} (₹{highest_category_amount:,.2f} • {highest_category_pct:.1f}%)\n\n"
            f"👤 **Top Spender:** {top_spender_name} (₹{top_spender_amount:,.2f} • {top_spender_pct:.1f}%)\n\n"
            f"📉 **Avg Monthly Expense:** ₹{avg_monthly:,.2f}\n\n"
            f"💵 **Total Expenses:** ₹{total_expense:,.2f}"
            f"{overspending_warning}"
        )
    else:
        st.info("💭 No expense data to analyze. Add expenses to see insights!")
