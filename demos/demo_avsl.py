# -*- coding: utf-8 -*-
import pandas as pd
import plotly.graph_objects as go
import pandas_ta as ta

df = pd.read_csv("../data/aapl.csv")
df.sort_values(by=['date'], inplace=True)
df["date"] = pd.to_datetime(df["date"])

# 2) Compute AVSL
# Note: adjust lengths if your df is small, e.g. vpc_length=10, vm_long=10
df["avsl"] = ta.avsl(
    low = df["low"], close = df["close"], volume = df["volume"],
)

# 3) Print the AVSL column
print(df)


# Graph the dataframe as a candlestick price chart
figure = go.Figure(data = [go.Candlestick(x = df.date,
                                         open = df.open,
                                         high = df.high,
                                         low = df.low,
                                         close = df.close
                                         )])

# Add AVSL indicator overlay to chart
figure.add_trace(go.Scatter(x = df.date,
                            y = df.avsl,
                            mode='lines',
                            line=dict(color='red'),
                            name='AVSL'
                            ))

# Customize layout
figure.update_layout(
    title='AVSL Indicator Overlay',
    xaxis_title='Index',
    yaxis_title='Price',
    xaxis=dict(rangeslider=dict(visible=False)),  # Hide rangeslider if not needed
    yaxis=dict(autorange=True),  # <- THIS enables y-axis autoscaling on zoom
    height=500,
)

figure.show()