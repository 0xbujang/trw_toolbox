import streamlit as st
import requests

url = "https://script.google.com/macros/s/AKfycbz0h66_RL1U1sEMLgbatnX_t5jKq0LUDdGufubyCdQSSh-oyPXsiTyyeG1sAe5F95ZP/exec"

st.set_page_config(page_title="Coding Requests", layout="wide")

st.markdown("<h1 style='text-align: center;'>Coding Requests</h1>", unsafe_allow_html=True)
st.write("---")
st.markdown("""
<p>
Use the form below to submit links to TradingView indicators you'd like to see with my backtesting library.<br><br>
This integration will enable easier visualization of indicator performance, helping you make more informed optimizations for your Systems.<br><br>
The adjusted codes will be published as private open-source indicators on my TradingView account,<br> links to them will be added to the Tradiview Indicators page under "Request" tab.<br><br>
            
What backtest metrics will be added? You can check here: https://www.tradingview.com/script/3KHj53H2-BacktestLibrary/
</p>
""", unsafe_allow_html=True)

st.write("---")

st.markdown("<h2>TradingView Indicator Submission</h2>", unsafe_allow_html=True)

indicator_link = st.text_input("TradingView Indicator link:")

if st.button("Submit"):
    if "tradingview.com" in indicator_link.lower():
        try:
            # Send the raw link as the POST body with 'text/plain' content type
            headers = {'Content-Type': 'text/plain'}
            response = requests.post(url, data=indicator_link, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    st.success(result.get("message"))
                else:
                    st.warning(result.get("message"))
            else:
                st.error(f"Server returned status code {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid TradingView Indicator link containing 'tradingview.com'.")
