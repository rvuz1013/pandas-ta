import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

# Show all columns
pd.set_option("display.max_columns", None)

# Show all rows
pd.set_option("display.max_rows", None)

# Show full content in each column (e.g., if a string is long)
pd.set_option("display.max_colwidth", None)

# Optional: prevent line wrapping in console
pd.set_option("display.expand_frame_repr", False)

htdf = ta.halftrend(high = df.high, low = df.low, close = df.close)
# df = df.join(ta.halftrend(high = df.high, low = df.low, close = df.close))

# x = yf.Ticker('ABB.NS', start = "2021-12-08", end = "2023-01-01", progress = False)
# ta.stc(x['Close']).iloc[:, 0].mean()

print(htdf)

# Bellow is all the messy plotly graphing functions

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

# fig = make_subplots(
#     rows=2, cols=1,
#     shared_xaxes=True,
#     vertical_spacing=0.03,
#     row_heights=[0.7, 0.3],
#     subplot_titles=("Candlestick Chart", "RMI")
# )
#
# # Candlestick chart
# fig.add_trace(go.Candlestick(
#     x=df.index,
#     open=df["open"],
#     high=df["high"],
#     low=df["low"],
#     close=df["close"],
#     name="Price"
# ), row=1, col=1)
#
# # RSI plot
# fig.add_trace(go.Scatter(
#     x=df.index,
#     y=df["rmi"],
#     line=dict(color="purple", width=1),
#     name="RMI"
# ), row=2, col=1)
#
# # Add overbought/oversold lines
# fig.add_hline(y=70, line=dict(color="red", dash="dash"), row=2, col=1)
# fig.add_hline(y=30, line=dict(color="green", dash="dash"), row=2, col=1)
#
# # Update layout
# fig.update_layout(
#     height=800,
#     showlegend=False,
#     xaxis_rangeslider_visible=False,
#     title="Candlestick with RMI"
# )

fig = go.Figure()

# Add candlestick chart
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name='Candles'
))

# Add HalfTrend middle line (close values)
fig.add_trace(go.Scatter(
    x=htdf.index,
    y=htdf['HALFTREND_close_14_2_2'],
    mode='lines',
    name='HalfTrend',
    line=dict(color='blue', width=2)
))

# Add atr_high (upper band)
fig.add_trace(go.Scatter(
    x=htdf.index,
    y=htdf['HALFTREND_atr_high_14_2_2'],
    mode='lines',
    name='ATR High',
    line=dict(color='green', width=1, dash='dot')
))

# Add atr_low (lower band)
fig.add_trace(go.Scatter(
    x=htdf.index,
    y=htdf['HALFTREND_atr_low_14_2_2'],
    mode='lines',
    name='ATR Low',
    line=dict(color='red', width=1, dash='dot')
))

# Customize layout
fig.update_layout(
    title='HalfTrend Indicator Overlay',
    xaxis_title='Index',
    yaxis_title='Price',
    xaxis=dict(rangeslider=dict(visible=False)),  # Hide rangeslider if not needed
    yaxis=dict(autorange=True),  # <- THIS enables y-axis autoscaling on zoom
    height=700,
)

fig.show()