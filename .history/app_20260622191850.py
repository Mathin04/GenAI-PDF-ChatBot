import streamlit as st

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

st.title("📄 PDF ChatBot")

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type="pdf"
)

if uploaded_file:

    st.success("PDF Uploaded Successfully!")

    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    loader = PyPDFLoader(uploaded_file.name)

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(
        documents
    )

    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(
    chunks,
    embeddings
    )

    vector_store.save_local(
    "faiss_index"
    )

    st.success(
    "FAISS Vector Database Created Successfully!"
    )

    test_embedding = embeddings.embed_query(
    chunks[0].page_content
    )

    st.write(
    "Embedding Dimension:",
    len(test_embedding)
    )

    st.write(
        "Number of Pages:",
        len(documents)
    )

    st.write(
        "Number of Chunks:",
        len(chunks)
    )

    st.write(
        chunks[0].page_content
    )