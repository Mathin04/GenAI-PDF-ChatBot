import streamlit as st

from langchain_community.document_loaders import PyPDFLoader

st.title(" PDF ChatBot")

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type="pdf"
)

if uploaded_file:
    st.success("PDF Uploaded Successfully!")