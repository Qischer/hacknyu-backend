from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
import datetime
from dotenv import load_dotenv
import os
import numpy as np
import talib
import plotly.graph_objects as go
import plotly.express as px
import pandas

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

client = StockHistoricalDataClient(API_KEY,  API_SECRET)


barsReq = StockBarsRequest(
    symbol_or_symbols="NRG",
    timeframe=TimeFrame(1, TimeFrame.Minute),
    start=datetime.datetime(2024, 2, 1),
    end=datetime.datetime(2024, 5, 10),
    limit=1000
)

# Define request
stockBars = client.get_stock_bars(barsReq)

mid = []
openVar = []
highVar = []
lowVar = []
closeVar = []
time = []

for bar in stockBars:
    data = bar[1]
    for symbol_data in data.values():
        for data_point in symbol_data:
            middle = (data_point.high + data_point.low) / 2
            mid.append(middle)
            openVar.append(data_point.open)
            highVar.append(data_point.high)
            lowVar.append(data_point.low)
            closeVar.append(data_point.close)
            # DTM = data_point.timestamp
            # time.append(int(DTM.minute) + int(DTM.hour) * (60))
            time.append(data_point.timestamp)


candlestick_fig = go.Figure(data=[go.Candlestick(x=time,
                open=openVar,
                high=highVar,
                low=lowVar,
                close=closeVar)])

arr = np.array(mid)

fastLim = 0.5
slowLim = 0.05

mama, fama = talib.MAMA(arr, fastlimit=fastLim, slowlimit=slowLim)

fig = go.Figure(data=candlestick_fig.data)

fig.add_trace(go.Scatter(x=time, y=arr, mode="lines", name="Price", line=dict(color="blue")))

fig.add_trace(go.Scatter(x=time, y=mama, mode="lines", name="MESA Adaptive Moving Average", line=dict(color="red", dash="dot")))
fig.add_trace(go.Scatter(x=time, y=fama, mode="lines", name="Follow-up Adaptive Moving Average", line=dict(color="green", dash="dot")))

fig.update_layout(
    title="MESA Adaptive Moving Average Visualization",
    xaxis_title="Time",
    yaxis_title="Price",
    legend=dict(x=0, y=1)
)


cash = 100000
stocks = 0
amt = 100
repeat = True
buy = False

dfBuy = pandas.DataFrame({
    "x": [],
    "y": [],
    "color": []  
})

dfSell = pandas.DataFrame({
    "x": [],
    "y": [],
    "color": []  
})

for i in range(len(mid)):
    if(mama[i] != np.nan and mama[i] >= fama[i] and (cash - amt * mid[i] > 10000) and (repeat or not buy)):
        stocks += amt
        cash -= amt * mid[i]
        dfBuy.loc[len(dfBuy)] = [time[i], mid[i], "green"]
        print(f"We bought {amt} stocks for {mid[i]} on {i} because the {mama[i]} value and the {fama[i]} value")
        buy = True
    elif(mama[i] != np.nan and mama[i] <= fama[i] and (stocks >= amt) and (repeat or buy)):
        cash += amt * mid[i]
        stocks -= amt
        dfSell.loc[len(dfSell)] = [time[i], mid[i], "red"]
        print(f"We sold {amt} stocks for {mid[i]} on {i} because the {mama[i]} value and the {fama[i]} value")
        buy = False

fig.add_scatter(
    x=dfBuy["x"],
    y=dfBuy["y"],
    mode="markers",
    marker=dict(size=10, color=dfBuy["color"]),  # Use the custom colors
    name="Buy"
)

fig.add_scatter(
    x=dfSell["x"],
    y=dfSell["y"],
    mode="markers",
    marker=dict(size=10, color=dfSell["color"]),  # Use the custom colors
    name="Sell"
)

total = cash + stocks * mid[-1]


print(f"started with {100000} got to {total} ended with {stocks} stocks and {cash} cash")
fig.show()