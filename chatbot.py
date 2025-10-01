import streamlit as st
import time

# --------------------------
# Simple rule-based chatbot function
# --------------------------
def chatbot_response(user_message: str) -> str:
    user_message = (user_message or "").lower().strip()

    if user_message in ["hi", "hello", "hey", "start"]:
        return "👋 Hello! How can I help you today?"

    elif "create account" in user_message or user_message == "1":
        return "📝 You can create an account here: https://e-tesda.gov.ph/login/signup.php"

    elif "courses" in user_message or user_message == "2":
        return "📦 Sure! Explore the available courses here: https://e-tesda.gov.ph/course"

    elif "talk to agent" in user_message or user_message == "3":
        return "📞 Okay, I’m connecting you to our human support staff."

    elif "assessment" in user_message:   # ✅ fixed (user_message not user_input)
        return """📝 Here’s what you need for assessment:
1. Accomplished application form 👉 [Download here](https://www.tesda.gov.ph/Uploads/File/prescribed%20forms/Assessment%20and%20certification/TESDA-OP-CO-05_Competency_Assessment%20Forms.pdf)  
2. Passport size picture (without name tag)   
3. Assessment fee  
"""

    else:
        return "❓ Sorry, I didn’t understand that. Please choose an option below or type 'help'."

# --------------------------
# Page config and session
# --------------------------
st.set_page_config(page_title="Simple Chatbot", page_icon="🤖", layout="wide")

if "messages" not in st.session_state:
    # messages is a list of tuples: (role, text)
    st.session_state.messages = [("Bot", "👋 Hi! Welcome to TESDA Chatbot. Type 'help' to see options.")]

# last_action will hold a quick-action command when a button is clicked
if "last_action" not in st.session_state:
    st.session_state.last_action = None

# --------------------------
# Sidebar info + reset
# --------------------------
with st.sidebar:
    st.image("logo.png", width=210)  # 🟢 Add logo also in sidebar
    st.title("ℹ️ BSAT Friendly Chatbot")
    st.write("You may ask anything about our Institution. You can:")
    st.markdown("""
    - 👋 Greet the bot  
    - 📝 Create an account  
    - 📦 View courses  
    - 📞 Talk to a human agent  
    - 📝 Ask about assessment  
    """)
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = [("Bot", "👋 Hi! Welcome to TESDA-BSAT Chatbot. Type 'help' to see options.")]
        st.session_state.last_action = None
        st.experimental_rerun()

# --------------------------
# Top title
# --------------------------
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖 TESDA-BSAT Chatbot</h1>", unsafe_allow_html=True)
st.write("Ask me anything about our Institution by typing or using quick action buttons below.")

# --------------------------
# Quick action buttons
# --------------------------
col1, col2, col3, col4 = st.columns(4)
if col1.button("📝 Create Account"):
    st.session_state.last_action = "create account"
if col2.button("📦 Courses"):
    st.session_state.last_action = "courses"
if col3.button("📞 Talk to Agent"):
    st.session_state.last_action = "talk to agent"
if col4.button("📝 Assessment"):
    st.session_state.last_action = "assessment"

# --------------------------
# Determine user_input
# --------------------------
user_input = None

if st.session_state.last_action:
    user_input = st.session_state.last_action
    st.session_state.last_action = None

try:
    if user_input is None:
        chat_in = st.chat_input("Type your message here...")
        if chat_in:
            user_input = chat_in
except Exception:
    if user_input is None:
        if "typed_value" not in st.session_state:
            st.session_state.typed_value = ""
        typed = st.text_input("Type your message here:", value=st.session_state.typed_value, key="typed_value")
        if typed and (len(st.session_state.messages) == 0 or st.session_state.messages[-1] != ("You", typed)):
            user_input = typed

# --------------------------
# Process user input
# --------------------------
if user_input:
    st.session_state.messages.append(("You", user_input))
    with st.spinner("Bot is typing..."):
        time.sleep(0.9)
    try:
        bot_reply = chatbot_response(user_input)
    except Exception as e:
        bot_reply = f"⚠️ An internal error occurred while generating a reply: {e}"
    st.session_state.messages.append(("Bot", bot_reply))
    if "typed_value" in st.session_state:
        st.session_state.typed_value = ""

# --------------------------
# Display conversation (new style)
# --------------------------
for sender, msg in st.session_state.messages:
    if sender == "You":
        st.markdown(
            f"""
            <div style='text-align: right;'>
                <div style='display: inline-block; background-color: #DCF8C6;
                            padding: 10px; border-radius: 15px; margin: 5px;
                            max-width: 70%; text-align: left;'>
                    <b>🧑 You:</b> {msg}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style='text-align: left;'>
                <div style='display: inline-block; background-color: #E6E6FA;
                            padding: 10px; border-radius: 15px; margin: 5px;
                            max-width: 70%; text-align: left;'>
                    <b>🤖 Bot:</b> {msg}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
