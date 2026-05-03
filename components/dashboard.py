import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from src.data_manager import DataManager
from src.finance import FinanceCalculator
from src.analytics import AnalyticsGenerator


def render_dashboard(dm: DataManager):
    """Render the Decision Dashboard."""
    st.title("📊 Financial Dashboard")
    
    fc = FinanceCalculator(dm)
    ag = AnalyticsGenerator(fc)
    
    # ============== 1. GLOBAL FILTERS ==============
    st.subheader("📅 Filters")
    
    # Quick filter buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("Last 7 Days", key="btn_dash_7days", use_container_width=True):
            st.session_state.dashboard_start_date = datetime.today() - timedelta(days=7)
            st.session_state.dashboard_end_date = datetime.today()
    
    with col2:
        if st.button("This Month", key="btn_dash_thismonth", use_container_width=True):
            st.session_state.dashboard_start_date = datetime.today().replace(day=1)
            st.session_state.dashboard_end_date = datetime.today()
    
    with col3:
        if st.button("All Time", key="btn_dash_alltime", use_container_width=True):
            st.session_state.dashboard_start_date = datetime.today() - timedelta(days=365*5)
            st.session_state.dashboard_end_date = datetime.today()
    
    st.write("")  # Spacing
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "From Date",
            value=st.session_state.get("dashboard_start_date", datetime.today() - timedelta(days=30)),
            key="dashboard_start_date"
        )
    
    with col2:
        end_date = st.date_input(
            "To Date",
            value=st.session_state.get("dashboard_end_date", datetime.today()),
            key="dashboard_end_date"
        )
    
    st.divider()
    
    # ============== 2. FINANCIAL SUMMARY (WITH ENHANCED STATUS) ==============
    st.subheader("💰 Financial Summary")
    
    # Get filtered data
    total_income = fc.get_total_income_by_date_range(str(start_date), str(end_date))
    total_expenses = fc.get_total_expenses_by_date_range(str(start_date), str(end_date))
    balance = fc.get_balance_by_date_range(str(start_date), str(end_date))
    
    # Calculate savings rate with edge case handling
    if total_income > 0:
        savings_rate = (balance / total_income * 100)
        savings_rate_display = f"{savings_rate:.1f}%"
    else:
        savings_rate = 0
        savings_rate_display = "N/A"
    
    # Get status indicator with percentage context
    status_emoji, status_text = fc.get_status(str(start_date), str(end_date))
    if total_income > 0:
        status_display = f"{status_emoji} {status_text} ({savings_rate:.1f}%)"
    else:
        status_display = "⚪ No Income Data"
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("💰 Income", f"₹{total_income:,.2f}")
    
    with col2:
        st.metric("💸 Expenses", f"₹{total_expenses:,.2f}")
    
    with col3:
        st.metric("🟢 Balance", f"₹{balance:,.2f}")
    
    with col4:
        col4_inner1, col4_inner2 = col4.columns([3, 1])
        with col4_inner1:
            st.metric("📊 Savings Rate", savings_rate_display)
        with col4_inner2:
            st.write("")
            st.write("")
            if st.button("ⓘ", key="info_savings_rate", help="Savings Rate = (Balance / Income) × 100"):
                pass
    
    with col5:
        col5_inner1, col5_inner2 = col5.columns([3, 1])
        with col5_inner1:
            st.metric("Status", "")
            st.write(f"**{status_display}**")
        with col5_inner2:
            st.write("")
            st.write("")
            if st.button("ⓘ", key="info_status", help="🟢 ≥20% savings | 🟡 0-20% | 🔴 <0%"):
                pass
    
    st.divider()
    
    # ============== 3. INCOME VS EXPENSE TREND ==============
    st.markdown("### 📊 Income vs Expense Trend")
    
    comparison_chart = ag.create_income_vs_expense_chart()
    if comparison_chart:
        st.pyplot(comparison_chart, use_container_width=True)
    else:
        st.info("📭 No monthly data available for selected period. Add transactions to see trends!")
    
    st.divider()
    
    # ============== 4 & 5. EXPENSE DISTRIBUTION + MEMBER CHART (SIDE BY SIDE) ==============
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("### 🥧 Expense Distribution")
        pie_chart = ag.create_category_pie_chart()
        if pie_chart:
            st.pyplot(pie_chart, use_container_width=True)
        else:
            st.info("📭 No expense data for selected period")
    
    with col_chart2:
        st.markdown("### 👥 Member Comparison")
        member_chart = ag.create_member_comparison_chart()
        if member_chart:
            st.pyplot(member_chart, use_container_width=True)
        else:
            st.info("📭 No member data")
    
    st.divider()
    
    # ============== 6. MEMBER SUMMARY TABLE (COLLAPSIBLE) ==============
    with st.expander("📋 View Member Details"):
        summary = fc.get_member_summary()
        if len(summary) > 0:
            st.dataframe(summary, use_container_width=True, hide_index=True)
        else:
            st.info("📭 No member data available")
    
    st.divider()
    
    # ============== 7. INSIGHTS ==============
    st.subheader("💡 Insights")
    
    # Check if there's data to analyze
    all_income = fc.get_total_income()
    all_expenses = fc.get_total_expenses()
    
    if all_income == 0 and all_expenses == 0:
        st.info("💭 No financial data yet. Start adding members, income, and expenses to see insights!")
    else:
        # Get insights data
        top_earner, top_earner_amount = fc.get_top_earner()
        top_spender, top_spender_amount = fc.get_top_spender()
        top_category, top_category_amount = fc.get_highest_spending_category_with_amount()
        best_month, best_month_savings = fc.get_best_month()
        
        # Calculate average monthly savings for context
        comparison = fc.get_monthly_comparison()
        if len(comparison) > 0:
            comparison["savings"] = comparison["income"] - comparison["expenses"]
            avg_savings = comparison["savings"].mean()
            if avg_savings != 0 and best_month_savings != 0:
                savings_change_pct = ((best_month_savings - avg_savings) / abs(avg_savings)) * 100
                best_month_context = f" ({savings_change_pct:+.0f}% vs avg)"
            else:
                best_month_context = ""
        else:
            best_month_context = ""
        
        # Check for overspending
        overspending_warning = ""
        if all_income > 0 and all_expenses > all_income:
            overspending_pct = ((all_expenses - all_income) / all_income) * 100
            overspending_warning = f"\n\n⚠️ **ALERT:** Total Expenses (₹{all_expenses:,.2f}) exceed Income (₹{all_income:,.2f}) by {overspending_pct:.1f}% - Overspending detected!"
        
        insights_text = (
            f"🏆 **Top Earner:** {top_earner} (₹{top_earner_amount:,.2f})\n\n"
            f"👤 **Top Spender:** {top_spender} (₹{top_spender_amount:,.2f})\n\n"
            f"🔥 **Highest Spending Category:** {top_category} (₹{top_category_amount:,.2f})\n\n"
            f"📈 **Best Month for Savings:** {best_month} (₹{best_month_savings:,.2f}){best_month_context}"
            f"{overspending_warning}"
        )
        
        st.write(insights_text)
