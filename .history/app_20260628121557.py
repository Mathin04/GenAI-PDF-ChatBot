import os
from dotenv import load_dotenv

import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI

# Load API Key
load_dotenv()

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("PDF ChatBot")

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type="pdf"
)

if uploaded_file:

    st.success(f" {uploaded_file.name} uploaded successfully!")

    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load PDF
    loader = PyPDFLoader(uploaded_file.name)
    documents = loader.load()

    # Split Text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    # Create Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create FAISS Database
    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    vector_store.save_local("faiss_index")

    # Create Retriever
    retriever = vector_store.as_retriever()

    # Gemini Model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3
    )

    st.subheader("Ask Questions From PDF")

    # Display Previous Chat Messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown("---")
            st.markdown("### Question")
            st.info(message["content"])
        else:   
            st.markdown("### Answer")
            st.success(message["content"])
            st.markdown("---")
    # Chat Input
    user_question = st.chat_input(
        "Ask a question about the PDF"
    )

    if user_question:

        # Save User Message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        # Show User Message
        st.markdown("---")
        st.markdown("### Question")
        st.info(user_question)

        # Retrieve Relevant Chunks
        retrieved_docs = retriever.invoke(
            user_question
        )

        # Build Context
        context = "\n\n".join(
            [doc.page_content for doc in retrieved_docs]
        )

        # Prompt
        prompt = f"""
You are a helpful PDF assistant.

Answer ONLY using the information present in the PDF context.

If the answer is not available in the PDF, say:

"I could not find this information in the uploaded PDF."

Context:
{context}

Question:
{user_question}
"""

        # Gemini Response
        with st.spinner("Thinking..."):
            response = llm.invoke(prompt)

        # Show Assistant Message
        st.markdown("### Answer")
        st.success(response.content)
        st.markdown("---")

        # Save Assistant Message
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response.content
            }
        )