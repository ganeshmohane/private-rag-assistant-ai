import streamlit as st

st.set_page_config(page_title="Private RAG Assistant AI", layout="wide")

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.markdown("<h1 style='text-align: center;'>📄 Private RAG Assistant AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Revolutionize Company Knowledge Access</h3>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align: center; font-size: 18px; margin-top: 30px;">
        <strong>Why?</strong>  
        Most companies store critical data in databases or warehouses, yet much of that knowledge goes unused.  
        Employees waste hours searching through files to answer questions, and when senior staff leave, valuable knowledge walks out the door.
        <br><br>
        <strong>What?</strong>  
        Our solution uses LLMs and Retrieval Augmented Generation (RAG) to let AI learn your company's data — <span style='color: #e67e22'>all on-premise</span>.  
        No reliance on cloud-based AI (like ChatGPT or Gemini): your data stays secure, your knowledge stays in-house.
        <br><br>
        <strong>Who?</strong>  
        Any company can benefit!  
        Empower your teams to instantly get answers from your own VectorDB, leveraging company documents and manuals.
        <br><br>
        <span style='color: #27ae60'><strong>Unlock AI-powered company knowledge — privately, securely, and efficiently.</strong></span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    login_clicked = st.button("Login", use_container_width=True)

    if login_clicked:
        st.switch_page("pages/login_page.py")