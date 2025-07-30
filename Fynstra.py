import streamlit as st
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Fynstra – Financial Health Index", layout="centered")

# Title and header
st.title("⌧ Fynstra")

# Form input container
with st.container(border=True):
    st.subheader("Calculate your FHI Score")
    st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. ")
    st.markdown("Enter the following details:")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Your Age", min_value=18, max_value=100, step=1, help="Your current age in years.")
        monthly_expenses = st.number_input("Monthly Living Expenses (₱)", min_value=0.0, step=50.0,
                                           help="E.g., rent, food, transportation, utilities.")
        monthly_savings = st.number_input("Monthly Savings (₱)", min_value=0.0, step=50.0,
                                          help="The amount saved monthly.")
        emergency_fund = st.number_input("Emergency Fund Amount (₱)", min_value=0.0, step=500.0,
                                         help="For medical costs, job loss, or other emergencies.")

    with col2:
        monthly_income = st.number_input("Monthly Gross Income (₱)", min_value=0.0, step=100.0,
                                         help="Income before taxes and deductions.")
        monthly_debt = st.number_input("Monthly Debt Payments (₱)", min_value=0.0, step=50.0,
                                       help="Loans, credit cards, etc.")
        total_investments = st.number_input("Total Investments (₱)", min_value=0.0, step=500.0,
                                            help="Stocks, bonds, retirement accounts.")
        net_worth = st.number_input("Net Worth (₱)", min_value=0.0, step=500.0,
                                    help="Total assets minus total liabilities.")

# FHI calculation logic
if st.button("Check My Financial Health"):
    if monthly_income == 0 or monthly_expenses == 0:
        st.warning("Please input your income and expenses.")
    else:
        # Age-based target multipliers
        if age < 30:
            alpha, beta = 2.5, 2.0
        elif age < 40:
            alpha, beta = 3.0, 3.0
        elif age < 50:
            alpha, beta = 3.5, 4.0
        else:
            alpha, beta = 4.0, 5.0

        annual_income = monthly_income * 12

        # Sub-scores
        Nworth = min(max((net_worth / (annual_income * alpha)) * 100, 0), 100)
        DTI = 100 - min((monthly_debt / monthly_income) * 100, 100)
        Srate = min((monthly_savings / monthly_income) * 100, 100)
        Invest = min(max((total_investments / (beta * annual_income)) * 100, 0), 100)
        Emerg = min((emergency_fund / monthly_expenses) / 6 * 100, 100)

        # Final FHI Score
        FHI = 0.20 * Nworth + 0.15 * DTI + 0.15 * Srate + 0.15 * Invest + 0.20 * Emerg + 15
        FHI_rounded = round(FHI, 2)
        st.markdown("---")
        # Gauge Chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=FHI_rounded,
            title={"text": "Your FHI Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "salmon"},
                    {'range': [50, 70], 'color': "gold"},
                    {'range': [70, 100], 'color': "lightgreen"}
                ]
            }
        ))

        st.session_state["FHI"] = FHI_rounded
        st.session_state["monthly_income"] = monthly_income
        st.session_state["monthly_expenses"] = monthly_expenses
        st.session_state["current_savings"] = monthly_savings

        fig.update_layout(height=300, margin=dict(t=20, b=20))
        score_col, text_col = st.columns([1, 2])

        with score_col:
            st.plotly_chart(fig, use_container_width=True)

        with text_col:
            st.markdown(f"### Overall FHI Score: *{FHI_rounded}/100*")

            # Identify weak areas
            weak_areas = []
            if Nworth < 60:
                weak_areas.append("net worth")
            if DTI < 60:
                weak_areas.append("debt-to-income ratio")
            if Srate < 60:
                weak_areas.append("savings rate")
            if Invest < 60:
                weak_areas.append("investment levels")
            if Emerg < 60:
                weak_areas.append("emergency fund")

            # Construct weakness text
            weak_text = ""
            if weak_areas:
                if len(weak_areas) == 1:
                    weak_text = f" However, your {weak_areas[0]} needs improvement."
                else:
                    all_but_last = ", ".join(weak_areas[:-1])
                    weak_text = f" However, your {all_but_last} and {weak_areas[-1]} need improvement."

                weak_text += " Addressing this will help strengthen your overall financial health."

            # Final output based on FHI
            if FHI >= 85:
                st.success(f"🎯 Excellent! You’re in great financial shape and well-prepared for the future.{weak_text}")
            elif FHI >= 70:
                st.info(f"🟢 Good! You have a solid foundation. Stay consistent and work on gaps where needed.{weak_text}")
            elif FHI >= 50:
                st.warning(f"🟡 Fair. You’re on your way, but some areas need attention to build a stronger safety net.{weak_text}")
            else:
                st.error(f"🔴 Needs Improvement. Your finances require urgent attention — prioritize stabilizing your income, debt, and savings.{weak_text}")

        # Component interpretations

        st.subheader("📊 Breakdown & Interpretation")

        def interpret(label, score):
            if label == "Net Worth":
                return (
                    "Your *net worth is low* relative to your income." if score < 40 else
                    "Your *net worth is progressing*, but still has room to grow." if score < 70 else
                    "You have a *strong net worth* relative to your income."
                ), [
                    "Build your assets by saving and investing consistently.",
                    "Reduce liabilities such as debts and loans.",
                    "Track your net worth regularly to monitor growth."
                ]
            if label == "Debt-to-Income":
                return (
                    "Your *debt is taking a big chunk of your income*." if score < 40 else
                    "You're *managing debt moderately well*, but aim to lower it further." if score < 70 else
                    "Your *debt load is well-managed*."
                ), [
                    "Pay down high-interest debts first.",
                    "Avoid taking on new unnecessary credit obligations.",
                    "Increase income to improve your ratio."
                ]
            if label == "Savings Rate":
                return (
                    "You're *saving very little* monthly." if score < 40 else
                    "Your *savings rate is okay*, but can be improved." if score < 70 else
                    "You're *saving consistently and strongly*."
                ), [
                    "Automate savings transfers if possible.",
                    "Set a target of saving at least 20% of income.",
                    "Review expenses to increase what's saved."
                ]
            if label == "Investment":
                return (
                    "You're *not investing much yet*." if score < 40 else
                    "You're *starting to invest*; try to boost it." if score < 70 else
                    "You're *investing well* and building wealth."
                ), [
                    "Start small and invest regularly.",
                    "Diversify your portfolio for stability.",
                    "Aim for long-term investing over short-term speculation."
                ]
            if label == "Emergency Fund":
                return (
                    "You have *less than 1 month saved* for emergencies." if score < 40 else
                    "You’re *halfway to a full emergency buffer*." if score < 70 else
                    "✅ Your *emergency fund is solid*."
                ), [
                    "Build up to 3–6 months of essential expenses.",
                    "Keep it liquid and easily accessible.",
                    "Set a monthly auto-save amount."
                ]

        components = {
            "Net Worth": Nworth,
            "Debt-to-Income": DTI,
            "Savings Rate": Srate,
            "Investment": Invest,
            "Emergency Fund": Emerg,
        }

        component_descriptions = {
            "Net Worth": "Your assets minus liabilities — shows your financial position. Higher is better.",
            "Debt-to-Income (DTI)": "Proportion of income used to pay debts. Lower is better.",
            "Savings Rate": "How much of your income you save. Higher is better.",
            "Investment Allocation": "Proportion of assets invested for growth. Higher means better long-term potential.",
            "Emergency Fund": "Covers how well you’re protected in financial emergencies. Higher is better."
        }

        col1, col2 = st.columns(2)
        for i, (label, score) in enumerate(components.items()):
            with (col1 if i % 2 == 0 else col2):
                with st.container(border=True):
                    # Use the more descriptive help text
                    help_text = component_descriptions.get(label, "Higher is better.")
                    st.markdown(f"*{label} Score:* {round(score)} / 100", help=help_text)

                    interpretation, suggestions = interpret(label, score)
                    st.markdown(f"<span style='font-size:13px; color:#444;'>{interpretation}</span>", unsafe_allow_html=True)

                    with st.expander("💡 How to improve"):
                        for tip in suggestions:
                            st.write(f"- {tip}")