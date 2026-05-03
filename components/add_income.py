import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from src.data_manager import DataManager


def render_add_income(dm: DataManager):
    """Render the Add Income component with date-driven analysis."""
    
    # Main Title
    st.title("💵 Track Income")
    
    members = dm.get_member_names()
    
    if not members:
        st.warning("⚠️ No members available. Please add a member first in the 'Add Member' section.")
        return
    
    # ============== 1. ADD INCOME FORM ==============
    st.subheader("➕ Record New Income")
    
    col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1])
    
    with col1:
        member = st.selectbox("Select Member", members, key="income_member_select")
    
    with col2:
        amount = st.number_input("Amount (₹)", min_value=0.01, step=100.0, key="income_amount_input")
    
    with col3:
        date = st.date_input("Date", datetime.today(), key="income_date_input")
    
    with col4:
        add_button = st.button("Add Income", key="add_income_btn", use_container_width=True)
    
    if add_button:
        if amount <= 0:
            st.error("❌ Amount must be greater than 0")
        else:
            member_id = dm.get_member_id(member)
            if dm.add_earning(member_id, amount, str(date)):
                st.success(f"✅ Income of ₹{amount:.2f} added for {member}")
                st.rerun()
            else:
                st.error("❌ Failed to add income")
    
    st.divider()
    
    # ============== 2. DATE FILTERS + QUICK BUTTONS ==============
    st.subheader("📅 Filters")
    
    # Quick filter buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("Last 7 Days", key="btn_7days", use_container_width=True):
            st.session_state.income_start_date = datetime.today() - timedelta(days=7)
            st.session_state.income_end_date = datetime.today()
    
    with col2:
        if st.button("This Month", key="btn_thismonth", use_container_width=True):
            st.session_state.income_start_date = datetime.today().replace(day=1)
            st.session_state.income_end_date = datetime.today()
    
    with col3:
        if st.button("All Time", key="btn_alltime", use_container_width=True):
            st.session_state.income_start_date = datetime.today() - timedelta(days=365*5)
            st.session_state.income_end_date = datetime.today()
    
    with col4:
        if st.button("🔄 Reset", key="btn_reset_income", use_container_width=True):
            st.session_state.income_start_date = datetime.today() - timedelta(days=30)
            st.session_state.income_end_date = datetime.today()
            st.rerun()
    
    st.write("")  # Spacing
    
    col1, col2, col3 = st.columns([1.5, 1.5, 2])
    
    with col1:
        start_date = st.date_input(
            "From Date",
            value=st.session_state.get("income_start_date", datetime.today() - timedelta(days=30)),
            key="income_start_date"
        )
    
    with col2:
        end_date = st.date_input(
            "To Date",
            value=st.session_state.get("income_end_date", datetime.today()),
            key="income_end_date"
        )
    
    with col3:
        filter_member = st.selectbox(
            "Member (Optional)",
            ["All Members"] + members,
            key="income_filter_member"
        )
    
    # Get filtered data
    member_id_filter = None if filter_member == "All Members" else dm.get_member_id(filter_member)
    filtered_earnings = dm.get_income_by_date_range(str(start_date), str(end_date), member_id_filter)
    
    st.divider()
    
    # ============== 3. INCOME SUMMARY ==============
    st.subheader("📊 Income Summary")
    
    total_income = dm.get_total_income()
    income_this_month = dm.get_income_this_month()
    income_today = dm.get_income_today()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Total Income", f"₹{total_income:,.2f}")
    with col2:
        st.metric("📅 This Month", f"₹{income_this_month:,.2f}")
    with col3:
        st.metric("📆 Today", f"₹{income_today:,.2f}")
    
    st.divider()
    
    # ============== 4. MONTHLY INCOME TREND CHART ==============
    st.subheader("📈 Monthly Income Trend")
    
    monthly_trend = dm.get_monthly_income_trend()
    
    if len(monthly_trend) > 0:
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.bar(monthly_trend["month"], monthly_trend["amount"], color="#4472C4", alpha=0.8, edgecolor="#2F5496", linewidth=1)
        ax.set_title("Monthly Income Trend", fontsize=12, fontweight="bold", pad=15)
        ax.set_xlabel("Month", fontsize=10)
        ax.set_ylabel("Amount (₹)", fontsize=10)
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        
        # Add value labels on bars
        for i, v in enumerate(monthly_trend["amount"]):
            ax.text(i, v + max(monthly_trend["amount"]) * 0.02, f"₹{v:,.0f}", ha="center", va="bottom", fontsize=8, fontweight="bold")
        
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
    else:
        st.info("📭 No income data available for chart. Add some income records to see trends!")
    
    st.divider()
    
    # ============== 5. INCOME HISTORY TABLE ==============
    with st.expander("📋 Income History"):
        if len(filtered_earnings) > 0:
            # Merge with member names
            earnings_display = filtered_earnings.copy()
            members_df = dm.load_members()
            earnings_display = earnings_display.merge(
                members_df[["member_id", "name"]],
                on="member_id",
                how="left"
            )
            
            # Format for display
            earnings_display = earnings_display[["name", "amount", "date"]].copy()
            earnings_display.columns = ["Member", "Amount (₹)", "Date"]
            earnings_display = earnings_display.sort_values("Date", ascending=False)
            
            # Format currency and dates
            earnings_display["Amount (₹)"] = earnings_display["Amount (₹)"].apply(lambda x: f"₹{x:,.2f}")
            earnings_display["Date"] = pd.to_datetime(earnings_display["Date"]).dt.strftime("%Y-%m-%d")
            
            st.dataframe(
                earnings_display,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("📭 No income records in the selected date range. Try adjusting your filters!")
    
    st.divider()
    
    # ============== 6. INSIGHTS ==============
    st.subheader("💡 Insights")
    
    if len(filtered_earnings) > 0:
        # Highest income entry
        max_entry = filtered_earnings.loc[filtered_earnings["amount"].idxmax()]
        members_df = dm.load_members()
        member_name = members_df[members_df["member_id"] == max_entry["member_id"]]["name"].values[0]
        
        # Best month (from monthly trend)
        if len(monthly_trend) > 0:
            best_month_idx = monthly_trend["amount"].idxmax()
            best_month = monthly_trend.loc[best_month_idx]
            best_month_value = best_month["amount"]
            best_month_label = best_month["month"]
            avg_monthly = monthly_trend["amount"].mean()
        else:
            best_month_value = 0
            best_month_label = "N/A"
            avg_monthly = 0
        
        # Average income in filtered period
        avg_income = filtered_earnings["amount"].mean()
        total_filtered = filtered_earnings["amount"].sum()
        
        st.write(
            f"🏆 **Highest Entry:** ₹{max_entry['amount']:,.2f} by {member_name} on {max_entry['date']}\n\n"
            f"📈 **Best Month:** {best_month_label} (₹{best_month_value:,.2f})\n\n"
            f"📊 **Average Income:** ₹{avg_income:,.2f} per entry | ₹{avg_monthly:,.2f} per month\n\n"
            f"💵 **Total (Filtered Period):** ₹{total_filtered:,.2f}"
        )
    else:
        st.info("💭 No income data to analyze. Add income records to see insights!")
