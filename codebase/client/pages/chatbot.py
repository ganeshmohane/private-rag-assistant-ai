import streamlit as st
import requests

st.set_page_config(page_title="Company Chat Bot", layout="wide")

st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown(
        "<div style='text-align:center;'><h2>🤖 Company Chat Bot</h2></div>",
        unsafe_allow_html=True
    )

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Only keep last 20 messages
    chat_history = st.session_state.chat_history[-20:]

    # Render message bubbles
    for role, msg in chat_history:
        align = "right" if role == "user" else "left"
        bubble_color = "#3498db" if role == "user" else "#27ae60"
        bubble_style = f"""
            float: {align};
            background-color: {bubble_color};
            color: white;
            padding: 12px 18px;
            border-radius: 18px;
            margin: 8px 0px;
            max-width: 65%;
            clear: both;
            font-size: 16px;
        """
        st.markdown(
            f"<div style='{bubble_style}'>{msg}</div>",
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)  # Spacer

    # Message input box
    question = st.text_input("Type your question...", key="chat_input", label_visibility="collapsed")

    send_btn = st.button("Send", use_container_width=True)
    if send_btn and question.strip():
        # Show user message instantly
        st.session_state.chat_history.append(("user", question.strip()))

        api_url = "http://127.0.0.1:8000/chat"
        payload = {"question": question.strip()}
        try:
            response = requests.post(api_url, json=payload, timeout=15)
            if response.status_code == 200:
                bot_reply = response.json().get("answer", "No reply received.")
            else:
                bot_reply = "❌ Error: Could not get answer from server."
        except Exception as e:
            bot_reply = f"❌ Error connecting to backend: {e}"

        st.session_state.chat_history.append(("bot", bot_reply))

        # Clear input box for next message
        # st.session_state.chat_input = ""
        
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)