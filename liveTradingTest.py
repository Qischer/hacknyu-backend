api_key = None
secret_key = None
paper = True # Please do not modify this. This example is for paper trading only.

trade_api_url = None
trade_api_wss = None
data_api_url = None
stream_data_wss = None
import os

if api_key is None:
    api_key = os.environ.get('API_KEY')

if secret_key is None:
    secret_key = os.environ.get('API_SECRET')

import alpaca
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from alpaca.trading.client import TradingClient
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.historical.corporate_actions import CorporateActionsClient
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.trading.stream import TradingStream
from alpaca.data.live.stock import StockDataStream

from alpaca.data.requests import (
    CorporateActionsRequest,
    StockBarsRequest,
    StockQuotesRequest,
    StockTradesRequest,
)
from alpaca.trading.requests import (
    ClosePositionRequest,
    GetAssetsRequest,
    GetOrdersRequest,
    LimitOrderRequest,
    MarketOrderRequest,
    StopLimitOrderRequest,
    StopLossRequest,
    StopOrderRequest,
    TakeProfitRequest,
    TrailingStopOrderRequest,
)
from alpaca.trading.enums import (
    AssetExchange,
    AssetStatus,
    OrderClass,
    OrderSide,
    OrderType,
    QueryOrderStatus,
    TimeInForce,
)
trade_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=paper, url_override=trade_api_url)

acct = trade_client.get_account()
print(acct)


acct_config = trade_client.get_account_configurations()
print(acct_config)

req = GetAssetsRequest(
  status=AssetStatus.ACTIVE,
  exchange=AssetExchange.NASDAQ,
)

assets = trade_client.get_all_assets(req)
assets[:2]

symbol = "SPY"
# simple, market order, fractional qty
# Alpaca trading platform support fractional trading by default
# you can specify:
# fractional qty (e.g. 0.01 qty) in the order request (which is shown in this example)
# or notional value (e.g. 100 USD) (which is in the next example)
#
# If you have an error of `qty must be integer`,
# please try to `Reset Account` of your paper account via the Alpaca Trading API dashboard
req = MarketOrderRequest(
    symbol = symbol,
    qty = 5.5,
    side = OrderSide.BUY,
    type = OrderType.MARKET,
    time_in_force = TimeInForce.DAY,
)
res = trade_client.submit_order(req)

req = MarketOrderRequest(
    symbol = symbol,
    notional = 1.11,  # notional is specified in USD, here we specify $1.11
    side = OrderSide.BUY,
    type = OrderType.MARKET,
    time_in_force = TimeInForce.DAY,
)
res = trade_client.submit_order(req)

req = LimitOrderRequest(
    symbol = symbol,
    qty = 0.01,
    limit_price = 550.25,
    side = OrderSide.BUY,
    type = OrderType.LIMIT,
    time_in_force = TimeInForce.DAY,
)
res = trade_client.submit_order(req)

req = StopOrderRequest(
                    symbol = symbol,
                    qty = 1,
                    side = OrderSide.BUY,
                    time_in_force = TimeInForce.GTC,
                    stop_price = 600
                    )

res = trade_client.submit_order(req)

req = StopLimitOrderRequest(
                    symbol = symbol,
                    qty = 1,
                    side = OrderSide.BUY,
                    time_in_force = TimeInForce.GTC,
                    limit_price = 550,
                    stop_price = 600
                    )

res = trade_client.submit_order(req)

req = MarketOrderRequest(
                    symbol = symbol,
                    qty = 5,
                    side = OrderSide.BUY,
                    time_in_force = TimeInForce.DAY,
                    order_class = OrderClass.BRACKET,
                    take_profit = TakeProfitRequest(limit_price=600),
                    stop_loss = StopLossRequest(stop_price=300)
)
res = trade_client.submit_order(req)

req = LimitOrderRequest(
                    symbol = symbol,
                    qty = 1,
                    limit_price = 500,
                    side = OrderSide.BUY,
                    time_in_force = TimeInForce.DAY,
                    Class = OrderClass.OTO,
                    stop_loss = StopLossRequest(stop_price = 300)
                    )

res = trade_client.submit_order(req)

req = LimitOrderRequest(
                    symbol = symbol,
                    qty = 1,
                    limit_price = 500,
                    side = OrderSide.BUY,
                    time_in_force = TimeInForce.DAY,
                    Class = OrderClass.OCO
                    )

res = trade_client.submit_order(req)

req = TrailingStopOrderRequest(
                    symbol = symbol,
                    qty = 1,
                    side = OrderSide.SELL,
                    time_in_force = TimeInForce.GTC,
                    trail_percent = 0.20 # you can also use trail_price instead of trail_percent
                    )

res = trade_client.submit_order(req)
req = GetOrdersRequest(
    status = QueryOrderStatus.ALL,
    symbols = [symbol]
)
orders = trade_client.get_orders(req)

req = GetOrdersRequest(
    status = QueryOrderStatus.OPEN,
    symbols = [symbol]
)
open_orders = trade_client.get_orders(req)

trade_client.cancel_orders()

positions = trade_client.get_all_positions()

position = trade_client.get_open_position(symbol_or_asset_id=symbol)

trade_client.get_open_position(symbol_or_asset_id=position.asset_id)

trade_client.close_position(
    symbol_or_asset_id = symbol,
    close_options = ClosePositionRequest(
        qty = "0.01",
    )
)

# subscribe trade updates
trade_stream_client = TradingStream(api_key, secret_key, paper=paper, url_override = trade_api_wss)

async def trade_updates_handler(data):
    print(data)

trade_stream_client.subscribe_trade_updates(trade_updates_handler)
trade_stream_client.run()