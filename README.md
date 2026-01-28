# BTC-ETH Statistical Arbitrage Strategy 📊💱

This repository implements a market-neutral **pair trading strategy** on BTC and ETH using **statistical arbitrage** techniques. The strategy dynamically estimates the hedge ratio using rolling OLS regression and detects mean-reversion in the spread via z-score thresholds.

---

## 🧠 Strategy Overview

- Constructs a rolling spread:  
  \[
  Spread(t) = BTC(t) − β(t)·ETH(t)
  \]
- Applies z-score thresholds to detect deviations from the spread mean
- Enters long/short positions based on spread divergence
- Exits trades when the spread reverts near its mean
- Simulates PnL with fees

---

## 🔧 Features

- Binance 6-hour OHLCV historical data
- Rolling OLS regression to compute dynamic hedge ratio (β)
- Mean-reversion detection with rolling z-score
- Entry/exit logic using |z-score| > 2. and < 0.5
- Backtest engine with:
  - Realistic fee modeling
  - Cumulative PnL and compounded return
  - Sharpe ratio calculation

---

## 📈 Performance Metrics

- Compounded returns over time
- Trade timing via z-score diagnostics
- ADF stationarity test on spread

---
