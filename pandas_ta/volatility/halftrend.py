import pandas as pd
import numpy as np
from numba import njit
from pandas import Series, DataFrame
from pandas_ta.volatility import atr
from pandas_ta.overlap import sma
from pandas_ta._typing import Int, DictLike
from pandas_ta.utils import v_pos_default, v_series


@njit
def halftrend_loop(
    high: np.ndarray, low: np.ndarray, close: np.ndarray,
    atr_arr: np.ndarray, high_ma: np.ndarray, low_ma: np.ndarray,
    highest_bars: np.ndarray, lowest_bars: np.ndarray,
    atr_length: int, amplitude: int, channel_deviation: int
):
    length = len(close)
    trend = 0
    alpha = 0.3  # Smoothing factor

    # Initialize up/down to a real price value to avoid long ramp-up
    up = low[atr_length]
    down = high[atr_length]
    atr_high = up
    atr_low = down

    max_low_price = low[atr_length]
    min_high_price = high[atr_length]

    if close[atr_length] > low[atr_length]:
        trend = 1

    atr_cap = np.nanmax(atr_arr[:atr_length * 2]) * 0.5

    arr_trend = np.zeros(length, dtype=np.int32)
    arr_up = np.full(length, np.nan)
    arr_down = np.full(length, np.nan)
    atr_high_series = np.full(length, np.nan)
    atr_low_series = np.full(length, np.nan)
    atr_close_series = np.full(length, np.nan)
    atr_direction_series = np.zeros(length, dtype=np.int32)

    for i in range(atr_length + 1, length):
        atr_raw = atr_arr[i]
        atr2 = atr_raw / 2.0
        atr2 = min(atr2, atr_cap)  # Clamp ATR
        dev = channel_deviation * atr2

        high_price = highest_bars[i]
        low_price = lowest_bars[i]

        # More tolerant trend switching
        if trend == 0:
            max_low_price = max(max_low_price, low_price)
            if high_ma[i] < (max_low_price - dev) and close[i] < close[i - 1]:
                trend = 1
                min_high_price = high_price
        elif trend == 1:
            min_high_price = min(min_high_price, high_price)
            if low_ma[i] > (min_high_price + dev) and close[i] > close[i - 1]:
                trend = 0
                max_low_price = low_price

        arr_trend[i] = trend

        if trend == 0:
            # Smooth 'up' with a warm start
            if np.isnan(up):
                up = max_low_price
            else:
                up = alpha * max_low_price + (1 - alpha) * up

            atr_high = up + dev
            atr_low = up - dev

            arr_up[i] = up
            atr_close_series[i] = up
            atr_direction_series[i] = 0  # long

        else:
            if np.isnan(down):
                down = min_high_price
            else:
                down = alpha * min_high_price + (1 - alpha) * down

            atr_high = down + dev
            atr_low = down - dev

            arr_down[i] = down
            atr_close_series[i] = down
            atr_direction_series[i] = 1  # short

        atr_high_series[i] = atr_high
        atr_low_series[i] = atr_low

    return (
        atr_high_series,
        atr_low_series,
        atr_close_series,
        atr_direction_series,
        arr_up,
        arr_down
    )

def halftrend(high: Series, low: Series, close: Series, atr_length: Int=14, amplitude: Int=2, channel_deviation: Int=2):
    high = high.to_numpy()
    low = low.to_numpy()
    close = close.to_numpy()

    atr_arr = atr(pd.Series(high), pd.Series(low), pd.Series(close), window=atr_length).to_numpy()
    high_ma = sma(pd.Series(high), amplitude).to_numpy()
    low_ma = sma(pd.Series(low), amplitude).to_numpy()
    highest_bars = pd.Series(high).rolling(amplitude, min_periods=1).max().to_numpy()
    lowest_bars = pd.Series(low).rolling(amplitude, min_periods=1).min().to_numpy()

    results = halftrend_loop(
        high, low, close, atr_arr, high_ma, low_ma,
        highest_bars, lowest_bars,
        atr_length, amplitude, channel_deviation
    )

    (
        atr_high_series, atr_low_series, atr_close_series,
        atr_direction_series, arr_up, arr_down
    ) = results

    df = DataFrame({
        f"HT_atr_high_{atr_length}_{amplitude}_{channel_deviation}": atr_high_series,
        f"HT_atr_low_{atr_length}_{amplitude}_{channel_deviation}": atr_low_series,
        f"HT_close_{atr_length}_{amplitude}_{channel_deviation}": atr_close_series,
        f"HT_direction_{atr_length}_{amplitude}_{channel_deviation}": np.where(atr_direction_series == 0, "long", "short"),
        f"HT_arr_up_{atr_length}_{amplitude}_{channel_deviation}": arr_up,
        f"HT_arr_down_{atr_length}_{amplitude}_{channel_deviation}": arr_down
    })

    _props = f"_{atr_length}_{amplitude}_{channel_deviation}"
    df.name = f"HT{_props}"

    return df
