import pandas_ta as ta
import pandas as pd

df = pd.read_csv("../data/sample.csv")
df.sort_values(by=['date'], inplace=True)
df["date"] = pd.to_datetime(df["date"])

print(ta.chandelier_exit(high = df.high, low = df.low, close = df.close, offset = 3))