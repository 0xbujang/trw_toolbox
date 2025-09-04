import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
import plotly.graph_objects as go
import requests


# Layout
st.set_page_config(
    page_title = "TPI Backtest",
    layout = "wide"
)

### FUNCTIONS ###
@st.cache_data(ttl=600)
def get_data_1(sheet_name, print_data):
    url = f'https://script.google.com/macros/s/AKfycbz5mJEV8UeCT4Jn8NAZnj_Poq5OCXQ--E8XNcMK306g8ZDdyFf73p0fMo9YximVmIGK/exec?sheet={sheet_name}'
    response = requests.get(url)
    data = response.json()
    return data[print_data]


@st.cache_data(ttl=600)
def calculate_equities(daily_returns, tpi_data, long_threshold, short_threshold):
    """Calculate strategy and buy-and-hold equities based on daily returns and TPI signals."""
    strategy_equity = [1]  # Starting equity for strategy
    buy_and_hold_equity = [1]  # Starting equity for buy-and-hold
    long_only_equity = [1]

    # Calculate the equity based on signals in 'tpi' column
    for i, signal in enumerate(tpi_data):
        if i < len(daily_returns):
            daily_return = daily_returns[i]

            # Strategy equity update based on 'tpi' signal
            if signal > long_threshold:
                strategy_equity.append(strategy_equity[-1] * (1 + daily_return))  # Long
                long_only_equity.append(long_only_equity[-1] * (1 + daily_return))
            elif signal < short_threshold:
                strategy_equity.append(strategy_equity[-1] * (1 - daily_return))  # Short
                long_only_equity.append(long_only_equity[-1])
            else:
                strategy_equity.append(strategy_equity[-1])  # Neutral/cash
                long_only_equity.append(long_only_equity[-1])

            # Buy-and-hold equity (always long)
            buy_and_hold_equity.append(buy_and_hold_equity[-1] * (1 + daily_return))
        else:
            # If daily returns data is shorter than tpi data
            strategy_equity.append(strategy_equity[-1])
            buy_and_hold_equity.append(buy_and_hold_equity[-1])
            long_only_equity.append(buy_and_hold_equity[-1])

    return strategy_equity, buy_and_hold_equity, long_only_equity

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
        "Evaluates the risk-adjusted performance of a strategy by dividing its excess return over a risk-free rate by the total standard deviation of returns. A higher Sharpe Ratio indicates better risk-adjusted returns. Interpretation: Higher is better.",
        "Focuses on the risk-adjusted performance of a strategy by considering only downside deviation (returns below a specified threshold or target rate). It penalizes strategies more heavily for negative returns. Interpretation: Higher is better.",
        "Compares the probability-weighted ratio of gains versus losses, above and below a specified threshold. It reflects the strategy's potential for gains relative to its risk of losses. Interpretation: Higher is better.",
        "Represents the strategy's excess return over the benchmark after accounting for systematic risk (beta). It quantifies the added value of active management. Interpretation: Higher is better.",
        "Measures the sensitivity of a strategy's returns to movements in the benchmark index. A beta of 1 indicates that the strategy moves in line with the benchmark, while values above or below 1 show higher or lower sensitivity, respectively. Interpretation: A beta closer to 1 is generally better for reducing market-specific risks.",
        "Assesses the efficiency of a strategy in delivering excess returns relative to its tracking error. A higher ratio indicates better performance for the level of active risk taken. Interpretation: Higher is better.",
        "Calculates the risk-adjusted return of a strategy by dividing the annualized return by the maximum drawdown, emphasizing performance in the context of historical drawdowns. Interpretation: Higher is better.",
        "The difference between the strategy's annualized return and the benchmark's annualized return, representing the added return generated by the strategy. Interpretation: Higher is better.",
        "The standard deviation of the return differences between the strategy and the benchmark, reflecting how much the strategy deviates from the benchmark. Interpretation: Lower is better for tracking error as it indicates more consistent alignment with the benchmark.",
        "Represents the average return generated by the strategy on a daily basis. It serves as a simple measure of daily performance. Interpretation: Higher is better.",
        "Indicates the daily volatility of returns, capturing the level of fluctuation in the strategy's performance. Interpretation: Lower is better for reduced risk and steadier performance.",
        "Describes the asymmetry in the distribution of returns. Positive skewness indicates a longer tail on the right (higher gains), while negative skewness reflects a longer tail on the left (higher losses). Interpretation: Higher is generally better as it suggests higher upside potential.",
        "Measures the tendency of return distributions to have tails heavier or lighter than the normal distribution. High excess kurtosis suggests a higher probability of extreme outcomes. Interpretation: Lower is better as it indicates fewer extreme risk events.",
        "The largest peak-to-trough decline in the strategy's equity during a specific time period. It highlights the worst-case loss scenario. Interpretation: Lower is better as it indicates less severe losses.",
        "The compounded annual rate of growth of the strategy over a specified time horizon. It accounts for the impact of reinvestment and is a key performance measure for long-term investments. Interpretation: Higher is better.",
        "The average of all daily returns that are positive, providing insight into the magnitude of gains during up days. Interpretation: Higher is better.",
        "The standard deviation of positive daily returns, capturing the volatility of gains when the strategy performs positively. Interpretation: Lower is better for more consistent positive returns.",
        "The average of all daily returns that are negative, reflecting the severity of losses during down days. Interpretation: Higher (less negative) is better as it indicates less severe losses.",
        "The standard deviation of negative daily returns, indicating the variability in losses during unfavorable performance periods. Interpretation: Lower is better as it shows more consistent losses and reduced risk.",
    ]


    # Dynamically create expanders
    for term, definition in zip(terms, definitions):
        with st.expander(term):
            st.write(definition)


### FUNCTIONS ###

# Title of the dashboard
st.markdown("<h1 style='text-align: center;'>TPI Backtesting Tool</h1>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("<p style='text-align: center;'><strong>No coding required!</strong> A TPI Backtester for students who don't know how to code but want to evaluate the quality of their TPIs.</p>", unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3, = st.columns([3,2,3])

with col2:
    with st.expander("How to Perform TPI Backtest"):
        st.markdown("[Google Doc Guide](https://docs.google.com/document/d/1dS9DTpmEEEeRbB_52zNhCG4EPwN9bedv3R_-P8cA6d4/edit?usp=sharing)")
    

# Input for the sheet name
sheet_name = "R1"

col1a, col2a, col3a = st.columns([4, 2, 4])

# Input for the specific data (daily returns) to use in backtesting
with col2a:
    backtest_for = st.selectbox("Backtest For", options=["total", "btc", "eth", "sol", "ethbtc", "solbtc", "soleth", "others.d"])
    long_thre = st.number_input("Enter Long Threshold", value=0.0, step=0.01, format="%.2f")
    short_thre = st.number_input("Enter Short Threshold", value=0.0, step=0.01, format="%.2f")

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
                strategy_equity, buy_and_hold_equity, long_only_equity = calculate_equities(daily_returns, df['tpi'], long_thre, short_thre)

                # Function to plot the equity chart
                def plot_equity_chart(yaxis_type='linear', title_suffix=''):
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=df['date'], y=strategy_equity[1:], mode='lines', name='Strategy Equity'))
                    fig.add_trace(go.Scatter(x=df['date'], y=long_only_equity[1:], mode='lines', name='Long-Only Equity'))
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
                long_metrics = calculate_metrics(long_only_equity, benchmark_equity=buy_and_hold_equity)
                strat_metrics = calculate_metrics(strategy_equity, benchmark_equity=buy_and_hold_equity)

                # Create DataFrames for metrics
                bah_df = pd.DataFrame.from_dict(bah_metrics, orient='index', columns=['Buy & Hold Metrics'])
                long_df = pd.DataFrame.from_dict(long_metrics, orient='index', columns=['Long-Only Metrics'])
                strat_df = pd.DataFrame.from_dict(strat_metrics, orient='index', columns=['Strategy Metrics'])

                # Combine and display metrics
                combined_metrics = pd.concat([bah_df, long_df, strat_df], axis=1)

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
