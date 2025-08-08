import streamlit as st
from datetime import datetime

def initialize_ai():
    """Initialize AI integration with proper error handling"""
    try:
        import google.generativeai as genai
        AI_AVAILABLE = True
        
        # Get API key from Streamlit secrets only
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            return True, model
        except KeyError:
            st.error("⚠️ GEMINI_API_KEY not found in Streamlit secrets")
            st.info("💡 Add your API key in the Secrets section of your Streamlit Cloud app")
            return False, None
        except Exception as e:
            st.error(f"AI configuration error: {str(e)}")
            return False, None
            
    except ImportError:
        st.warning("Google AI not available. Install with: pip install google-generativeai")
        return False, None

def get_ai_response(user_question, fhi_context, model):
    """Get response from Gemini AI"""
    try:
        # Create detailed prompt with user context
        fhi_score = fhi_context.get('FHI', 'Not calculated')
        income = fhi_context.get('income', 0)
        expenses = fhi_context.get('expenses', 0)
        savings = fhi_context.get('savings', 0)
        
        prompt = f"""
        You are FYNyx, an AI financial advisor specifically designed for Filipino users. You provide practical, culturally-aware financial advice.

        IMPORTANT CONTEXT:
        - User is Filipino, use Philippine financial context
        - Mention Philippine financial products when relevant (SSS, Pag-IBIG, GSIS, BPI, BDO, etc.)
        - Use Philippine Peso (₱) in examples
        - Consider Philippine economic conditions
        - If the question is not financial, politely redirect to financial topics
        
        USER'S FINANCIAL PROFILE:
        - FHI Score: {fhi_score}/100
        - Monthly Income: ₱{income:,.0f}
        - Monthly Expenses: ₱{expenses:,.0f}
        - Monthly Savings: ₱{savings:,.0f}
        
        USER'S QUESTION: {user_question}
        
        INSTRUCTIONS:
        - Provide specific, actionable advice
        - Keep response under 150 words
        - Use friendly, encouraging tone
        - Include specific numbers/percentages when helpful
        - Mention relevant Philippine financial institutions or products if applicable
        - If FHI score is low (<50), prioritize emergency fund and debt reduction
        - If FHI score is medium (50-70), focus on investment and optimization
        - If FHI score is high (>70), discuss advanced strategies
        
        Start your response with a brief acknowledgment of their question, then provide clear advice.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        st.error(f"AI temporarily unavailable: {str(e)}")
        return get_fallback_response(user_question, fhi_context)

def get_fallback_response(user_question, fhi_context):
    """Fallback responses when AI is unavailable"""
    question_lower = user_question.lower()
    fhi_score = fhi_context.get('FHI', 0)
    income = fhi_context.get('income', 0)
    expenses = fhi_context.get('expenses', 0)
    
    # Handle non-financial questions
    if not any(keyword in question_lower for keyword in ['money', 'save', 'invest', 'debt', 'financial', 'emergency', 'retirement', 'income', 'expense', 'fund', 'bank', 'loan']):
        return "I'm FYNyx, your financial advisor! While I can't help with non-financial questions, I'm here to assist with your financial health. Would you like to discuss savings strategies, investments, or debt management instead?"
    
    if "emergency" in question_lower:
        target_emergency = expenses * 6
        monthly_target = target_emergency / 12
        return f"Build an emergency fund of ₱{target_emergency:,.0f} (6 months of expenses). Save ₱{monthly_target:,.0f} monthly to reach this in a year. Keep it in a high-yield savings account like BPI or BDO."
    
    elif "debt" in question_lower:
        if fhi_score < 50:
            return "Focus on high-interest debt first (credit cards, personal loans). Pay minimums on everything, then put extra money toward the highest interest rate debt. Consider debt consolidation with lower rates."
        else:
            return "You're managing debt well! Continue current payments and avoid taking on new high-interest debt. Consider investing surplus funds."
    
    elif "invest" in question_lower or "investment" in question_lower:
        if income < 30000:
            return "Start small with ₱1,000/month in index funds like FMETF or mutual funds from BPI/BDO. Focus on emergency fund first, then gradually increase investments."
        else:
            return "Consider diversifying: 60% stocks (FMETF, blue chips like SM, Ayala), 30% bonds (government treasury), 10% alternative investments. Start with ₱5,000-10,000 monthly."
    
    elif "save" in question_lower or "savings" in question_lower:
        savings_rate = (fhi_context.get('savings', 0) / income * 100) if income > 0 else 0
        target_rate = 20
        if savings_rate < target_rate:
            needed_increase = (target_rate/100 * income) - fhi_context.get('savings', 0)
            return f"Your savings rate is {savings_rate:.1f}%. Aim for 20% (₱{target_rate/100 * income:,.0f}/month). Increase by ₱{needed_increase:,.0f} monthly through expense reduction or income increase."
        else:
            return f"Excellent {savings_rate:.1f}% savings rate! Consider automating transfers and exploring higher-yield options like time deposits or money market funds."
    
    elif "retirement" in question_lower:
        return "Maximize SSS contributions first, then add private retirement accounts. Aim to save 10-15% of income for retirement. Consider PERA (Personal Equity Retirement Account) for tax benefits."
    
    else:
        if fhi_score < 50:
            return "Focus on basics: emergency fund (3-6 months expenses), pay down high-interest debt, and track your spending. Build a solid foundation before investing."
        elif fhi_score < 70:
            return "You're on the right track! Optimize your budget, increase investments gradually, and consider insurance for protection. Review and adjust quarterly."
        else:
            return "Great financial health! Consider advanced strategies: real estate investment, business opportunities, or international diversification. Consult a certified financial planner."

def initialize_session_state():
    """Initialize session state variables"""
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}
    if "calculation_history" not in st.session_state:
        st.session_state.calculation_history = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

# Initialize session state
initialize_session_state()

# Initialize AI
AI_AVAILABLE, model = initialize_ai()

st.subheader("🤖 FYNyx - Your AI Financial Assistant")

# Display chat history (Your existing code for this is fine)
if st.session_state.chat_history:
    st.markdown("### Previous Conversations")
    for i, chat in enumerate(st.session_state.chat_history[-5:]):
        with st.expander(f"Q: {chat['question'][:50]}..." if len(chat['question']) > 50 else f"Q: {chat['question']}"):
            st.markdown(f"**You asked:** {chat['question']}")
            st.markdown(f"**FYNyx replied:** {chat['response']}")
            st.caption(f"Asked on {chat['timestamp']}")
            if 'was_ai_response' in chat:
                st.caption("🤖 AI-powered response" if chat['was_ai_response'] else "🧠 Smart fallback response")

with st.container(border=True):
    st.markdown("Ask FYNyx about your finances and get personalized AI-powered advice!")
    
    st.markdown("**Try asking:**")
    sample_questions = [
        "How can I improve my emergency fund?",
        "What investments are good for beginners in the Philippines?",
        "How should I pay off my debt faster?",
        "What's a good savings rate for someone my age?",
        "Should I invest in stocks or save more first?"
    ]
    
    cols = st.columns(len(sample_questions))
    for i, question in enumerate(sample_questions):
        if cols[i % len(cols)].button(f"💡 {question}", key=f"sample_{i}"):
            st.session_state.user_question = question
            st.session_state.auto_process_question = True
            st.rerun()
    
    user_question = st.text_input(
        "Ask FYNyx:", 
        value=st.session_state.get('user_question', ''),
        placeholder="e.g., How can I improve my emergency fund?",
        key="question_input"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        ask_button = st.button("🚀 Ask FYNyx", type="primary")
    with col2:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()
    
    should_process = ask_button and user_question.strip()
    
    if not should_process and user_question.strip() and st.session_state.get('auto_process_question', False):
        should_process = True
        st.session_state.auto_process_question = False
    
    if should_process:
        with st.spinner("🤖 FYNyx is analyzing your question..."):
            fhi_context = {
                'FHI': st.session_state.get('FHI', 0),
                'income': st.session_state.get('monthly_income', 0),
                'expenses': st.session_state.get('monthly_expenses', 0),
                'savings': st.session_state.get('current_savings', 0)
            }
            
            if AI_AVAILABLE and model:
                response = get_ai_response(user_question, fhi_context, model)
            else:
                response = get_fallback_response(user_question, fhi_context)
            
            # Display response
            st.markdown("### 🤖 FYNyx's Response:")
            st.info(response)
            
            # Save to chat history
            chat_entry = {
                'question': user_question,
                'response': response,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'fhi_context': fhi_context,
                'was_ai_response': AI_AVAILABLE
            }
            st.session_state.chat_history.append(chat_entry)
            
            if 'user_question' in st.session_state:
                del st.session_state.user_question
    
    if st.session_state.chat_history:
        st.markdown("**Quick Actions:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💰 More Savings Tips", key="savings_tip"):
                st.session_state.user_question = "Give me more specific tips to increase my savings rate"
                st.session_state.auto_process_question = True
                st.rerun()
        with col2:
            if st.button("📈 Investment Advice", key="investment_tip"):
                st.session_state.user_question = "What specific investments should I consider for my situation?"
                st.session_state.auto_process_question = True
                st.rerun()
        with col3:
            if st.button("🏦 Debt Strategy", key="debt_tip"):
                st.session_state.user_question = "What's the best strategy for my debt situation?"
                st.session_state.auto_process_question = True
                st.rerun()

if "FHI" in st.session_state:
    st.markdown("---")
    st.markdown("**🎯 FYNyx knows your context:**")
    context_col1, context_col2, context_col3 = st.columns(3)
    with context_col1:
        st.metric("Your FHI", f"{st.session_state['FHI']}")
    with context_col2:
        st.metric("Monthly Income", f"₱{st.session_state.get('monthly_income', 0):,.0f}")
    with context_col3:
        st.metric("Monthly Savings", f"₱{st.session_state.get('current_savings', 0):,.0f}")
