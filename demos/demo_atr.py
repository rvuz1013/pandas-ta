import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("../data/SPY_D.csv")
df.sort_values(by=['date'], inplace=True)
df["date"] = pd.to_datetime(df["date"])

df["ATR"] = ta.atr(high=df.high, low=df.low, close=df.close, talib=False)

df["ATRP"] = ta.atr(high=df.high, low=df.low, close=df.close, percent=True, talib=False)

df["NATR"] = ta.natr(high=df.high, low=df.low, close=df.close, talib=False)

print(df)