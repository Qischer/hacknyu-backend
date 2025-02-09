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
import plotly.io as pio
import pandas

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

client = StockHistoricalDataClient(API_KEY,  API_SECRET)

class MovingAverageCD:
    def __init__(self, 
                 symbol,
                 limit = 50,
                 fastScale = 4,
                 slowScale = 8,
                 signalPeriod = 3,
                 start = "2024-02-01",
                 end = "2024-02-02") -> None:

        self.symbol = symbol
        self.limit = limit
        self.fastScale = fastScale
        self.signalPeriod = signalPeriod
        self.slowScale = slowScale
        self.start = start
        self.end = end

    def generate_chart(self):
        barsReq = StockBarsRequest(
            symbol_or_symbols=self.symbol,
            timeframe=TimeFrame(1, TimeFrame.Minute),
            start =datetime.datetime.strptime(self.start, '%Y-%m-%d'),
            end=datetime.datetime.strptime(self.end, '%Y-%m-%d'),
            limit=self.limit
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

        fastScale = self.fastScale
        slowScale = self.slowScale
        signalPeriod = self.signalPeriod

        macd, macdsignal, macdhist = talib.MACD(arrM, fastperiod=fastScale, slowperiod=slowScale, signalperiod=signalPeriod)

        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=("", ""),
            row_heights=[0.3, 0.3, 0.4]
        )

        fig.add_trace(go.Candlestick(x=time,
                                    open=openVar,
                                    high=highVar,
                                    low=lowVar,
                                    close=closeVar,
                                    name="Stock Price"),
                    row=3, col=1)

        fig.add_trace(go.Scatter(x=time, y=macd, mode="lines", name="Moving Average Convergence/Divergence", line=dict(color="green")), row=2, col=1)
        fig.add_trace(go.Scatter(x=time, y=macdsignal, mode="lines", name="Signal line", line=dict(color="blue")), row=2, col=1)

        fig.add_trace(go.Bar(x=time, y=macdhist, name="MACD Histogram", marker=dict(color="green")), row=1, col=1)


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
        orderThresh = 0.5
        repeat = True
        buy = False

        for i in range(len(mid)):
            if macd[i] != np.nan and macd[i] >= macdsignal[i] and (cash - amt * mid[i] > 10000) and (repeat or not buy):
                stocks += amt
                cash -= amt * mid[i]
                dfBuy.loc[len(dfBuy)] = [time[i], macd[i], "green"]
                buy = True
            elif macd[i] != np.nan and macd[i] <= macdsignal[i]  and (stocks >= amt) and (repeat or buy):
                cash += amt * mid[i]
                stocks -= amt
                dfSell.loc[len(dfSell)] = [time[i], macd[i], "red"]
                buy = False

        fig.add_trace(go.Scatter(
            x=dfBuy["x"], y=dfBuy["y"],
            mode="markers", marker=dict(size=10, color=dfBuy["color"]),
            name="Buy"), row=2, col=1)

        fig.add_trace(go.Scatter(
            x=dfSell["x"], y=dfSell["y"],
            mode="markers", marker=dict(size=10, color=dfSell["color"]),
            name="Sell"), row=2, col=1)

        fig.update_layout(
            xaxis_title="Time",
            yaxis2_title="Price",
            yaxis_title="MACDEXT",
            showlegend=True,
            title="Moving Average Convergence/Divergence",
            width=1100,
            height=690
        )

        total = cash + stocks * mid[-1]
        fig.add_annotation(
            text=(f"started with {100000} got to {total} ended with {stocks} stocks and {cash} cash"),
            x=1,  # x position (0 to 1)
            y=1,  # y position (0 to 1)
            xref="paper",  # Position relative to the whole figure (not data points)
            yref="paper",  # Position relative to the whole figure (not data points)
            showarrow=False,  # No arrow
            font=dict(size=14, color="black"),  # Customize font size and color
            align="right"  # Right-align the text
        )

        obj = pio.to_json(fig)
        return obj