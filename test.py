from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

# Example stock tickers
STOCK_TICKERS = ["AAPL", "GOOG", "MSFT", "AMZN", "TSLA"]

def simulate_market_data():
    """
    Simulates equity market data with stock tickers, bid price, ask price, and trading volume.
    """
    ticker = random.choice(STOCK_TICKERS)
    bid_price = round(random.uniform(100, 500), 2)
    ask_price = round(bid_price + random.uniform(0.1, 5), 2)
    volume = random.randint(1000, 100000)

    return {
        "ticker": ticker,
        "bid_price": bid_price,
        "ask_price": ask_price,
        "volume": volume,
        "timestamp": time.time()
    }

@app.route("/")
def hello_world():
    return "<p>Hello, this is the Test app!</p>"

@app.route("/start", methods=["GET"])
def simulate():
    """
    Simulate market data and return it as JSON.
    """
    data = simulate_market_data()
    return jsonify({"status": "Success", "data": data}), 200

if __name__ == "__main__":
    app.run(debug=True)