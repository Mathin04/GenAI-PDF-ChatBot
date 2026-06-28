import streamlit as st

from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

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