import streamlit as st

st.set_page_config(page_title="HTML Test")

st.title("Streamlit Test")

st.markdown(
    "<h1 style='color:red;'>HTML IS WORKING</h1>",
    unsafe_allow_html=True
)

st.html("<h2 style='color:cyan;'>HTML TEST</h2>")