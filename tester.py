import plotly.express as px
import pandas as pd

# Sample DataFrame with custom colors for each point
df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 20, 15, 25, 18],
    "color": ["blue", "green", "blue", "red", "blue"]  # Custom colors per point
})

# Create the line plot
fig = px.line(df, x="x", y="y", title="Line Chart with Custom Colored Dots")

# Overlay scatter plot for custom-colored dots
fig.add_scatter(
    x=df["x"],
    y=df["y"],
    mode="markers",
    marker=dict(size=10, color=df["color"]),  # Use the custom colors
    name="Custom Dots"
)

# Show figure
fig.show()
