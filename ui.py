import streamlit as st
import base64
from askmypdf import PDFChat

st.title("Chat with Your PDF")

# Decode the base64-encoded API key
encoded_key = st.secrets["AIzaSyC3qjkAfj_5YmFx2DYry7aEx8PPfYcaAVE"]
api_key = base64.b64decode(encoded_key).decode('utf-8')
chat = PDFChat(api_key)

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    chat.process_pdf(uploaded_file)
    st.success("PDF processed successfully!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Ask a question about the PDF")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.text(user_input)

    # Get assistant response
    answer = chat.ask_question(user_input)
    
    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": answer})
    
    # Display assistant message
    with st.chat_message("assistant"):
        st.text(answer)