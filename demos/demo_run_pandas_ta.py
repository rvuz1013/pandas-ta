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

df = pd.read_csv("../data/sample.csv")
df.sort_values(by=['date'], inplace=True)

df["date"] = pd.to_datetime(df["date"])

df["sma"] = ta.sma(close = df.close, length = 3)

# x = yf.Ticker('ABB.NS', start = "2021-12-08", end = "2023-01-01", progress = False)
# ta.stc(x['Close']).iloc[:, 0].mean()

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