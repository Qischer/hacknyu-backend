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
    symbol_or_symbols="MSFT",
    timeframe=TimeFrame(1, TimeFrame.Minute),
    start=datetime.datetime(2024, 2, 1, 10),
    end=datetime.datetime(2024, 2, 2, 20),
    limit=50
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

smaTime = 5
stdUp = 1
stdDown = 1

upperband, middleband, lowerband = talib.BBANDS(arr, timeperiod=smaTime, nbdevup=stdUp, nbdevdn=stdDown, matype=0)

fig = go.Figure(data=candlestick_fig.data)

fig.add_trace(go.Scatter(x=time, y=arr, mode="lines", name="Price", line=dict(color="blue")))

fig.add_trace(go.Scatter(x=time, y=upperband, mode="lines", name="Upper Band", line=dict(color="red", dash="dot")))
fig.add_trace(go.Scatter(x=time, y=middleband, mode="lines", name="Middle Band (SMA)", line=dict(color="black", dash="dash")))
fig.add_trace(go.Scatter(x=time, y=lowerband, mode="lines", name="Lower Band", line=dict(color="green", dash="dot")))

fig.update_layout(
    title="Bollinger Bands Visualization",
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
    if(middleband[i] != np.nan and mid[i] <= lowerband[i] and (cash - amt * mid[i] > 10000) and (repeat or not buy)):
        stocks += amt
        cash -= amt * mid[i]
        dfBuy.loc[len(dfBuy)] = [time[i], mid[i], "green"]
        print(f"We bought {amt} stocks for {mid[i]} on {i} because the {lowerband[i]} value")
        buy = True
    elif(middleband[i] != np.nan and mid[i] >= upperband[i] and (stocks >= amt) and (repeat or buy)):
        cash += amt * mid[i]
        stocks -= amt
        dfSell.loc[len(dfSell)] = [time[i], mid[i], "red"]
        print(f"We sold {amt} stocks for {mid[i]} on {i} because the {upperband[i]} value")
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