import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("../data/sample.csv")
df.sort_values(by=['date'], inplace=True)
df["date"] = pd.to_datetime(df["date"])

# Show all columns and data when printed to console
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.expand_frame_repr", False)

htdf = ta.halftrend(high = df.high, low = df.low, close = df.close)

print(htdf)

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
    y=htdf['HT_close_14_2_2'],
    mode='lines',
    name='HalfTrend',
    line=dict(color='blue', width=2)
))

# Add atr_high (upper band)
fig.add_trace(go.Scatter(
    x=htdf.index,
    y=htdf['HT_atr_high_14_2_2'],
    mode='lines',
    name='ATR High',
    line=dict(color='green', width=1, dash='dot')
))

# Add atr_low (lower band)
fig.add_trace(go.Scatter(
    x=htdf.index,
    y=htdf['HT_atr_low_14_2_2'],
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