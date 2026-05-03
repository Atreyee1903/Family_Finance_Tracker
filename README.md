# 💰 Family Finance Tracker

A professional web-based financial management dashboard built with streamlit for tracking family income, expenses, and financial health with real-time analytics and intelligent insights.

## ✨ Key Features

### 📊 Dashboard
- **5 Key Metrics**: Total income, expenses, balance, savings rate, and health status
- **Smart Status Indicator**: 🟢 Healthy | 🟡 Moderate | 🔴 Overspending | ⚪ No Data
- **Income vs Expense Trends**: Visual comparison with monthly breakdowns
- **Category Analysis**: Pie chart showing spending distribution
- **Member Comparison**: Side-by-side member performance
- **Financial Insights**: Top earner, top spender, best months, overspending alerts
- **Quick Filters**: Last 7 Days, This Month, All Time, Custom Date Range

### 👥 Member Management
- **Add & Delete Members**: Easy family member onboarding
- **Search Functionality**: Quickly find members (scales to 50+ members)
- **Member Overview**: View income, expenses, and balance per member
- **Sort Options**: By name, income, or expense
- **Delete Warnings**: Protects against accidental data loss with transaction alerts
- **Member Insights**: Top earner, highest spender, collective balance

### 💵 Income Tracking
- **Record Earnings**: Date-driven income entry by member
- **Monthly Trends**: Bar chart showing income patterns
- **Income Insights**: Highest entry, best month, average income
- **Smart Filters**: Last 7 Days, This Month, All Time, Reset Filters
- **Income History**: Collapsible table with date sorting
- **Quick Stats**: Total, this month, and today's income

### 💸 Expense Management
- **Multi-Dimensional Tracking**: Category, amount, date, and who paid
- **6 Categories**: Food, Rent, Bills, Transport, Entertainment, Other
- **Dual Analysis**: Category pie chart + monthly trend bar chart
- **Percentage Insights**: See spending distribution (e.g., Food: ₹50K • 40%)
- **Overspending Detection**: Alert with exact excess amount and percentage
- **Smart Filters**: Last 7 Days, This Month, All Time, Reset Filters
- **Expense History**: Comprehensive transaction log with sorting

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Frontend & Backend** | Streamlit | 1.28.1 |
| **Data Processing** | pandas | 2.0.3 |
| **Visualization** | matplotlib | 3.7.2 |
| **Storage** | CSV Files | Native |
| **Currency** | Indian Rupees (₹) | ₹X,XXX.XX format |

## 📁 Project Structure

```
Family finance tracker/
├── app.py                           # 🚀 Main Streamlit application entry point
├── requirements.txt                 # 📦 Python dependencies
│
├── src/                             # 🧠 Core Business Logic (MVC Pattern)
│   ├── data_manager.py             # 💾 CSV operations (CRUD, queries, aggregations)
│   ├── finance.py                  # 🧮 Financial calculations & analysis
│   └── analytics.py                # 📈 Chart generation & visualization
│
├── components/                      # 🎨 UI Components (Streamlit)
│   ├── dashboard.py                # 📊 Main decision-focused dashboard
│   ├── add_member.py               # 👥 Member management interface
│   ├── add_income.py               # 💵 Income tracking interface
│   └── add_expense.py              # 💸 Expense tracking interface
│
├── data/                            # 📂 CSV Storage (Auto-generated)
│   ├── members.csv                 # Family members list
│   ├── earnings.csv                # Income records
│   └── expenses.csv                # Expense records
│
└── README.md                        # 📝 This file
```

## ⚡ Quick Start

### Prerequisites
- **Python 3.11+** (required for Streamlit 1.28.1)
- Windows/macOS/Linux

### Installation

1. **Clone or download the project**:
```bash
cd "Family finance tracker"
```

2. **Create a virtual environment** (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

🌐 Open `http://localhost:8501` in your browser

## 📖 How to Use

### Sidebar Navigation
- **Left Sidebar**: 4-page navigation with quick stats (Members, Total Income, Total Expenses)
- **Default View**: Dashboard opens on startup
- **Switch Tabs**: Single-click navigation between pages

### 1️⃣ Dashboard Tab
- **View Financial Overview**: See total income, expenses, balance in one screen
- **Apply Quick Filters**: Last 7 Days | This Month | All Time | Custom Dates
- **Analyze Trends**: Income vs expense chart shows financial patterns
- **Review Insights**: Discover top earner, top spender, best months
- **Check Status**: 🟢🟡🔴⚪ indicator shows financial health
- **Monitor Alerts**: Get notified if expenses exceed income

### 2️⃣ Add Member Tab
- **Add Members**: Enter family member name → Auto-incremented ID
- **Search Members**: 🔍 Find anyone instantly (handles 50+ members)
- **Sort By**: Name | Income | Expense
- **View Summary**: See each member's income, expenses, balance
- **Delete Members**: ⚠️ Warnings prevent accidental data loss
- **Member Insights**: Top earner, highest spender, collective balance

### 3️⃣ Add Income Tab
- **Record Earnings**: Select member → Amount → Date → Save
- **Quick Filters**: Last 7 Days | This Month | All Time | 🔄 Reset
- **Analyze Trends**: Monthly bar chart shows income patterns
- **View History**: Collapsible table with all income records
- **Income Insights**: Highest entry, best month, average income
- **Track Stats**: Total, this month, today's income at a glance

### 4️⃣ Add Expense Tab
- **Record Expenses**: Category → Amount → Who Paid → Date → Save
- **Smart Filtering**: Last 7 Days | This Month | All Time | 🔄 Reset
- **Expense Categories**: Food | Rent | Bills | Transport | Entertainment | Other
- **Dual Charts**: Category pie + monthly trend analysis
- **View Distribution**: See percentage per category (e.g., Food: 40%)
- **Expense Insights**: Highest category, top spender, overspending alerts with percentages
- **Detect Overspending**: 🔴 Alert shows exact excess and percentage

## ✅ Data Validation & Safety

### Input Validation
| Rule | Implementation | Benefit |
|------|----------------|---------|
| ✓ Positive numbers only | `min_value=0.01` on forms | Prevents invalid entries |
| ✓ No duplicate member names | Check before add | Data integrity |
| ✓ Valid dates required | Date picker widget | Prevents parsing errors |
| ✓ Member must exist | Check before income/expense | Referential integrity |
| ✓ Category selection | Dropdown (not free text) | Consistency |

### Empty State Handling
- ❌ **No members** → Add Member form enabled, Income/Expense forms disabled
- ❌ **No income data** → Shows "No data" message, charts don't break
- ❌ **No expenses** → Smart empty state with helpful message
- ❌ **Date range with no data** → "No records in selected range" message

### Deletion Safety
- ⚠️ **Delete warning**: Shows member's transactions before deletion
- ✅ **Confirmation required**: Two-button confirm/cancel pattern
- 🔄 **Auto-refresh**: Dashboard updates immediately after delete

## 🏗️ Architecture (MVC Pattern)

```
┌─────────────────────────────────────────┐
│         Streamlit UI (View)              │
│  ├─ Dashboard Component                  │
│  ├─ Add Member Component                 │
│  ├─ Add Income Component                 │
│  └─ Add Expense Component                │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│      Business Logic (Controller)         │
│  ├─ FinanceCalculator (calculations)    │
│  ├─ AnalyticsGenerator (charts)         │
│  └─ Navigation & State Management        │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         Data Layer (Model)               │
│  ├─ DataManager (CSV CRUD)              │
│  ├─ Aggregations (queries)              │
│  └─ Persistence (file operations)        │
└──────────────────┬──────────────────────┘
                   │
            ┌──────▼──────┐
            │  CSV Files  │
            │  in /data/  │
            └─────────────┘
```

### Separation of Concerns
- **`src/data_manager.py`**: All CSV operations (280+ lines)
- **`src/finance.py`**: All calculations & analysis (280+ lines)
- **`src/analytics.py`**: All chart generation (120+ lines)
- **`components/*.py`**: Only UI rendering (200+ lines each)
- **`app.py`**: Entry point & navigation (70 lines)

## 📊 Data Schema

### members.csv
```csv
member_id,name
1,Aritra
2,Priya
3,Rohan
```

### earnings.csv
```csv
member_id,amount,date
1,50000.00,2026-05-01
2,40000.00,2026-05-02
1,75000.00,2026-05-03
```

### expenses.csv
```csv
category,amount,date,paid_by
Food,5000.00,2026-05-01,1
Rent,15000.00,2026-05-01,2
Bills,2000.00,2026-05-02,1
```

## 📋 Requirements

All dependencies specified in `requirements.txt`:

```
streamlit==1.28.1
pandas==2.0.3
matplotlib==3.7.2
```

### Why These Versions?
- **Streamlit 1.28.1**: Latest stable with responsive containers
- **pandas 2.0.3**: Performance improvements & datetime handling
- **matplotlib 3.7.2**: Professional chart styling & optimization

## ⚙️ Performance Optimizations

### Responsive Design
- Charts sized for single-screen view (no scrolling)
- Collapsible sections reduce clutter
- Side-by-side layouts maximize space

### Data Efficiency
- Single DataFrame creation, multiple reuse
- Lazy loading with Streamlit caching
- Efficient pandas groupby operations

### User Experience
- Quick filters reduce date picker interactions
- Reset buttons provide instant relief
- Member search scales to 50+ members

## 🎯 Key Highlights

### For Portfolio / Interview
1. **Clean Architecture**: MVC pattern with clear separation of concerns
2. **Professional UI**: Responsive design, smart empty states, helpful messages
3. **Production-Ready**: Edge case handling, validation, error messages
4. **Data Intelligence**: Automatic insights, trend analysis, alerts
5. **User Experience**: Smart filters, search, reset buttons, percentage context
6. **Scalability**: Handles growing data without performance degradation

### Code Quality
- ✅ Type consistency (all floats properly formatted)
- ✅ Session state management (proper state handling)
- ✅ Error handling (no crashes on edge cases)
- ✅ Code organization (modular & maintainable)
- ✅ Documentation (clear comments & docstrings)
- ✅ Testing (validated across all tabs & states)

## 🚀 Usage Examples

### Scenario 1: Track Monthly Family Budget
1. Add family members (Aritra, Priya, Rohan)
2. Record their monthly earnings
3. Log daily expenses by category
4. Dashboard shows total savings & spending percentage
5. Identify top spender & highest expense category

### Scenario 2: Analyze Member Performance
1. Go to Add Member tab
2. Use Sort By feature to see top earner
3. Compare income vs expenses side-by-side
4. Identify who contributes most

### Scenario 3: Monitor Overspending
1. Dashboard status indicator turns 🔴
2. Click Add Expense tab
3. See "🔴 Expenses exceed income by ₹X,XXX (20%)"
4. Review category breakdown to cut costs

## 🤝 Contributing

This project is complete and production-ready. To use as a base:

1. Fork/clone the repository
2. Modify data schema as needed
3. Add new expense categories
4. Extend analytics with new insights
5. Submit improvements via pull requests

## 📝 License

This project is open source and available for personal and commercial use.

---

**Built with ❤️ for family financial management**

*Last updated: May 3, 2026*
