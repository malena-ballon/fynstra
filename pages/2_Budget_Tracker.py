import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="Budget Tracker", layout="wide")
st.title("💸 Budget Tracker")

# --- SESSION STATE INIT ---
if "budget_entries" not in st.session_state:
    st.session_state.budget_entries = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# --- BUDGET ENTRY FORM ---
st.subheader("➕ Add New Entry")
with st.form("budget_form"):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        entry_date = st.date_input("Date", value=date.today())

    with col2:
        entry_type = st.selectbox("Type", ["Income", "Expense"])

    with col3:
        category_options = ["Food", "Transportation", "Bills", "Shopping", "Entertainment", "Health", "Savings", "Others", "➕ Add new..."]
        selected = st.selectbox("Category", category_options)

        if selected == "➕ Add new...":
            new_category = st.text_input("New Category")
            category = new_category if new_category else "Others"
        else:
            category = selected

    with col4:
        amount = st.number_input("Amount", min_value=0.0, step=1.0)

    submitted = st.form_submit_button("Add Entry")
    if submitted:
        new_entry = {
            "date": entry_date,
            "type": entry_type,
            "category": category,
            "amount": amount
        }

        if st.session_state.edit_index is not None:
            st.session_state.budget_entries[st.session_state.edit_index] = new_entry
            st.session_state.edit_index = None
            st.success("✅ Entry updated!")
        else:
            st.session_state.budget_entries.append(new_entry)
            st.success("✅ Entry added!")

# --- IF THERE ARE ENTRIES ---
if st.session_state.budget_entries:
    df = pd.DataFrame(st.session_state.budget_entries)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date", ascending=False)

    st.subheader("📊 Budget Summary")
    total_income = df[df["type"] == "Income"]["amount"].sum()
    total_expense = df[df["type"] == "Expense"]["amount"].sum()
    net_savings = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₱{total_income:,.2f}")
    col2.metric("Total Expenses", f"₱{total_expense:,.2f}")
    col3.metric("Net Savings", f"₱{net_savings:,.2f}")

    st.subheader("📈 Visual Breakdown")
    col4, col5 = st.columns(2)

    with col4:
        expense_df = df[df["type"] == "Expense"]
        if not expense_df.empty:
            pie = px.pie(expense_df, values="amount", names="category", title="Expenses by Category")
            st.plotly_chart(pie, use_container_width=True)
        else:
            st.info("No expenses to show.")

    with col5:
        df_by_date = df.groupby(["date", "type"])["amount"].sum().reset_index()
        bar = px.bar(df_by_date, x="date", y="amount", color="type", barmode="group", title="Daily Income vs Expenses")
        st.plotly_chart(bar, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧾 Transactions")
        for i, entry in df.iterrows():
            with st.expander(f"{entry['date'].strftime('%Y-%m-%d')} | {entry['type']} | {entry['category']} | ₱{entry['amount']:,.2f}"):
                colA, colB = st.columns(2)
                if colA.button("✏️ Edit", key=f"edit_{i}"):
                    st.session_state.edit_index = i
                    # preload values
                    st.experimental_rerun()
                if colB.button("❌ Delete", key=f"delete_{i}"):
                    st.session_state.budget_entries.pop(i)
                    st.experimental_rerun()

    with col2:
        st.subheader("📂 Expense Breakdown")
        if not expense_df.empty:
            breakdown = expense_df.groupby("category")["amount"].sum().reset_index()
            st.dataframe(breakdown)
        else:
            st.info("No expenses recorded yet.")

else:
    st.info("No entries yet. Add your income or expenses above.")

# --- FUTURE BANK INTEGRATION ---
st.markdown("---")
st.subheader("🏦 Bank Integration (Coming Soon)")
st.markdown("""
Sync your budget tracker directly with BPI’s online system.

✅ Auto-track your transactions  
✅ Real-time budget suggestions  
✅ Safer, smarter saving
🔒 This feature is part of our future roadmap to integrate with banks for automated budget tracking and financial health analysis.
.
""")
You sent
import streamlit as st

st.title("Dashboard")

st.subheader("To finalize what insights to display hhahha")
You sent
import streamlit as st, uuid, math
from datetime import date

st.title("Goal Tracker")

# Required session data
required_keys = ["FHI", "monthly_income", "monthly_expenses", "current_savings"]
if any(key not in st.session_state for key in required_keys):
        st.warning("⚠️ Please complete the homepage first.")
        st.stop()

# Initialize session state
if "goals" not in st.session_state:
    st.session_state.goals = {}
if "selected_goal" not in st.session_state:
    st.session_state.selected_goal = None

# Common emoji options
emoji_options = ["🎯", "💰", "🏠", "🚗", "🎓", "✈️", "💼", "❤️", "📚", "🛍️", "📈", "🎁"]

# Add new goal
if st.button("➕ Add New Goal"):
    goal_id = str(uuid.uuid4())
    st.session_state.goals[goal_id] = {
        "name": f"New Goal {len(st.session_state.goals)+1}",
        "goal_amount": 1000.0,
        "target_date": date.today(),
        "use_recommended_fhi": True,
        "emoji": "🎯",
    }
    st.session_state.selected_goal = goal_id

# Show list of goals with status
st.subheader("Your Goals")

goals = list(st.session_state.goals.items())
num_goals = len(goals)
cols_per_row = 4
num_rows = math.ceil(num_goals / cols_per_row)

for i in range(num_rows):
    row_goals = goals[i * cols_per_row: (i + 1) * cols_per_row]
    cols = st.columns(cols_per_row)
    
    for col, (goal_id, goal) in zip(cols, row_goals):
        with col:
            # Calculate on-track status
            target_date = goal.get("target_date", date.today())
            goal_amount = goal.get("goal_amount", 1000.0)
            current_savings = st.session_state.get("current_savings", 0)
            monthly_income = st.session_state.get("monthly_income", 0)
            monthly_expenses = st.session_state.get("monthly_expenses", 0)
            FHI = st.session_state.get("FHI", 0)
            min_fhi = FHI if goal.get("use_recommended_fhi", True) else 50  # Or your default

            today = date.today()
            delta = target_date - today
            months = max(delta.days // 30, 1)
            remaining_amount = max(goal_amount - current_savings, 0)
            required_monthly_saving = remaining_amount / months
            available_to_save = max(monthly_income - monthly_expenses, 0)

            on_track = required_monthly_saving <= available_to_save and FHI >= min_fhi

            # Display goal card
           # Display goal card
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style='text-align: left;'>
                        <div style='font-size: 2rem'>{goal.get('emoji', '🎯')}</div>
                        <div style='font-size: 1.2rem; font-weight: bold;'>{goal['name']}</div>
                        <div style='color: {'green' if on_track else 'red'}; margin-bottom: 0.5rem;'>
                            {'✅ On track' if on_track else '🚨 Not on track'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True
                )

                # Left-aligned View button
                if st.button("View", key=f"view_{goal_id}"):
                    st.session_state.selected_goal = goal_id
                    st.rerun()


# Show goal details if one is selected
if st.session_state.selected_goal:
    goal = st.session_state.goals[st.session_state.selected_goal]

    st.markdown("---")
    with st.container(border=True):
        # Goal name input
        goal_name = st.text_input("✏️ Goal Name", value=goal["name"], key="goal_name_input")

        # Emoji picker buttons
        st.markdown("🌟 *Choose an Emoji Icon*")
        current_emoji = goal.get("emoji", "🎯")
        selected_emoji = current_emoji

        emoji_cols = st.columns(6)
        for i, icon in enumerate(emoji_options):
            if emoji_cols[i % 6].button(icon, key=f"emoji_{icon}"):
                selected_emoji = icon

        # Save selected emoji and goal name
        st.session_state.goals[st.session_state.selected_goal]["emoji"] = selected_emoji
        st.session_state.goals[st.session_state.selected_goal]["name"] = goal_name

        

        # Target amount and date
        col1, col2 = st.columns(2)
        with col1:
            goal_amount = st.number_input("💰 Target Amount (₱)", min_value=1000.0, step=1000.0, format="%.2f", key="goal_amount_input")
        with col2:
            target_date = st.date_input("📅 Target Date", min_value=date.today(), key="target_date_input")

        st.session_state.goals[st.session_state.selected_goal]["goal_amount"] = goal_amount
        st.session_state.goals[st.session_state.selected_goal]["target_date"] = target_date

        # Financial Health Setting
        st.markdown("#### Financial Health Setting")
        use_recommended_fhi = st.checkbox(
            f"Use your current FHI ({st.session_state.get('FHI', 0)})",
            value=goal.get("use_recommended_fhi", True),
            key="use_recommended_fhi_input"
        )
        st.session_state.goals[st.session_state.selected_goal]["use_recommended_fhi"] = use_recommended_fhi

        min_fhi = (st.session_state.get("FHI", 0) if use_recommended_fhi else
                   st.slider("Set your own minimum FHI to maintain", 0, 100, int(st.session_state.get("FHI", 0))))


        FHI = st.session_state["FHI"]
        monthly_income = st.session_state["monthly_income"]
        monthly_expenses = st.session_state["monthly_expenses"]
        current_savings = st.session_state["current_savings"]

        # Compute feasibility
        today = date.today()
        delta = target_date - today
        months = max(delta.days // 30, 1)
        remaining_amount = max(goal_amount - current_savings, 0)
        required_monthly_saving = remaining_amount / months
        available_to_save = max(monthly_income - monthly_expenses, 0)
    
    with st.container(border=True):
        # Status check
        st.subheader("Status Check")
        if required_monthly_saving <= available_to_save and FHI >= min_fhi:
            st.success(f"✅ You're on track! Save ₱{required_monthly_saving:,.2f} per month by {target_date}.")
        else:
            st.error("🚨 You're not on track.")
            st.markdown(f"💡 Need to save: ₱{required_monthly_saving:,.2f}/month")
            st.markdown(f"⚠️ Can only save: ₱{available_to_save:,.2f}/month")

            st.markdown("#### Suggestions:")
            suggestions = []
            if FHI < min_fhi:
                suggestions.append("- Improve your FHI by reducing debt or increasing savings.")
            if monthly_expenses > 0.5 * monthly_income:
                suggestions.append("- Reduce non-essential expenses.")
            if current_savings == 0:
                suggestions.append("- Start an emergency fund.")
            suggestions.append("- Extend your goal deadline.")
            suggestions.append("- Increase your income (e.g., side hustles).")

            for s in suggestions:
                st.write(s)

    if st.button("💾 Save Goal"):
        st.session_state.goals[st.session_state.selected_goal]["name"] = st.session_state.get("goal_name_input", goal["name"])
        st.session_state.selected_goal = None
        st.rerun()