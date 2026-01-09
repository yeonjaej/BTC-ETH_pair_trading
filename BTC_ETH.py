import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import statsmodels.api as sm

from binance.client import Client
import time

client = Client(api_key='', api_secret='', tld='us')

def get_binance_data(symbol, interval, start_str, end_str=None):
    df = pd.DataFrame(client.get_historical_klines(symbol, interval, start_str, end_str))
    df = df.iloc[:, :6]
    df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df.astype(float)
    return df

# Pull 30 days of 5-min BTC/ETH data
btc = get_binance_data("BTCUSDT", "6h", "1 June, 2024", "1 March, 2025")
eth = get_binance_data("ETHUSDT", "6h", "1 June, 2024", "1 March, 2025")

btc['close'].plot(label='BTC', figsize=(14,5))
eth['close'].plot(label='ETH')
plt.title('BTC, ETH Prices')
plt.legend()
plt.grid(True)
plt.show()

window = 40  # rolling window in timesteps (e.g., 40*6h ~ 10 days)
betas = []
spreads = []

btc_prices = btc['close']
eth_prices = eth['close']

for i in range(window, len(btc_prices)):
    y = btc_prices.iloc[i - window:i]
    X = eth_prices.iloc[i - window:i]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    beta = model.params.iloc[1]
    betas.append(beta)

    # Use this beta to calculate current spread
    spread = btc_prices.iloc[i] - beta * eth_prices.iloc[i]
    spreads.append(spread)

# Convert to aligned pandas Series
index = btc_prices.index[window:]
spread_series = pd.Series(spreads, index=index)
beta_series = pd.Series(betas, index=index)

spread_mean = spread_series.rolling(50).mean().shift(1) # rolling window: 12.5 days
spread_std = spread_series.rolling(50).std().shift(1)
zscore = (spread_series - spread_mean) / spread_std

plt.figure(figsize=(14,5))
zscore.plot(label='Z-score')
plt.axhline(1.5, color='r', linestyle='--')
plt.axhline(-1.5, color='g', linestyle='--')
plt.axhline(0, color='k', linestyle='-')
plt.title('Z-score of BTC-ETH Spread')
plt.legend()
plt.grid(True)
plt.show()