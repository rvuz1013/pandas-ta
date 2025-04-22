import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("../data/sample.csv")
df.sort_values(by=['date'], inplace=True)
df["date"] = pd.to_datetime(df["date"])

df["TRAMA"] = ta.trama(close = df.close, length = 10)

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
                            y = df.TRAMA,
                            mode='lines',
                            line=dict(color='black'),
                            name='TRAMA'
                            ))

figure.show()