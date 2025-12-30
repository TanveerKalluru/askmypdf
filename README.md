# Ask My PDF

A Streamlit-based web application that allows you to chat with your PDF documents using AI-powered retrieval and generation.

## Features

- Upload PDF files
- Ask questions about the content
- AI-powered answers using Google's Gemini model
- Vector-based document search for accurate responses

## Setup

1. Clone or download the repository.

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `secrets.toml` file in a `.streamlit` directory and add your base64-encoded Google AI API key:
   ```
   .streamlit/secrets.toml
   GOOGLE_API_KEY = "base64_encoded_key_here"
   ```
   To encode your API key, you can use an online base64 encoder or run:
   ```
   python -c "import base64; print(base64.b64encode('your_actual_api_key'.encode()).decode())"
   ```
   This adds an extra layer of obfuscation to keep your API key secure.

4. Run the Streamlit application:
```
streamlit run ui.py
```

The app will be available at `http://localhost:8501`.

## Usage

1. Upload a PDF file using the file uploader.
2. Enter your questions in the chat input.
3. Get AI-generated answers based on the PDF content.