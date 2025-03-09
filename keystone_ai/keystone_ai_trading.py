import alpaca_trade_api as tradeapi
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import time
import os

# ✅ Alpaca API Credentials (Replace with your keys)
API_KEY = "your_alpaca_api_key"
API_SECRET = "your_alpaca_secret_key"
BASE_URL = "https://paper-api.alpaca.markets"  # Use paper trading for testing

# ✅ Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version="v2")

# ✅ AI Parameters
SYMBOL = "AAPL"  # Change this to any stock symbol
SHORT_EMA = 9
LONG_EMA = 21
TRADE_AMOUNT = 10  # Number of shares per trade

# ✅ Fetch historical data
def get_stock_data(symbol, timeframe="5Min", limit=100):
    bars = api.get_barset(symbol, timeframe, limit=limit)
    df = bars[symbol].df
    df["EMA_Short"] = df["close"].ewm(span=SHORT_EMA, adjust=False).mean()
    df["EMA_Long"] = df["close"].ewm(span=LONG_EMA, adjust=False).mean()
    return df

# ✅ AI Model (Reinforcement Learning for Trade Optimization)
def build_ai_model():
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(10, 4)),
        LSTM(50),
        Dense(25, activation="relu"),
        Dense(2, activation="softmax")  # Output: [BUY, SELL]
    ])
    model.compile(optimizer="adam", loss="mse")
    return model

# ✅ Train the AI model on historical market data
def train_ai_model(model, data):
    X = []
    y = []

    for i in range(10, len(data) - 1):
        X.append(data.iloc[i - 10:i][["close", "EMA_Short", "EMA_Long", "volume"]].values)
        if data["EMA_Short"].iloc[i] > data["EMA_Long"].iloc[i]:
            y.append([1, 0])  # Buy
        else:
            y.append([0, 1])  # Sell

    X, y = np.array(X), np.array(y)
    model.fit(X, y, epochs=10, batch_size=8, verbose=1)

# ✅ Execute Trades Based on AI Predictions
def execute_trade(action):
    if action == "BUY":
        api.submit_order(
            symbol=SYMBOL,
            qty=TRADE_AMOUNT,
            side="buy",
            type="market",
            time_in_force="gtc"
        )
        print(f"✅ Bought {TRADE_AMOUNT} shares of {SYMBOL}")
    elif action == "SELL":
        api.submit_order(
            symbol=SYMBOL,
            qty=TRADE_AMOUNT,
            side="sell",
            type="market",
            time_in_force="gtc"
        )
        print(f"✅ Sold {TRADE_AMOUNT} shares of {SYMBOL}")

# ✅ Run AI Trading System
def run_trading():
    model = build_ai_model()

    print("🚀 Training AI Model...")
    data = get_stock_data(SYMBOL, limit=200)
    train_ai_model(model, data)
    print("✅ AI Model Training Complete!")

    while True:
        data = get_stock_data(SYMBOL, limit=50)
        last_10 = np.array([data.iloc[-10:][["close", "EMA_Short", "EMA_Long", "volume"]].values])

        prediction = model.predict(last_10)
        action = "BUY" if np.argmax(prediction) == 0 else "SELL"

        execute_trade(action)
        time.sleep(60)  # Run every minute

# ✅ Run the Trading Bot
if __name__ == "__main__":
    run_trading()
