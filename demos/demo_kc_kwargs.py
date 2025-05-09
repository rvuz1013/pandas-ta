import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("../data/sample.csv")
df.sort_values(by=['date'], inplace=True)
df["date"] = pd.to_datetime(df["date"])

mamode = "linreg"
# kwargs = {'angles': True, 'degrees': True, 'intercept': True, 'slope': True, 'r': True, 'tsf': True, 'talib': False}
kwargs = {'r': True}

# if mamode == "linreg":
#     kwargs = {'degrees': True, 'slope': True, 'tsf': True}
# print(kwargs)

print(ta.kc(high=df.high, low=df.low, close=df.close, mamode=mamode, **kwargs))

print(ta.kc(high=df.high, low=df.low, close=df.close, mamode=mamode))

# print(ta.linreg(close=df.close, length=20))

# print(ta.linreg(close=df.close, r=True))
