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


set_background()


tab1, tab2 = st.tabs(["About", "Update Log"])

with tab1:
    st.markdown(
"""
<p style='text-align: center; color: white;'>
Welcome to The Real World Cryptocurrency Investing Campus Toolbox.
<br>
<br>
This app is developed and maintained by Andrej S. | 𝓘𝓜𝓒 𝓖𝓾𝓲𝓭𝓮 (01GJBE2DBX7ACHTWS7YSHEFZEW)
<br>
<br>
Any student of TRW is welcome to use anything they find useful, but this app is primarily built for IMC graduates.
</p>
"""
    , unsafe_allow_html=True
    )

with tab2:
    st.markdown(
"""
<p style='text-align: left; color: white;'>
22/11/2024 | v1.0 | Added: TPI Backtest Tool Guide
"""
    , unsafe_allow_html=True
    )

st.sidebar.success("Select a page above")
