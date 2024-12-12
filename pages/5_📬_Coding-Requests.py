import streamlit as st
import requests

url = "https://script.google.com/macros/s/AKfycbwGjnQozrFcGHyIhKq1j9brAPWBvJT1j6zZjlGOz-T2wANUHnQkNGczuhgdIKdNiRH3/exec"

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

datas = {'link': indicator_link}

if st.button("Submit"):
    if "tradingview.com" in indicator_link.lower():
        response = requests.post(url, data=datas))
        st.success("Request sent successfully!")
        st.write("Response from server:", response)
    else:
        st.warning("Please enter a valid TradingView Indicator link containing 'tradingview.com'.")
