import streamlit as st
import requests

st.title("📄 Private RAG Assistant AI")

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

# send txt data
if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")
    st.text_area("File Content:", file_content, height=200)

    if st.button("Send to API"):
        files = {"file": ("uploaded.txt", file_content.encode("utf-8"), "text/plain")}
        response = requests.post("http://127.0.0.1:8000/upload_text/", files=files)

        if response.status_code == 200:
            st.success("✅ File content stored successfully!")
        else:
            st.error("❌ Failed to store content")


# fetch embeddings
if st.button("Fetch Existing Embeddings"):
    response = requests.get("http://127.0.0.1:8000/fetch_embeddings/")
    if response.status_code == 200:
        embeddings = response.json()
        st.json(embeddings)
    else:
        st.error("❌ Failed to fetch embeddings")