import pandas as pd
from numpy import isnan, nan
from pandas import Series, DataFrame
from pandas_ta.volatility import atr
from pandas_ta.overlap import sma
from pandas_ta._typing import Int, DictLike
from pandas_ta.utils import v_pos_default, v_series


def nz(value, default):
    """Return default if value is NaN, otherwise return value."""
    return default if pd.isnull(value) else value


def na(value):
    """Check if a value is NaN."""
    return pd.isnull(value)


def halftrend(
    high: Series, low: Series, close: Series,
    atr_length: Int = None,
    amplitude: Int = None,
    channel_deviation: Int = None,
    **kwargs: DictLike
) -> DataFrame:

    # Validate inputs
    atr_length = v_pos_default(atr_length, 14)
    amplitude = v_pos_default(amplitude, 2)
    channel_deviation = v_pos_default(channel_deviation, 2)
    _length = max(atr_length, amplitude, channel_deviation) + 1

    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)

    if high is None or low is None or close is None:
        return None

    # Initialize variables
    trend = next_trend = 0
    up = down = atr_high = atr_low = 0.0
    direction = None
    df_length = high.size

    arr_trend = [None] * df_length
    arr_up = [None] * df_length
    arr_down = [None] * df_length

    atr_high_series = pd.Series([0.0] * df_length)
    atr_low_series = pd.Series([0.0] * df_length)
    atr_close_series = pd.Series([0.0] * df_length)
    atr_direction_series = pd.Series([None] * df_length)

    max_low_price = low.iat[atr_length - 1]
    min_high_price = high.iat[atr_length - 1]

    if close.iat[0] > low.iat[atr_length]:
        trend = next_trend = 1

    # Main calculation loop
    atr_N = atr(high, low, close, window=atr_length)
    high_ma = sma(high, amplitude)
    low_ma = sma(low, amplitude)
    highest_bars = high.rolling(amplitude, min_periods=1).max()
    lowest_bars = low.rolling(amplitude, min_periods=1).min()

    for i in range(1, df_length):
        atr2 = atr_N.iat[i] / 2.0
        dev = channel_deviation * atr2

        high_price = highest_bars.iat[i]
        low_price = lowest_bars.iat[i]

        if next_trend == 1:
            max_low_price = max(low_price, max_low_price)
            if high_ma.iat[i] < max_low_price and close.iat[i] < nz(low.iat[i - 1], low.iat[i]):
                trend = next_trend = 0
                min_high_price = high_price
        else:
            min_high_price = min(high_price, min_high_price)
            if low_ma.iat[i] > min_high_price and close.iat[i] > nz(high.iat[i - 1], high.iat[i]):
                trend = next_trend = 1
                max_low_price = low_price

        arr_trend[i] = trend

        if trend == 0:
            up = max(max_low_price, nz(arr_up[i - 1], max_low_price))
            direction = "long"
            atr_high, atr_low = up + dev, up - dev
            arr_up[i] = up
        else:
            down = min(min_high_price, nz(arr_down[i - 1], min_high_price))
            direction = "short"
            atr_high, atr_low = down + dev, down - dev
            arr_down[i] = down

        atr_high_series.iat[i] = atr_high
        atr_low_series.iat[i] = atr_low
        atr_close_series.iat[i] = up if trend == 0 else down
        atr_direction_series.iat[i] = direction

    # Output DataFrame
    _props = f"_{atr_length}_{amplitude}_{channel_deviation}"
    _name = "HALFTREND"

    data = {
        f"{_name}_atr_high{_props}": atr_high_series,
        f"{_name}_close{_props}": atr_close_series,
        f"{_name}_atr_low{_props}": atr_low_series,
        f"{_name}_direction{_props}": atr_direction_series,
        f"{_name}_arr_up{_props}": arr_up,
        f"{_name}_arr_down{_props}": arr_down
    }

    df = DataFrame(data, index=close.index)
    df.name = f"{_name}{_props}"
    df.category = "volatility"

    return df
