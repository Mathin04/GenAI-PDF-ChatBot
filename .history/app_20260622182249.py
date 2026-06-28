import streamlit as st

st.title(" PDF ChatBot")

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type="pdf"
)

if uploaded_file:
    st.success("PDF Uploaded Successfully!")