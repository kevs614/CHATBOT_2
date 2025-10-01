import streamlit as st

# -------------------------
# Simple Chatbot Function
# -------------------------
def chatbot_response(user_message: str) -> str:
    user_message = (user_message or "").lower().strip()

    if user_message in ["hi", "hello", "hey"]:
        return "👋 Hello! How can I help you today?"
    elif "help" in user_message:
        return "🛠 Sure! Tell me what you need help with."
    elif "bye" in user_message:
        return "👋 Goodbye! Have a great day."
    else:
        return "🤖 Sorry, I don't understand that yet."


# -------------------------
# Streamlit Config
# -------------------------
st.set_page_config(page_title="Chatbot", page_icon="💬", layout="centered")
st.title("💬 My Chatbot")
st.write("Talk to me like it’s Messenger 😉")

# Add some CSS for chat bubbles
st.markdown("""
<style>
.chat-bubble-user {
    background-color: #DCF8C6;
    padding: 10px;
    border-radius: 15px;
    margin: 5px;
    text-align: right;
}
.chat-bubble-bot {
    background-color: #EDEDED;
    padding: 10px;
    border-radius: 15px;
    margin: 5px;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Conversation Logic
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Type your message:", "")

if st.button("Send"):
    if user_input:
        response = chatbot_response(user_input)
        st.session_state.history.append(("user", user_input))
        st.session_state.history.append(("bot", response))

# Display conversation with bubbles
for sender, text in st.session_state.history:
    if sender == "user":
        st.markdown(f"<div class='chat-bubble-user'>🧑 {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'>🤖 {text}</div>", unsafe_allow_html=True)
