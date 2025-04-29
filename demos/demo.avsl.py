# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pandas_ta as ta

df = pd.read_csv("../data/sample.csv")
df.sort_values(by=['date'], inplace=True)

df["date"] = pd.to_datetime(df["date"])

# 2) Compute AVSL
# Note: adjust lengths if your df is small, e.g. vpc_length=10, vm_long=10
df["avsl"] = ta.avsl(
    low = df["low"], close = df["close"], volume = df["volume"],
)

# 3) Print the AVSL column
print(df)
