import streamlit as st

st.set_page_config(page_title="Company Login", layout="wide")

col1, col2, col3 = st.columns([1,2,1])

with col2:

    st.markdown("<h1 style='text-align: center;'>🏢 Company Login & Register</h1>", unsafe_allow_html=True)

    email = st.text_input("Company Email", key="email", label_visibility="visible")
    password = st.text_input("Password", type="password", key="password", label_visibility="visible")

    login_clicked = st.button("Login", use_container_width=True)
    if login_clicked:
        st.success("Logged in successfully!")
        st.switch_page("pages/chatbot.py")

    st.markdown("</div>", unsafe_allow_html=True)