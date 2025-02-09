from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
import datetime
from dotenv import load_dotenv
import os
import numpy as np
import talib
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
            time.append(data_point.timestamp)

arrH = np.array(highVar)
arrL = np.array(lowVar)
arrC = np.array(closeVar)
arrO = np.array(openVar)
arrM = np.array(mid)

fastKFrame = 5
fastDframe = 3

fastk, fastd = talib.STOCHF(arrH, arrL, arrC, fastk_period=fastKFrame, fastd_period=fastDframe, fastd_matype=0)

fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.1,
    subplot_titles=("", ""),
    row_heights=[0.4, 0.6]
)

fig.add_trace(go.Candlestick(x=time,
                             open=openVar,
                             high=highVar,
                             low=lowVar,
                             close=closeVar,
                             name="Stock Price"),
              row=2, col=1)

fig.add_trace(go.Scatter(x=time, y=fastk, mode="lines", name="Fast stochastic", line=dict(color="green")),
              row=1, col=1)

fig.add_trace(go.Scatter(x=time, y=fastd, mode="lines", name="Smooth stochastic", line=dict(color="blue")),
              row=1, col=1)

line1 = [80] * len(time)
line2 = [20] * len(time)
fig.add_trace(go.Scatter(x=time, y=line1, mode="lines", name="Upper Threshold", line=dict(color="black", dash="dash")),
              row=1, col=1)
fig.add_trace(go.Scatter(x=time, y=line2, mode="lines", name="Lower Threshold", line=dict(color="black", dash="dash")),
              row=1, col=1)

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

cash = 100000
stocks = 0
amt = 100
ut = 80
lt = 20
repeat = True
buy = False

for i in range(len(mid)):
    if fastk[i] != np.nan and fastk[i] > fastd[i] and fastk[i] < ut and (cash - amt * mid[i] > 10000) and (repeat or not buy):
        stocks += amt
        cash -= amt * mid[i]
        dfBuy.loc[len(dfBuy)] = [time[i], fastk[i], "green"]
        buy = True
    elif fastk[i] != np.nan and fastk[i] < fastd[i] and fastk[i] > lt and (stocks >= amt) and (repeat or buy):
        cash += amt * mid[i]
        stocks -= amt
        dfSell.loc[len(dfSell)] = [time[i], fastk[i], "red"]
        buy = False

fig.add_trace(go.Scatter(
    x=dfBuy["x"], y=dfBuy["y"],
    mode="markers", marker=dict(size=10, color=dfBuy["color"]),
    name="Buy"), row=1, col=1)

fig.add_trace(go.Scatter(
    x=dfSell["x"], y=dfSell["y"],
    mode="markers", marker=dict(size=10, color=dfSell["color"]),
    name="Sell"), row=1, col=1)

fig.update_layout(
    xaxis_title="Time",
    yaxis2_title="Price",
    yaxis_title="Stochastic's",
    showlegend=True,
    title="Stochastic Fast",
)

total = cash + stocks * mid[-1]

print(f"started with {100000} got to {total} ended with {stocks} stocks and {cash} cash")

fig.show()