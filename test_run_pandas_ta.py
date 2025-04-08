import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf

# Example: Test a moving average function
dataframe = pd.DataFrame({
    "close": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
})

# Apply an indicator, for example, Simple Moving Average (SMA)
dataframe['SMA'] = ta.sma(dataframe['close'], length=3)

print(dataframe)

df = pd.read_csv("data/sample.csv")
df.sort_values(by=['date'], inplace=True)

df["date"] = pd.to_datetime(df["date"])

df["sma"] = ta.sma(close = df.close, length = 3)

# Testing new RMI indicator function
df["rmi"] = ta.rmi(close = df.close, momentum = 5)

# df["natr"] = ta.natr(high = df.high, low = df.low, close = df.close, length = 10)

# df["atr"] = ta.atr(high = df.high, low = df.low, close = df.close, percent = True)

# x = yf.Ticker('ABB.NS', start = "2021-12-08", end = "2023-01-01", progress = False)
# ta.stc(x['Close']).iloc[:, 0].mean()

print(df)

# Graph the dataframe as a candlestick price chart
figure = go.Figure(data = [go.Candlestick(x = df.date,
                                         open = df.open,
                                         high = df.high,
                                         low = df.low,
                                         close = df.close
                                         )])

# Add SMA indicator overlay to chart
figure.add_trace(go.Scatter(x = df.date,
                            y = df.sma,
                            mode='lines',
                            line=dict(color='black'),
                            name='SMA'
                            ))

# figure.show()

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