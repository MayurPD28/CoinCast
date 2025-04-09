# 🚀 CoinCast – Cryptocurrency Price Forecasting App

CoinCast is an interactive Streamlit-based web application that forecasts cryptocurrency prices using SARIMA (Seasonal ARIMA) time series models. The app retrieves real-time market data via Yahoo Finance, enabling users to generate short- to mid-term forecasts with downloadable results and visual insights.

---

## 📊 Features

- Forecast prices for popular cryptocurrencies (e.g., BTC, ETH)
- Choose forecast range (7 to 90 days)
- View interactive historical and predicted trend graphs
- Download forecast data as CSV
- Clean and responsive Streamlit interface

---

## 🧠 Tech Stack

| Layer         | Tools & Libraries                          |
|---------------|--------------------------------------------|
| Programming   | Python                                     |
| Modeling      | SARIMA (via `statsmodels`)                 |
| Data Source   | `yfinance`                                 |
| Visualization | `matplotlib`, `pandas`, `streamlit`        |
| Deployment    | Streamlit Cloud (optional)                 |

---

## 🚀 Getting Started

### 🔧 Installation

```bash
git clone https://github.com/YOUR_USERNAME/CoinCast.git
cd CoinCast
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
