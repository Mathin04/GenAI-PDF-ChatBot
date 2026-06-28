from dotenv import load_dotenv
import streamlit as st
import tempfile

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

from utils.vector_store import create_vector_store

# -----------------------------
# Load environment
# -----------------------------
load_dotenv()

st.set_page_config(
    page_title="GenAI PDF ChatBot",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_pdf" not in st.session_state:
    st.session_state.uploaded_pdf = None

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

# -----------------------------
# UI Header
# -----------------------------
st.title("📚 GenAI PDF ChatBot")
st.info("Upload a PDF and ask questions from it.")

# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:

    # Reset when new file uploaded
    if st.session_state.uploaded_pdf != uploaded_file.name:
        st.session_state.uploaded_pdf = uploaded_file.name
        st.session_state.messages = []
        st.session_state.qa_chain = None

    # Save file safely (IMPORTANT FIX)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getbuffer())
        pdf_path = tmp.name

    # -----------------------------
    # Build Vector Store (ONLY ONCE)
    # -----------------------------
    if st.session_state.qa_chain is None:

        with st.spinner("Processing PDF... Please wait ⏳"):

            vector_store, total_pages = create_vector_store(pdf_path)

            retriever = vector_store.as_retriever(
                search_type="mmr",
                search_kwargs={
                    "k": 5,
                    "fetch_k": 10,
                    "lambda_mult": 0.7
                }
            )

            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0.3
            )

            st.session_state.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True
            )

            st.session_state.total_pages = total_pages

        st.success("PDF processed successfully!")

    qa_chain = st.session_state.qa_chain

    # -----------------------------
    # Sidebar Info
    # -----------------------------
    st.sidebar.title("📄 PDF Info")
    st.sidebar.write(f"File: {uploaded_file.name}")
    st.sidebar.write(f"Pages: {st.session_state.get('total_pages', 'N/A')}")

    if st.sidebar.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.session_state.qa_chain = None
        st.session_state.uploaded_pdf = None
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.info("Built with LangChain + FAISS + Gemini + Streamlit")

    # -----------------------------
    # Chat History
    # -----------------------------
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown("### 🧑 You")
            st.info(msg["content"])
        else:
            st.markdown("### 🤖 Bot")
            st.success(msg["content"])
            st.markdown("---")

    # -----------------------------
    # Chat Input
    # -----------------------------
    user_question = st.chat_input("Ask something from your PDF...")

    if user_question:

        st.session_state.messages.append({
            "role": "user",
            "content": user_question
        })

        st.markdown("### 🧑 You")
        st.info(user_question)

        with st.spinner("Thinking... 🤔"):

            result = qa_chain.invoke({"query": user_question})
            answer = result["result"]

        st.markdown("### 🤖 Bot")
        st.success(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })