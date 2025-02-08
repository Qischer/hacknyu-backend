from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = "https://paper-api.alpaca.markets"  # Alpaca Paper Trading URL

trading_client = TradingClient(API_KEY, API_SECRET)

# Get our account information.
account = trading_client.get_account()

# Check if our account is restricted from trading.
if account.trading_blocked:
    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
print('${} is available as buying power.'.format(account.buying_power))

# Check our current balance vs. our balance at the last market close
balance_change = float(account.equity) - float(account.last_equity)
print(f'Today\'s portfolio balance change: ${balance_change}')

search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)

assets = trading_client.get_all_assets(search_params)
# print(assets)

aapl_asset = trading_client.get_asset('AAPL')

if aapl_asset.tradable:
    print('We can trade AAPL.')

def cancel_existing_orders(symbol):
    """Cancel any open orders for a stock before placing a new one."""
    open_orders = trading_client.get_orders()
    for order in open_orders:
        print(f"🚫 Canceling existing order: {order.id}")
        trading_client.cancel_order_by_id(order.id)

# cancel_existing_orders("SPY")


market_order_data = MarketOrderRequest(
                    symbol="SPY",
                    qty=1,
                    side=OrderSide.BUY,
                    type=OrderType.MARKET,
                    time_in_force=TimeInForce.GTC
                    )

# # Market order
market_order = trading_client.submit_order(
                order_data=market_order_data
               )

orders = trading_client.get_orders()  # Fetch last 5 orders
for order in orders:
    print(f"Order ID: {order.id}, Status: {order.status}, Filled Qty: {order.filled_qty}")
