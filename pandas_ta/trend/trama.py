# -*- coding: utf-8 -*-
from pandas import Series
import numpy as np
from pandas_ta._typing import DictLike, Int
from pandas_ta.ma import ma
from pandas_ta.utils import (
    v_mamode,
    v_pos_default,
    v_series
)



def trama(
        close: Series, length: Int = None,
        mamode: str = None,
        **kwargs: DictLike
) -> Series:

    # Validate
    length = v_pos_default(length, 10)
    close = v_series(close, length)

    if close is None:
        return

    mamode = v_mamode(mamode, "sma")

    highest = close.rolling(length).max()
    lowest = close.rolling(length).min()

    hh = np.maximum(np.sign(highest.diff()), 0)
    ll = np.maximum(np.sign(-lowest.diff()), 0)

    # trend_signal = np.where((hh | ll) > 0, 1, 0)
    trend_series = Series(np.where((hh.astype(bool) | ll.astype(bool)), 1, 0), index=close.index)
    tc = ma(mamode, trend_series, length = length, **kwargs) ** 2

    ama = Series(index = close.index, dtype = float)
    ama.iloc[0] = close.iloc[0]

    ama = [close.iloc[0]]  # seed with the first close
    for i in range(1, len(close)):
        prev_ama = ama[-1]
        curr_tc = tc.iloc[i] if not np.isnan(tc.iloc[i]) else 0
        curr_src = close.iloc[i]
        ama.append(prev_ama + curr_tc * (curr_src - prev_ama))

    ama_series = Series(ama, index=close.index)

    ama_series.name = f"TRAMA_{length}"
    ama_series.category = "trend"

    return ama_series