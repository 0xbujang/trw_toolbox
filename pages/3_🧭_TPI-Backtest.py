import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
import plotly.graph_objects as go
import requests


def set_background():
    st.markdown("""
        <style>
        .stApp {
            background-color: #1D2B3A;
        }
        </style>
        """, unsafe_allow_html=True)

# Layout
st.set_page_config(
    page_title = "TPI Backtest",
    layout = "wide"
)
set_background()

### FUNCTIONS ###
@st.cache_data(ttl=600)
def get_data_1(sheet_name, print_data):
    url = f'https://script.google.com/macros/s/AKfycbz5mJEV8UeCT4Jn8NAZnj_Poq5OCXQ--E8XNcMK306g8ZDdyFf73p0fMo9YximVmIGK/exec?sheet={sheet_name}'
    response = requests.get(url)
    data = response.json()
    return data[print_data]


@st.cache_data(ttl=600)
def calculate_equities(daily_returns, tpi_data):
    """Calculate strategy and buy-and-hold equities based on daily returns and TPI signals."""
    strategy_equity = [1]  # Starting equity for strategy
    buy_and_hold_equity = [1]  # Starting equity for buy-and-hold

    # Calculate the equity based on signals in 'tpi' column
    for i, signal in enumerate(tpi_data):
        if i < len(daily_returns):
            daily_return = daily_returns[i]

            # Strategy equity update based on 'tpi' signal
            if signal > 0:
                strategy_equity.append(strategy_equity[-1] * (1 + daily_return))  # Long
            elif signal < 0:
                strategy_equity.append(strategy_equity[-1] * (1 - daily_return))  # Short
            else:
                strategy_equity.append(strategy_equity[-1])  # Neutral/cash

            # Buy-and-hold equity (always long)
            buy_and_hold_equity.append(buy_and_hold_equity[-1] * (1 + daily_return))
        else:
            # If daily returns data is shorter than tpi data
            strategy_equity.append(strategy_equity[-1])
            buy_and_hold_equity.append(buy_and_hold_equity[-1])

    return strategy_equity, buy_and_hold_equity

def calculate_metrics(indexed_equity, benchmark_equity=None, risk_free_rate=0.0):
    equity = np.array(indexed_equity)
    daily_returns = np.diff(equity) / equity[:-1]
    
    if benchmark_equity is not None:
        benchmark_returns = np.diff(benchmark_equity) / benchmark_equity[:-1]
    else:
        benchmark_returns = None

    # Positive and negative returns
    positive_returns = daily_returns[daily_returns > 0]
    negative_returns = daily_returns[daily_returns < 0]

    mean_positive = np.mean(positive_returns) if len(positive_returns) > 0 else 0
    std_positive = np.std(positive_returns) if len(positive_returns) > 0 else 0
    mean_negative = np.mean(negative_returns) if len(negative_returns) > 0 else 0
    std_negative = np.std(negative_returns) if len(negative_returns) > 0 else 0

    # Mean and standard deviation of daily returns
    mean_return = np.mean(daily_returns)
    std_dev = np.std(daily_returns)
    downside_returns = negative_returns
    sortino_denominator = np.std(downside_returns) if len(downside_returns) > 0 else 1

    # Annualization factor (252 trading days assumed)
    trading_days_per_year = 252
    annualized_mean = mean_return * trading_days_per_year
    annualized_std_dev = std_dev * np.sqrt(trading_days_per_year)
    annualized_sortino_denominator = sortino_denominator * np.sqrt(trading_days_per_year)

    # Sharpe Ratio (annualized)
    sharpe_ratio = (annualized_mean - risk_free_rate) / annualized_std_dev if annualized_std_dev != 0 else np.nan

    # Sortino Ratio (annualized)
    sortino_ratio = (annualized_mean - risk_free_rate) / annualized_sortino_denominator if annualized_sortino_denominator != 0 else np.nan

    # Omega Ratio
    threshold = 0
    gains = positive_returns
    losses = -negative_returns
    omega_ratio = gains.sum() / losses.sum() if losses.sum() != 0 else np.nan

    # Alpha and Beta
    if benchmark_returns is not None:
        covariance = np.cov(daily_returns, benchmark_returns)[0, 1]
        beta = covariance / np.var(benchmark_returns) if np.var(benchmark_returns) != 0 else np.nan
        annualized_benchmark_mean = np.mean(benchmark_returns) * trading_days_per_year
        alpha = (annualized_mean - risk_free_rate) - (beta * (annualized_benchmark_mean - risk_free_rate))
    else:
        alpha = np.nan
        beta = np.nan

    # Direct excess return for comparison
    if benchmark_returns is not None:
        excess_return = annualized_mean - annualized_benchmark_mean
        tracking_error = np.std(daily_returns - benchmark_returns) * np.sqrt(trading_days_per_year)
        information_ratio = excess_return / tracking_error if tracking_error != 0 else np.nan
    else:
        excess_return = np.nan
        tracking_error = np.nan
        information_ratio = np.nan

    # Skewness and kurtosis
    skewness = skew(daily_returns)
    excess_kurtosis = kurtosis(daily_returns)

    # Max drawdown
    max_drawdown = np.max(np.maximum.accumulate(equity) - equity) / np.maximum.accumulate(equity).max()

    # Calmar Ratio
    calmar_ratio = annualized_mean / max_drawdown if max_drawdown != 0 else np.nan

    # CAGR
    cagr = (equity[-1] / equity[0]) ** (trading_days_per_year / len(daily_returns)) - 1

    metrics = {
        "Sharpe Ratio": sharpe_ratio,
        "Sortino Ratio": sortino_ratio,
        "Omega Ratio": omega_ratio,
        "Alpha": alpha,
        "Beta": beta,
        "Information Ratio": information_ratio,
        "Calmar Ratio": calmar_ratio,
        "Excess Return (Alpha)": excess_return,
        "Tracking Error": tracking_error,
        "Mean Return (Daily)": mean_return,
        "Standard Deviation (Daily)": std_dev,
        "Skewness": skewness,
        "Excess Kurtosis": excess_kurtosis,
        "Max Drawdown": max_drawdown,
        "CAGR (Annualized Return)": cagr,
        "Mean Positive Return (Daily)": mean_positive,
        "Standard Deviation Positive Returns (Daily)": std_positive,
        "Mean Negative Return (Daily)": mean_negative,
        "Standard Deviation Negative Returns (Daily)": std_negative,
    }

    return metrics


def display_metric_explanations():
    """
    Dynamically creates expanders for metrics and their definitions.
    """
    terms = [
        "Sharpe Ratio",
        "Sortino Ratio",
        "Omega Ratio",
        "Alpha",
        "Beta",
        "Information Ratio",
        "Calmar Ratio",
        "Excess Return (Alpha)",
        "Tracking Error",
        "Mean Return (Daily)",
        "Standard Deviation (Daily)",
        "Skewness",
        "Excess Kurtosis",
        "Max Drawdown",
        "CAGR (Annualized Return)",
        "Mean Positive Return (Daily)",
        "Standard Deviation Positive Returns (Daily)",
        "Mean Negative Return (Daily)",
        "Standard Deviation Negative Returns (Daily)",
    ]

    definitions = [
        "Measures risk-adjusted return using total volatility.",
        "Measures risk-adjusted return, focusing on downside volatility.",
        "Ratio of gains to losses above a threshold.",
        "Excess return of the strategy compared to the benchmark after adjusting for beta.",
        "Measures sensitivity of strategy returns to benchmark returns.",
        "Measures excess return per unit of tracking error (strategy's deviation from the benchmark).",
        "Annualized return divided by maximum drawdown, focusing on risk-adjusted return.",
        "Difference between the strategy's annualized return and the benchmark's annualized return.",
        "Volatility of the difference between strategy and benchmark returns.",
        "Average daily return of the strategy.",
        "Volatility of daily returns.",
        "Asymmetry in the distribution of returns.",
        "Measures the tail risk of the returns distribution.",
        "Largest peak-to-trough decline in equity.",
        "Compound annual growth rate of the strategy.",
        "Average of all positive daily returns.",
        "Volatility of positive daily returns.",
        "Average of all negative daily returns.",
        "Volatility of negative daily returns.",
    ]

    # Dynamically create expanders
    for term, definition in zip(terms, definitions):
        with st.expander(term):
            st.write(definition)


### FUNCTIONS ###

# Title of the dashboard
st.markdown("<h1 style='text-align: center; color: white;'>Backtesting Tool - under construction</h1>", unsafe_allow_html=True)


col1, col2, col3, = st.columns([3,2,3])

with col2:
    with st.expander("How to Perform TPI Backtest"):
        st.write("Coming soon...")
    

# Input for the sheet name
sheet_name = "R1"

col1a, col2a, col3a = st.columns([4, 2, 4])

# Input for the specific data (daily returns) to use in backtesting
with col2a:
    backtest_for = st.selectbox("Backtest For", options=["total", "btc", "eth", "sol", "ethbtc", "solbtc", "soleth", "others.d"])

# File upload widget (only accepts CSV files)
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    backtest_trig = st.button("Perform Backtest")

# Button to perform backtest if conditions are met
if backtest_trig:
    if sheet_name and backtest_for and uploaded_file is not None:
        try:
            # Fetch data using the get_data_1 function
            daily_returns_data = get_data_1(sheet_name, backtest_for)
            daily_returns = pd.Series(daily_returns_data)  # Convert to Pandas Series

            # Read the uploaded CSV file
            df = pd.read_csv(uploaded_file)

            # Ensure 'tpi' and 'date' columns exist in the uploaded CSV file
            if 'tpi' in df.columns and 'date' in df.columns:

                # Calculate and cache the equities
                strategy_equity, buy_and_hold_equity = calculate_equities(daily_returns, df['tpi'])

                # Function to plot the equity chart
                def plot_equity_chart(yaxis_type='linear', title_suffix=''):
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=df['date'], y=strategy_equity[1:], mode='lines', name='Strategy Equity'))
                    fig.add_trace(go.Scatter(x=df['date'], y=buy_and_hold_equity[1:], mode='lines', name='Buy and Hold Equity'))

                    # Customize layout with adjustable y-axis type
                    fig.update_layout(
                        title=f"Strategy Equity vs. Buy and Hold Over Time {title_suffix}",
                        xaxis_title="Date",
                        yaxis_title="Equity",
                        legend_title="Equity Curves",
                        yaxis_type=yaxis_type  # Set the y-axis to either linear or log scale
                    )
                    return fig

                # Display both charts side by side
                st.plotly_chart(plot_equity_chart(yaxis_type="linear", title_suffix="(Linear Scale)"))
                st.plotly_chart(plot_equity_chart(yaxis_type='log', title_suffix="(Log Scale)"))

                # Calculate metrics for both strategies and include alpha
                bah_metrics = calculate_metrics(buy_and_hold_equity)
                strat_metrics = calculate_metrics(strategy_equity, benchmark_equity=buy_and_hold_equity)

                # Create DataFrames for metrics
                bah_df = pd.DataFrame.from_dict(bah_metrics, orient='index', columns=['Buy & Hold Metrics'])
                strat_df = pd.DataFrame.from_dict(strat_metrics, orient='index', columns=['Strategy Metrics'])

                # Combine and display metrics
                combined_metrics = pd.concat([bah_df, strat_df], axis=1)

                col1b, col2b = st.columns([1,1])

                with col1b:
                    st.header("Performance Metrics")
                    st.dataframe(combined_metrics.style.format("{:.4f}"), height = 700)
                with col2b:
                    st.header("Metric Explanations")
                    display_metric_explanations()



            else:
                st.error("The uploaded CSV file must contain both 'tpi' and 'date' columns.")
        except Exception as e:
            st.error(f"Error fetching data or processing backtest: {e}")
    else:
        st.warning("Please enter the sheet name, key for daily returns, and upload a CSV file.")
