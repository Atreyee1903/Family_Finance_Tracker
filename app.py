import streamlit as st
from src.data_manager import DataManager
from components.add_member import render_add_member
from components.add_income import render_add_income
from components.add_expense import render_add_expense
from components.dashboard import render_dashboard


# Page configuration
st.set_page_config(
    page_title="Family Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize data manager
dm = DataManager(data_dir="data")

# Sidebar navigation
st.sidebar.title("💰 Family Finance Tracker")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    options=["Dashboard", "Add Member", "Add Income", "Add Expense"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")

# Display quick stats in sidebar
total_members = len(dm.load_members())
st.sidebar.metric("Members", total_members)

total_income = 0
earnings = dm.load_earnings()
if len(earnings) > 0:
    total_income = earnings["amount"].sum()
st.sidebar.metric("Total Income", f"₹{total_income:.2f}")

total_expenses = 0
expenses = dm.load_expenses()
if len(expenses) > 0:
    total_expenses = expenses["amount"].sum()
st.sidebar.metric("Total Expenses", f"₹{total_expenses:.2f}")

# Main content area
st.title("💰 Family Finance Tracker")

if page == "Dashboard":
    render_dashboard(dm)
elif page == "Add Member":
    render_add_member(dm)
elif page == "Add Income":
    render_add_income(dm)
elif page == "Add Expense":
    render_add_expense(dm)
