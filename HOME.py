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

st.markdown(
"""
<h1 style='text-align: center; color: white;'>
Main Page</h1>
"""
    , unsafe_allow_html=True
)

st.markdown("---")

set_background()

st.markdown(
"""
<p style='text-align: center; color: white;'>
Welcome to the The Real World Cryptocurrency Investing Campus Toolbox.
<br>
<br>
This App is developed and maintained by Andrej S. | 𝓘𝓜𝓒 𝓖𝓾𝓲𝓭𝓮 (01GJBE2DBX7ACHTWS7YSHEFZEW)
</p>
"""
    , unsafe_allow_html=True
)



st.sidebar.success("Select a page above")
