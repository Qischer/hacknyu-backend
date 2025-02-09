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
    symbol_or_symbols="AAPL",
    timeframe=TimeFrame(1, TimeFrame.Minute),
    start=datetime.datetime(2024, 2, 1, 10),
    end=datetime.datetime(2024, 2, 2, 20),
    limit=50
)

# Define request
stockBars = client.get_stock_bars(barsReq)

avgs = []
openVar = []
highVar = []
lowVar = []
closeVar = []
time = []

for bar in stockBars:
    data = bar[1]
    for symbol_data in data.values():
        for data_point in symbol_data:
            avg = (data_point.high + data_point.low) / 2
            avgs.append(avg)
            openVar.append(data_point.open)
            highVar.append(data_point.high)
            lowVar.append(data_point.low)
            closeVar.append(data_point.close)
            DTM = data_point.timestamp
            time.append(int(DTM.minute) + int(DTM.hour) * (60))

candlestick_fig = go.Figure(data=[go.Candlestick(x=time,
                open=openVar,
                high=highVar,
                low=lowVar,
                close=closeVar)])

arr = np.array(avgs)

output = talib.SMA(arr, 10)

sma_fig = px.line(x=time, y=output)
fig = go.Figure(data=candlestick_fig.data + sma_fig.data)

cash = 100000
stocks = 0
amt = 100

df = pandas.DataFrame({
    "x": [],
    "y": [],
    "color": []  
})

for i in range(len(avgs)):
    if(output[i] != np.nan and output[i] > avgs[i] and (cash - amt * avgs[i] > 10000)):
        stocks += amt
        cash -= amt * avgs[i]
        df.loc[len(df)] = [time[i], avgs[i], "green"]
        print(f"We bought {amt} stocks for {avgs[i]} on {i} because the {output[i]} value")
    elif(output[i] != np.nan and output[i] < avgs[i]):
        cash += stocks * avgs[i]
        stocks = 0
        df.loc[len(df)] = [time[i], avgs[i], "red"]
        print(f"We sold {amt} stocks for {avgs[i]} on {i} because the {output[i]} value")

total = cash + stocks * avgs[-1]

fig.add_scatter(
    x=df["x"],
    y=df["y"],
    mode="markers",
    marker=dict(size=10, color=df["color"]),  # Use the custom colors
    name="Buy/Sell"
)

print(f"started with {100000} got to {total}")
# print(output)
fig.show()
