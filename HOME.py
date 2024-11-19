import streamlit as st

def set_background():
    st.markdown("""
        <style>
        .stApp {
            background-color: #1D2B3A;
        }
        </style>
        """, unsafe_allow_html=True)

st.set_page_config(
    page_title = "Home",
    layout = "wide"
)

set_background()

st.title("Main Page")
st.sidebar.success("Select a page above")
