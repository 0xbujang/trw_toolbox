import streamlit as st

st.set_page_config(
    page_title = "TV Indicators",
    layout = "wide"
)

st.markdown("<h1 style='text-align: center;'>Andrej S. | InvestorUnknown's Toolbox</h1>", unsafe_allow_html=True)

Valuation, Tpi, Rsps, Other, Req = st.tabs(["Valuation", "TPI & Strat Dev", "RSPS", "Other", "Requests"]) 

Valuation.markdown("""
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

Tpi.markdown("""
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
* *[Z-Score Weighted Trend System I](https://www.tradingview.com/script/jKvaojB0-Z-Score-Weighted-Trend-System-I-InvestorUnknown/)*
* *[RBF Kijun Trend System](https://www.tradingview.com/script/KLKOA9hY-RBF-Kijun-Trend-System-InvestorUnknown/)*
* *[TrigWave Suite](https://www.tradingview.com/script/V8FTemnA-TrigWave-Suite-InvestorUnknown/)* 
* *[MA Ratio Weighted Trend System I](https://www.tradingview.com/script/7ARqNdTn-MA-Ratio-Weighted-Trend-System-I-InvestorUnknown/)*
* *[MadTrend](https://www.tradingview.com/script/nhyCYGKn-MadTrend-InvestorUnknown/)*
* *[AadTrend](https://www.tradingview.com/script/cIyhGm6c-AadTrend-InvestorUnknown/)*
* *[CauchyTrend](https://www.tradingview.com/script/XuPnhy3w-CauchyTrend-InvestorUnknown/)*
* *[Median Deviation Suite](https://www.tradingview.com/script/jhoPkiLx-Median-Deviation-Suite-InvestorUnknown/)*
""")

Rsps.markdown("""
* *[Universal Ratio Trend Matrix](https://www.tradingview.com/script/ZCHt0ScM-Universal-Ratio-Trend-Matrix-InvestorUnknown/)*
""")

Other.markdown("""
* *[Central Banks Balance Sheet](https://www.tradingview.com/script/LENP1MRO-InvestorUnknown-Central-Banks-Balance-Sheet/)*
* *[Performance Metrics](https://www.tradingview.com/script/wZzo5T6u-InvestorUnknown-Performance-Metrics/)*    
* *[Asset Drawdown & Drawdown HeatMap](https://www.tradingview.com/script/BlxD6hb3-Asset-Drawdown-Drawdown-HeatMap-InvestorUnknown/)*
""")

Req.markdown("""
* *[Normalized KAMA Oscillator | IkkeOmar](https://www.tradingview.com/script/6G8VDt6p-Normalized-KAMA-Oscillator-IkkeOmar-BLv2/)* 
* *[Squeeze Momentum Indicator](https://www.tradingview.com/script/IDOs0ebZ-Squeeze-Momentum-Indicator-LazyBear-BLv2/)* 
""")
