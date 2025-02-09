import numpy as np
import talib
import plotly.graph_objects as go
import pandas as pd

# Generate sample OHLC data
np.random.seed(42)
time = pd.date_range(start="2024-02-01", periods=50, freq="D")
open_prices = np.random.uniform(90, 110, 50)
high_prices = open_prices + np.random.uniform(0, 5, 50)
low_prices = open_prices - np.random.uniform(0, 5, 50)
close_prices = open_prices + np.random.uniform(0, 3, 50)

# Detect Three White Soldiers pattern
pattern = talib.CDL3WHITESOLDIERS(open_prices, high_prices, low_prices, close_prices)

# Find where the pattern appears
pattern_indices = np.where(pattern == 100)[0]

# Create candlestick chart
fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=time, open=open_prices, high=high_prices, low=low_prices, close=close_prices,
    name="Candlestick"
))

# Add a red circle around the interesting section
for i in pattern_indices:
    fig.add_shape(
        type="circle",
        xref="x", yref="y",
        x0=time[i-1], x1=time[i+1],
        y0=min(low_prices[i-1:i+2]) - 1, y1=max(high_prices[i-1:i+2]) + 1,
        line=dict(color="red", width=3)
    )

# Update layout
fig.update_layout(
    title="Three White Soldiers Pattern",
    xaxis_title="Date",
    yaxis_title="Price",
    showlegend=True
)

fig.show()
