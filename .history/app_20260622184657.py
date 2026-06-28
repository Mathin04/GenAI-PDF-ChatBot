import streamlit as st

from langchain_community.document_loaders import PyPDFLoader

st.title("PDF ChatBot")

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

    st.write(
        "Number of Pages:",
        len(documents)
    )

    st.write(
        documents[0].page_content
    )