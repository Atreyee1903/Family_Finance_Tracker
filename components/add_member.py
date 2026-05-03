import streamlit as st
import pandas as pd
from src.data_manager import DataManager


def render_add_member(dm: DataManager):
    """Render the Add Member management dashboard with clean structure."""
    
    # Main Title
    st.title("👥 Manage Family Members")
    
    # Load existing members data
    members_df = dm.load_members()
    member_count = len(members_df)
    
    # Build member summary data once
    member_data = []
    total_income = 0
    total_expenses = 0
    
    for _, member in members_df.iterrows():
        member_id = int(member["member_id"])
        name = member["name"]
        income = dm.get_member_income(member_id)
        expenses = dm.get_member_expenses(member_id)
        
        total_income += income
        total_expenses += expenses
        
        member_data.append({
            "ID": member_id,
            "Name": name,
            "Income (₹)": income,
            "Expenses (₹)": expenses,
            "Balance (₹)": income - expenses
        })
    
    # ============== TOP SECTION: METRICS ==============
    st.subheader("📊 Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👥 Total Members", member_count)
    with col2:
        st.metric("💰 Total Income", f"₹{total_income:,.2f}")
    with col3:
        st.metric("💸 Total Expenses", f"₹{total_expenses:,.2f}")
    
    st.divider()
    
    # ============== ADD MEMBER FORM ==============
    st.subheader("➕ Add New Member")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        member_name = st.text_input(
            "Member Name",
            placeholder="Enter family member name...",
            key="member_name_input"
        )
    with col2:
        add_button = st.button("Add Member", key="add_member_btn", use_container_width=True)
    
    if add_button:
        if not member_name or member_name.strip() == "":
            st.error("❌ Member name cannot be empty")
        else:
            if dm.add_member(member_name):
                st.success(f"✅ Member '{member_name}' added successfully!")
                st.rerun()
            else:
                st.error("❌ Member already exists or failed to add")
    
    st.divider()
    
    # Empty state
    if member_count == 0:
        st.info("📭 No members added yet. Add your first family member above!")
        return
    
    # ============== MEMBER TABLE SECTION ==============
    st.subheader("📋 Members List")
    
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    
    with col1:
        search_name = st.text_input(
            "🔍 Search Member",
            placeholder="Type member name...",
            key="search_member_input"
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by:",
            ["Name", "Income", "Expense"],
            key="sort_members"
        )
    
    # Create DataFrame
    summary_df = pd.DataFrame(member_data)
    
    # Apply search filter
    if search_name:
        summary_df = summary_df[summary_df["Name"].str.contains(search_name, case=False, na=False)]
    
    # Apply sorting
    if sort_by == "Name":
        summary_df = summary_df.sort_values("Name")
    elif sort_by == "Income":
        summary_df = summary_df.sort_values("Income (₹)", ascending=False)
    else:  # Expense
        summary_df = summary_df.sort_values("Expenses (₹)", ascending=False)
    
    # Format for display
    display_df = summary_df.copy()
    display_df["Income (₹)"] = display_df["Income (₹)"].apply(lambda x: f"₹{x:,.2f}")
    display_df["Expenses (₹)"] = display_df["Expenses (₹)"].apply(lambda x: f"₹{x:,.2f}")
    display_df["Balance (₹)"] = display_df["Balance (₹)"].apply(lambda x: f"₹{x:,.2f}")
    
    # Display table (remove ID column for cleaner view)
    table_df = display_df[["Name", "Income (₹)", "Expenses (₹)", "Balance (₹)"]].copy()
    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()
    
    # ============== MEMBER ACTIONS ==============
    st.subheader("⚙️ Delete Member")
    
    # Only show delete section if members exist and search returned results
    if len(summary_df) == 0:
        st.info("📭 No members found matching search criteria.")
    else:
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_member = st.selectbox(
                "Select a member to delete:",
                options=summary_df["Name"].tolist(),
                key="member_selector"
            )
        with col2:
            delete_button = st.button("🗑️ Delete", key="delete_member_btn", use_container_width=True)
        
        # Handle delete action
        if delete_button:
            member_id = int(summary_df[summary_df["Name"] == selected_member]["ID"].values[0])
            member_income = summary_df[summary_df["Name"] == selected_member]["Income (₹)"].values[0]
            member_expenses = summary_df[summary_df["Name"] == selected_member]["Expenses (₹)"].values[0]
            
            # Check for associated transactions
            if dm.has_member_transactions(member_id):
                st.warning(
                    f"⚠️ **Warning**: '{selected_member}' has {member_income > 0 and 'income' or ''}"
                    f"{member_income > 0 and member_expenses > 0 and ' and ' or ''}"
                    f"{member_expenses > 0 and 'expense' or ''} records. "
                    f"Deleting may affect your financial data.",
                    icon="⚠️"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Confirm Delete", key="confirm_delete"):
                        dm.delete_member(member_id)
                        st.success(f"✅ Member '{selected_member}' deleted!")
                        st.rerun()
                with col2:
                    if st.button("❌ Cancel", key="cancel_delete"):
                        st.info("Deletion cancelled")
            else:
                dm.delete_member(member_id)
                st.success(f"✅ Member '{selected_member}' deleted!")
                st.rerun()
    
    st.divider()
    
    # ============== MEMBER INSIGHTS ==============
    st.subheader("💡 Member Insights")
    
    # Highest earner
    highest_earner = summary_df.loc[summary_df["Income (₹)"].idxmax()]
    # Highest spender
    highest_spender = summary_df.loc[summary_df["Expenses (₹)"].idxmax()]
    # Total family balance
    total_balance = summary_df["Balance (₹)"].sum()
    
    st.write(
        f"🏆 **Highest Earner:** {highest_earner['Name']} (₹{highest_earner['Income (₹)']:,.2f})\n\n"
        f"💳 **Highest Spender:** {highest_spender['Name']} (₹{highest_spender['Expenses (₹)']:,.2f})\n\n"
        f"⚖️ **Total Family Balance:** ₹{total_balance:,.2f}"
    )
