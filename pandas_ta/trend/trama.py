# -*- coding: utf-8 -*-
from pandas import Series
import numpy as np
from pandas_ta._typing import DictLike, Int
from pandas_ta.ma import ma
from pandas_ta.overlap import sma
from pandas_ta.utils import (
    non_zero_range,
    v_drift,
    v_mamode,
    v_offset,
    v_pos_default,
    v_series
)



def trama(
        close: Series, length: Int = None,
        mamode: str = None,
        offset: Int = None, **kwargs: DictLike
) -> Series:

    # Validate
    length = v_pos_default(length, 99)
    close = v_series(close, length)

    if close is None:
        return

    highest = close.rolling(length).max()
    lowest = close.rolling(length).min()

    hh = np.maximum(np.sign(highest.diff()), 0)
    ll = np.maximum(np.sign(-lowest.diff()), 0)

    print("//////////HERE//////////")
    print(hh)
    print("//////////HERE//////////")
    print(ll)

    # trend_signal = np.where((hh | ll) > 0, 1, 0)
    trend_series = Series(np.where((hh.astype(bool) | ll.astype(bool)), 1, 0), index=close.index)
    tc = sma(trend_series, length = length) ** 2

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

    print(ama_series)

    return ama_series