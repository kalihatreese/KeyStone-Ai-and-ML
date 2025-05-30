import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='keystone_ai/.env')
from polygon import RESTClient
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ✅ Alpaca API Credentials (Use paper trading keys)
API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = os.getenv("ALPACA_BASE_URL")

# ✅ Initialize Alpaca API
client = RESTClient(os.getenv("POLYGON_API_KEY"))

# ✅ Load Historical Data for Backtesting
def get_historical_data(symbol, timeframe="1Day", limit=1000):
    bars = client.stocks_equities_aggregates(symbol, 1, timeframe.lower(), "2023-01-01", "2025-01-01", unadjusted=False).df
    df = bars[symbol].df
    df["EMA_Short"] = df["close"].ewm(span=9, adjust=False).mean()
    df["EMA_Long"] = df["close"].ewm(span=21, adjust=False).mean()
    return df

# ✅ Simulated Trading Logic
def backtest_strategy(df, initial_balance=10000, trade_size=100):
    balance = initial_balance
    shares = 0
    trade_log = []
    
    for i in range(1, len(df)):
        if df["EMA_Short"].iloc[i] > df["EMA_Long"].iloc[i]:  # BUY Signal
            if balance >= trade_size * df["close"].iloc[i]:
                shares = trade_size
                balance -= shares * df["close"].iloc[i]
                trade_log.append(("BUY", df.index[i], df["close"].iloc[i]))
        elif df["EMA_Short"].iloc[i] < df["EMA_Long"].iloc[i]:  # SELL Signal
            if shares > 0:
                balance += shares * df["close"].iloc[i]
                trade_log.append(("SELL", df.index[i], df["close"].iloc[i]))
                shares = 0
    
    # Final Value Calculation
    final_value = balance + (shares * df["close"].iloc[-1])
    return trade_log, final_value

# ✅ Performance Metrics Calculation
def calculate_performance(trade_log, initial_balance, final_balance):
    total_return = (final_balance - initial_balance) / initial_balance * 100
    win_trades = sum(1 for trade in trade_log if trade[0] == "SELL" and trade[2] > trade_log[trade_log.index(trade) - 1][2])
    total_trades = len([trade for trade in trade_log if trade[0] == "SELL"])
    win_rate = (win_trades / total_trades) * 100 if total_trades > 0 else 0

    print(f"📊 Total Return: {total_return:.2f}%")
    print(f"✅ Winning Trades: {win_trades} / {total_trades} ({win_rate:.2f}%)")

# ✅ Run Backtesting
def run_backtest(symbol):
    print(f"🔍 Running Backtest for {symbol}...")
    df = get_historical_data(symbol)
    trade_log, final_balance = backtest_strategy(df)
    calculate_performance(trade_log, 10000, final_balance)

    # Plot Results
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["close"], label="Stock Price", color="blue")
    plt.plot(df.index, df["EMA_Short"], label="EMA Short", color="green", linestyle="dashed")
    plt.plot(df.index, df["EMA_Long"], label="EMA Long", color="red", linestyle="dashed")

    # Mark buy/sell points
    for trade in trade_log:
        if trade[0] == "BUY":
            plt.scatter(trade[1], trade[2], color="green", marker="^", label="Buy Signal", s=100)
        elif trade[0] == "SELL":
            plt.scatter(trade[1], trade[2], color="red", marker="v", label="Sell Signal", s=100)

    plt.legend()
    plt.title(f"Backtest Results for {symbol}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()

# ✅ Run Backtest for a Specific Stock
if __name__ == "__main__":
    run_backtest("AAPL")  # Backtest on Apple stock

from dotenv import load_dotenv
import os
load_dotenv()

import os
from dotenv import load_dotenv
load_dotenv()

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='keystone_ai/.env')
