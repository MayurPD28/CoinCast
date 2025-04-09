# src/forecast.py

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.filterwarnings("ignore")


def download_data(symbol="BTC-USD", start="2020-01-01"):
    df = yf.download(symbol, start=start)
    return df['Close'].dropna()


def test_stationarity(timeseries):
    result = adfuller(timeseries)
    if result[1] > 0.05:
        return timeseries.diff().dropna()
    return timeseries


def train_sarima(data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7)):
    model = SARIMAX(data, order=order, seasonal_order=seasonal_order)
    return model.fit()


def forecast(model_fit, data, steps=30):
    forecast = model_fit.forecast(steps=steps)
    forecast.index = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=steps)
    return forecast


def plot_forecast(data, forecast):
    plt.figure(figsize=(12, 6))
    plt.plot(data, label='Historical')
    plt.plot(forecast, label='Forecast', color='red')
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.title("CoinCast: Crypto Price Forecast")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("forecast_plot.png")
    return "forecast_plot.png"
