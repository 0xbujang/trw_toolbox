import streamlit as st

def set_background():
    st.markdown("""
        <style>
        .stApp {
            background-color: #1D2B3A;
        }
        </style>
        """, unsafe_allow_html=True)

set_background()

st.set_page_config(
    page_title = "Home"
)

st.title("Main Page")
st.sidebar.success("Select a page above")
