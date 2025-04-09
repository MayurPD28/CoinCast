import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings

warnings.filterwarnings("ignore")

# -------------------------------
# Helper Functions
# -------------------------------

@st.cache_data
def load_data(symbol: str, start: str):
    df = yf.download(symbol, start=start)
    return df

def test_stationarity(timeseries):
    result = adfuller(timeseries.dropna())
    p_value = result[1]
    return p_value < 0.05  # True if stationary

def train_sarima(data):
    model = SARIMAX(data, order=(2, 1, 2), seasonal_order=(1, 1, 1, 7))
    model_fit = model.fit(disp=False)
    return model_fit

def forecast_prices(model_fit, steps, last_date):
    forecast = model_fit.forecast(steps=steps)
    forecast_index = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=steps)
    forecast = pd.Series(forecast, index=forecast_index)
    return forecast

# -------------------------------
# Streamlit UI
# -------------------------------

st.set_page_config(page_title="CoinCast", layout="wide")
st.title("🪙 CoinCast — Cryptocurrency Price Forecasting with SARIMA")

# Sidebar Inputs
st.sidebar.header("⚙️ Forecast Settings")
symbol = st.sidebar.selectbox("Choose Cryptocurrency", ["BTC-USD", "ETH-USD", "SOL-USD"])
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
steps = st.sidebar.slider("Forecast Horizon (Days)", 7, 90, 30)

# Load Data
data_load_state = st.text("Loading data...")
df = load_data(symbol, str(start_date))
data_load_state.text("✅ Data loaded successfully!")

# Show Raw Data
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.dataframe(df.tail())

# Preprocess
data = df["Close"].dropna()

# Stationarity Check
is_stationary = test_stationarity(data)
st.markdown(f"📉 ADF Stationarity Test: **{'Stationary ✅' if is_stationary else 'Not Stationary ❌'}**")

# Train SARIMA on original data
model_fit = train_sarima(data)

# Forecast
forecast = forecast_prices(model_fit, steps, data.index[-1])

# Plotting
fig, ax = plt.subplots(figsize=(14, 6))
data.plot(ax=ax, label="Historical")
forecast.plot(ax=ax, label="Forecast", color="red")
ax.set_title(f"{symbol} Forecast for Next {steps} Days", fontsize=14)
ax.set_xlabel("Date")
ax.set_ylabel("Price (USD)")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Show forecast values
if st.checkbox("Show Forecasted Values"):
    st.subheader("📈 Forecasted Prices")
    st.dataframe(forecast.round(2).reset_index().rename(columns={"index": "Date", 0: "Price (USD)"}))
