from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
import datetime
from dotenv import load_dotenv
import os
import numpy as np
import talib
import plotly.graph_objects as go
import plotly.io as pio
import pandas

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

client = StockHistoricalDataClient(API_KEY,  API_SECRET)

class ParabolicSAR:
    def __init__(self, 
                 symbol, 
                 limit = 50,
                 accl = 0.2,
                 max = 0.6) -> None:

        self.symbol = symbol
        self.limit = limit
        self.accl = accl
        self.max = max
        
    def generate_chart(self):
        barsReq = StockBarsRequest(
            symbol_or_symbols=self.symbol,
            timeframe=TimeFrame(1, TimeFrame.Minute),
            start=datetime.datetime(2024, 2, 1, 10),
            end=datetime.datetime(2024, 2, 2, 20),
            limit=self.limit
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
                    time.append(data_point.timestamp)


        fig = go.Figure(data=[go.Candlestick(x=time,
                        open=openVar,
                        high=highVar,
                        low=lowVar,
                        close=closeVar)])

        arrH = np.array(highVar)
        arrL = np.array(lowVar)

        accl = self.accl
        max = self.max

        sar = talib.SAR(arrH, arrL, acceleration=accl, maximum=max)

        fig.add_trace(go.Scatter(x=time, y=arrH, mode="lines", name="High", line=dict(color="green")))
        fig.add_trace(go.Scatter(x=time, y=mid, mode="lines", name="Price", line=dict(color="blue")))
        fig.add_trace(go.Scatter(x=time, y=arrL, mode="lines", name="Low", line=dict(color="red")))

        fig.add_trace(go.Scatter(x=time, y=arrL, mode="lines", name="Parabolic SAR", line=dict(color="black", dash="dash")))

        fig.update_layout(
            title="Parabolic SAR (Stop and Reverse) Visualization",
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

        for i in range(len(sar)):
            if(sar[i] != np.nan and mid[i] >= sar[i] and (cash - amt * mid[i] > 10000) and (repeat or not buy)):
                stocks += amt
                cash -= amt * mid[i]
                dfBuy.loc[len(dfBuy)] = [time[i], mid[i], "green"]
                buy = True
            elif(sar[i] != np.nan and mid[i] <= sar[i] and (stocks >= amt) and (repeat or buy)):
                cash += amt * mid[i]
                stocks -= amt
                dfSell.loc[len(dfSell)] = [time[i], mid[i], "red"]
                buy = False

        fig.add_scatter(
            x=dfBuy["x"],
            y=dfBuy["y"],
            mode="markers",
            marker=dict(size=10, color=dfBuy["color"]),
            name="Buy"
        )

        fig.add_scatter(
            x=dfSell["x"],
            y=dfSell["y"],
            mode="markers",
            marker=dict(size=10, color=dfSell["color"]),
            name="Sell"
        )

        obj = pio.to_json(fig)
        return obj