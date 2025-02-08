from alpaca.data.requests import StockTradesRequest
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
import datetime
from alpaca.data.requests import StockQuotesRequest
from alpaca.data.requests import StockLatestTradeRequest
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

client = StockHistoricalDataClient(API_KEY,  API_SECRET)

# Define request parameters
trade_request = StockTradesRequest(
    symbol_or_symbols="AAPL",
    start=datetime.datetime(2024, 2, 1),
    end=datetime.datetime(2024, 2, 1, 10, 0),
    limit=500  # Fetches only 500 trades per request
)

# Define request
latest_trade_request = StockLatestTradeRequest(symbol_or_symbols=["AAPL"])

# Get latest trade price
latest_trade = client.get_stock_latest_trade(latest_trade_request)

# Print the last traded price
print(f"AAPL Last Trade Price: {latest_trade['AAPL'].price}")

# Get historical bid/ask prices
quotes = client.get_stock_trades(trade_request)

# Print the first few quote entries
print(quotes["AAPL"][:5])  # Shows a sample of bid/ask prices
