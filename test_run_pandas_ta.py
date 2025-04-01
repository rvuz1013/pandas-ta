import pandas_ta as ta
import pandas as pd

# Example: Test a moving average function
df = pd.DataFrame({
    "close": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
})

# Apply an indicator, for example, Simple Moving Average (SMA)
df['SMA'] = ta.sma(df['close'], length=3)

print(df)