import streamlit as st

st.set_page_config(layout = "wide")

st.title(":hammer_and_wrench: Andrej S. | InvestorUnknown's Toolbox :hammer_and_wrench:")

st.write("---")

st.write("""
Below is the collection of Indicators I developed for you Gs, feel free to use any of them throughout your journey in Post IMC Levels.
""")

st.write("---")

L1 = st.expander(":chart_with_upwards_trend: Valuation")
L2 = st.expander(":clock12: TPI & Strat-Dev")
L3 = st.expander(":rocket: RSPS")
ot = st.expander(":abacus: Other")

L1.markdown("""
* *[Bitcoin Automated Valuation System](https://www.tradingview.com/script/bVZ3grFX-Bitcoin-Automated-Valuation-System/)*
* *[Sentix Data](https://www.tradingview.com/script/SdtltJSE-BTC-Sentix-Sentiment-Strategic-Bias-Z-Score/)*
* *[Optimized AVIV](https://www.tradingview.com/script/02rBvPSy-AVIV-MVRV-Ratio-Z-Score-Optimized/)*
* *[EMA-Based Cumulative Return Log](https://www.tradingview.com/script/VeLrzbBU-EMA-Based-Cumulative-Return-Log/)*
* *[Moving Average Ratio](https://www.tradingview.com/script/l3LmuHJK-Moving-Average-Ratio-InvestorUnknown/)*            
* *[Bitcoin Power Law Oscillator](https://www.tradingview.com/script/31mh8mTd-Bitcoin-Power-Law-Oscillator-InvestorUnknown/)*
* *[Realized Price Oscillator](https://www.tradingview.com/script/UxC7meAg-Realized-Price-Oscillator-InvestorUnknown/)*
* *[Bitcoin Thermocap](https://www.tradingview.com/script/WdnPvtn7-Bitcoin-Thermocap-InvestorUnknown/)*
* *[Pi Cycle Top & Bottom Indicator](https://www.tradingview.com/script/UCKGuMlC-Pi-Cycle-Top-Bottom-Indicator-InvestorUnknown/)*
""")

L2.markdown("""
* *[Enhanced LNL Trend System](https://www.tradingview.com/script/qm2mnC17-Enhanced-LNL-Trend-System/)*
* *[Adaptive Trend Classification: Moving Averages](https://www.tradingview.com/script/L6NreqzB-Adaptive-Trend-Classification-Moving-Averages-InvestorUnknown/)*
* *[DMI ForLoop](https://www.tradingview.com/script/aoadTINE-DMI-ForLoop-InvestorUnknown/)*    
* *[Fisher ForLoop](https://www.tradingview.com/script/5mnjLS2x-Fisher-ForLoop-InvestorUnknown/)*
* *[Aroon ForLoop](https://www.tradingview.com/script/NMyA2MgX-Aroon-ForLoop-InvestorUnknown/)*
* *[EFI ForLoop](https://www.tradingview.com/script/4FpNcsAs-EFI-ForLoop-InvestorUnknown/)*
* *[ChandeMO ForLoop](https://www.tradingview.com/script/UHrGjJGH-ChandeMO-ForLoop-InvestorUnknown/)*
* *[Infinite Impulse Response Filter ForLoop](https://www.tradingview.com/script/N4Q8sCkm-Infinite-Impulse-Response-Filter-ForLoop-InvestorUnknown/)*
* *[Zero Lag Exponential Moving Average ForLoop](https://www.tradingview.com/script/6PJpu86v-Zero-Lag-Exponential-Moving-Average-ForLoop-InvestorUnknown/)*
* *[Median Kijun-Sen](https://www.tradingview.com/script/EjXXXaVk-Median-Kijun-Sen-InvestorUnknown/)*
* *[Hyperbolic Tangent SuperTrend](https://www.tradingview.com/script/nQHyS5XK-Hyperbolic-Tangent-SuperTrend-InvestorUnknown/)*
* *[Hyperbolic Tangent Volatility Stop](https://www.tradingview.com/script/yM7yGIJ0-Hyperbolic-Tangent-Volatility-Stop-InvestorUnknown/)*
* *[Sine-Weighted MA ATR](https://www.tradingview.com/script/Ku1jOXK0-Sine-Weighted-MA-ATR-InvestorUnknown/)*
* *[Cosine-Weighted MA ATR](https://www.tradingview.com/script/HIsr34CV-Cosine-Weighted-MA-ATR-InvestorUnknown/)*
* *[RSI Weighted Trend System I](https://www.tradingview.com/script/oAlwjKtM-RSI-Weighted-Trend-System-I-InvestorUnknown/)*
""")

L3.markdown("""
* *[Universal Ratio Trend Matrix](https://www.tradingview.com/script/ZCHt0ScM-Universal-Ratio-Trend-Matrix-InvestorUnknown/)*
""")

ot.markdown("""
* *[Central Banks Balance Sheet](https://www.tradingview.com/script/LENP1MRO-InvestorUnknown-Central-Banks-Balance-Sheet/)*
* *[Performance Metrics](https://www.tradingview.com/script/wZzo5T6u-InvestorUnknown-Performance-Metrics/)*    
* *[Asset Drawdown & Drawdown HeatMap](https://www.tradingview.com/script/BlxD6hb3-Asset-Drawdown-Drawdown-HeatMap-InvestorUnknown/)*
""")
