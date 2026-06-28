from dotenv import load_dotenv
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

from utils.vector_store import create_vector_store

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Session State Initialization
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_pdf" not in st.session_state:
    st.session_state.uploaded_pdf = None

# -----------------------------
# App Title
# -----------------------------
st.title("📚 GenAI PDF ChatBot")
st.caption("Upload a PDF and ask questions using AI")

# -----------------------------
# Upload PDF
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload your PDF",
    type="pdf"
)

if uploaded_file:

    # -----------------------------------
    # Detect New PDF Upload
    # -----------------------------------
    if st.session_state.uploaded_pdf != uploaded_file.name:

        st.session_state.uploaded_pdf = uploaded_file.name

        if "vector_store" in st.session_state:
            del st.session_state.vector_store

        if "total_pages" in st.session_state:
            del st.session_state.total_pages

        st.session_state.messages = []

    # Save PDF
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # -----------------------------------
    # Create Vector Store Only Once
    # -----------------------------------
    if "vector_store" not in st.session_state:

        with st.spinner("Processing PDF... Please wait..."):

            vector_store, total_pages = create_vector_store(
                uploaded_file.name
            )

            st.session_state.vector_store = vector_store
            st.session_state.total_pages = total_pages

        st.success(f"'{uploaded_file.name}' processed successfully!")

    vector_store = st.session_state.vector_store
    total_pages = st.session_state.total_pages

    # -----------------------------------
    # Sidebar
    # -----------------------------------
    st.sidebar.title("GenAI PDF ChatBot")

    st.sidebar.markdown("---")

    st.sidebar.subheader("Uploaded PDF")

    st.sidebar.write(f"**File Name:** {uploaded_file.name}")

    file_size = uploaded_file.size / 1024

    st.sidebar.write(f"**File Size:** {file_size:.2f} KB")

    st.sidebar.write(f"**Pages:** {total_pages}")

    st.sidebar.markdown("---")

    question_count = len(
        [m for m in st.session_state.messages if m["role"] == "user"]
    )

    st.sidebar.subheader("Chat")

    st.sidebar.write(f"Questions Asked: {question_count}")

    if st.sidebar.button("Clear Chat"):

        st.session_state.messages = []

        if "vector_store" in st.session_state:
            del st.session_state.vector_store

        if "total_pages" in st.session_state:
            del st.session_state.total_pages

        st.session_state.uploaded_pdf = None

        st.rerun()

    st.sidebar.markdown("---")

    st.sidebar.info(
        """
GenAI PDF ChatBot

Built using

• LangChain

• Hugging Face

• FAISS

• Gemini 2.5 Flash

• Streamlit
"""
    )

    # -----------------------------------
    # Retriever
    # -----------------------------------
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    # -----------------------------------
    # Gemini Model
    # -----------------------------------
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3
    )

    # -----------------------------------
    # QA Chain
    # -----------------------------------
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    st.subheader("Ask Questions From PDF")

    # -----------------------------------
    # Display Chat History
    # -----------------------------------
    for message in st.session_state.messages:

        if message["role"] == "user":

            st.markdown("---")
            st.markdown("### Question")
            st.info(message["content"])

        else:

            st.markdown("### Answer")
            st.success(message["content"])
            st.markdown("---")

    # -----------------------------------
    # Chat Input
    # -----------------------------------
    user_question = st.chat_input(
        "Ask anything from the uploaded PDF..."
    )

    if user_question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        st.markdown("---")
        st.markdown("### Question")
        st.info(user_question)

        with st.spinner("Thinking..."):

            result = qa_chain.invoke(
                {"query": user_question}
            )

        answer = result["result"]

        st.markdown("### Answer")
        st.success(answer)
        st.markdown("---")

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )