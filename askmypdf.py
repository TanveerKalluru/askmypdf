import os
import tempfile

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage


class PDFChat:
    def __init__(self, api_key):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            api_key=api_key,
        )
        self.retriever = None

    def process_pdf(self, uploaded_file):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            pdf_path = tmp.name

        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        chunks = splitter.split_documents(docs)

        if chunks:
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            vector_store = FAISS.from_documents(chunks, embeddings)
            self.retriever = vector_store.as_retriever(
                search_kwargs={"k": 4}
            )

    def ask_question(self, user_input):
        if self.retriever is None:
            return "Please upload a PDF first."

        docs = self.retriever.invoke(user_input)
        context = "\n\n".join([d.page_content for d in docs])

        if not context.strip():
            return "I could not find the answer in the uploaded document."

        prompt = f"""
You are a careful and reliable assistant whose job is to answer questions
ONLY using the information provided in the context below.

Rules you MUST follow:
1. Use ONLY the given context to answer the question.
2. Do NOT use any outside knowledge, assumptions, or prior training.
3. If the answer is not clearly present in the context, say:
   "I could not find the answer in the uploaded document."
4. Do NOT hallucinate or make up details.
5. Keep the answer clear, structured, and easy to understand.
6. If the user asks for a summary, provide a concise but complete summary
   based strictly on the context.
7. If the question is factual, answer precisely.
8. If the question is conceptual, explain it clearly using only the context.

Context (from the uploaded PDF):
--------------------------------
{context}
--------------------------------

User Question:
{user_input}

Now generate the best possible answer strictly following the rules above.
"""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content