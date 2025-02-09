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

class HAM:
    def __init__(self, 
                 symbol,
                 limit = 50,
                 timeFrame1 = 5) -> None:

        self.symbol = symbol
        self.limit = limit
        self.timeFrame1 = timeFrame1

    def generate_chart(self):
        barsReq = StockBarsRequest(
            symbol_or_symbols=self.symbol,
            timeframe=TimeFrame(1, TimeFrame.Minute),
            start=datetime.datetime(2024, 6, 26),
            end=datetime.datetime(2024, 7, 3),
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
                        close=closeVar,
                        name="Stock Price")])

        arrH = np.array(highVar)
        arrL = np.array(lowVar)
        arrC = np.array(closeVar)
        arrO = np.array(openVar)

        ham = talib.CDLHAMMER(arrO, arrH, arrL, arrC)
        sma = talib.SMA(arrC, self.timeFrame1)

        points = []

        for i in range(len(ham)):
            if(ham[i] == 100):
                points.append(i)

        fig.add_trace(go.Scatter(x=time, y=mid, mode="lines", name="Price", line=dict(color="blue")))
        fig.add_trace(go.Scatter(x=time, y=sma, mode="lines", name="Simple Moving Avg", line=dict(color="green")))

        for i in points:
            fig.add_shape(
                type="circle",
                xref="x", yref="y",
                x0=time[i-1], x1=time[i+1],
                y0= (arrL[i] - 1), y1= (arrH[i]) + 1,
                line=dict(color="red", width=3)
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
            if(i in points and (cash - amt * mid[i] > 10000) and (repeat or not buy)):
                stocks += amt
                cash -= amt * mid[i]
                dfBuy.loc[len(dfBuy)] = [time[i], mid[i], "green"]
                print(f"We bought {amt} stocks for {mid[i]} on {i} because the {ham[i]} value")
                buy = True
            elif(i not in points and sma[i] > mid[i] and (stocks >= amt) and (repeat or buy)):
                cash += amt * mid[i]
                stocks -= amt
                dfSell.loc[len(dfSell)] = [time[i], mid[i], "red"]
                print(f"We sold {amt} stocks for {mid[i]} on {i} because the {sma[i]} value")
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

        fig.update_layout(
            title="Hammer Pattern Visualization",
            xaxis_title="Time",
            yaxis_title="Price",
            legend=dict(x=0, y=1),
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