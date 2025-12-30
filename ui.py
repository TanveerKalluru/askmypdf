import streamlit as st
import base64
from askmypdf import PDFChat

st.title("Chat with Your PDF")

encoded_key = st.secrets["GOOGLE_API_KEY"]
api_key = base64.b64decode(encoded_key).decode('utf-8')
chat = PDFChat(api_key)

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    chat.process_pdf(uploaded_file)
    st.success("PDF processed successfully!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Ask a question about the PDF")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.text(user_input)

    answer = chat.ask_question(user_input)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
    
    with st.chat_message("assistant"):
        st.text(answer)