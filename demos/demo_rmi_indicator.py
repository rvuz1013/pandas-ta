import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("../data/sample.csv")
df.sort_values(by=['date'], inplace=True)

df["date"] = pd.to_datetime(df["date"])

# Testing new RMI indicator function
df["rmi"] = ta.rmi(close = df.close, momentum = 5)

print(df)

fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    row_heights=[0.7, 0.3],
    subplot_titles=("Candlestick Chart", "RMI")
)

# Candlestick chart
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df["open"],
    high=df["high"],
    low=df["low"],
    close=df["close"],
    name="Price"
), row=1, col=1)

# RSI plot
fig.add_trace(go.Scatter(
    x=df.index,
    y=df["rmi"],
    line=dict(color="purple", width=1),
    name="RMI"
), row=2, col=1)

# Add overbought/oversold lines
fig.add_hline(y=70, line=dict(color="red", dash="dash"), row=2, col=1)
fig.add_hline(y=30, line=dict(color="green", dash="dash"), row=2, col=1)

# Update layout
fig.update_layout(
    height=800,
    showlegend=False,
    xaxis_rangeslider_visible=False,
    title="Candlestick with RMI"
)

fig.show()