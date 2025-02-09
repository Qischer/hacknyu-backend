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

stock = "AAPL"

barsReq = StockBarsRequest(
    symbol_or_symbols=stock,
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

smaTimeFrame = 10

smas = talib.SMA(arr, smaTimeFrame)

sma_fig = px.line(x=time, y=smas)
fig = go.Figure(data=candlestick_fig.data + sma_fig.data)

cash = 100000
stocks = 0
amt = 100

df = pandas.DataFrame({
    "x": [],
    "y": [],
    "color": []  
})

for i in range(len(mid)):
    if(smas[i] != np.nan and smas[i] > mid[i] and (cash - amt * mid[i] > 10000)):
        stocks += amt
        cash -= amt * mid[i]
        df.loc[len(df)] = [time[i], mid[i], "green"]
        print(f"We bought {amt} stocks for {mid[i]} on {i} because the {smas[i]} value")
    elif(smas[i] != np.nan and smas[i] < mid[i] and (stocks >= amt)):
        cash += amt * mid[i]
        stocks -= amt
        df.loc[len(df)] = [time[i], mid[i], "red"]
        print(f"We sold {amt} stocks for {mid[i]} on {i} because the {smas[i]} value")

fig.add_scatter(
    x=df["x"],
    y=df["y"],
    mode="markers",
    marker=dict(size=10, color=df["color"]),  # Use the custom colors
    name="Buy/Sell"
)

fig.update_layout(
    title="Bollinger Bands Visualization",
    xaxis_title="Time",
    yaxis_title="Price",
    legend=dict(x=0, y=1)
)

total = cash + stocks * mid[-1]


print(f"started with {100000} got to {total} ended with {stocks} stocks and {cash} cash")
# print(smas)
fig.show()