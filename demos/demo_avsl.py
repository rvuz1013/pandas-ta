# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pandas_ta as ta

# 1) Generate sample data (20 rows)
np.random.seed(42)
dates = pd.date_range("2021-01-01", periods=20, freq="D")
close = np.cumsum(np.random.randn(len(dates))) + 100
high = close + np.random.rand(len(dates)) * 2
low = close - np.random.rand(len(dates)) * 2
volume = np.random.randint(100, 1000, size=len(dates))

df = pd.DataFrame({
    "High": high,
    "Low": low,
    "Close": close,
    "Volume": volume
}, index=dates)

# 2) Compute AVSL
# Note: adjust lengths if your df is small, e.g. vpc_length=10, vm_long=10
df["avsl"] = ta.avsl(
    df["High"], df["Low"], df["Close"], df["Volume"],
    vpc_length=10, vpr_length=5,
    vm_short=5, vm_long=10,
    scalar=2.0
)

# 3) Print the AVSL column
print(df["avsl"])
