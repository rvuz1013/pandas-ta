# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from pandas import Series
from pandas_ta._typing import DictLike, Int, Float
from pandas_ta.utils import v_series, v_offset
from pandas_ta.overlap.sma import sma
from pandas_ta.volume.vwma import vwma


def avsl(
    high: Series,
    low: Series,
    close: Series,
    volume: Series,
    vpc_length: Int = 50,
    vpr_length: Int = 10,
    vm_short: Int = 10,
    vm_long: Int = 50,
    scalar: Float = 2.0,
    offset: Int = 0,
    **kwargs: DictLike
) -> Series:
    """
    Anti‑Volume Stop Loss (AVSL)

    Combines support, volatility, and the inverse relationship
    between price and volume to create a trailing stop‑loss line.

    Based on Buff Dormeier’s “Investing w/ Volume Analysis” (page 254).

    1. VPC  = VWMA(close, vol, vpc_length) - SMA(close, vpc_length)
    2. VPR  = VWMA(close, vol, vpr_length) / SMA(close, vpr_length)
    3. VM   = SMA(volume, vm_short) / SMA(volume, vm_long)
    4. VPCI = VPC * VPR * VM
    5. dyn_len = round(3 + VPCI) as nullable Int64 series
    6. factor  = low * (1/VPC) * (1/VPR)
    7. AVSL[i] = lower Bollinger Band of factor over dyn_len[i]
               = mean(factor[i-dyn_len+1:i]) - (scalar * VPCI[i]*VM[i]) * std(...)

    Args:
      high, low, close, volume (pd.Series): your price & volume data
      vpc_length (int): period for Volume‑Price Correlation (default 50)
      vpr_length (int): period for Volume‑Price Ratio (default 10)
      vm_short (int):   short window for Volume Multiplier (default 10)
      vm_long (int):    long  window for Volume Multiplier (default 50)
      scalar (float):   multiplier on the band (default 2.0)
      offset (int):     shift the result (default 0)
      **kwargs:         fillna=value

    Returns:
      pd.Series: AVSL line
    """
    # — validate inputs —
    high_  = v_series(high)
    low_   = v_series(low)
    close_ = v_series(close)
    vol_   = v_series(volume)
    if high_ is None or low_ is None or close_ is None or vol_ is None:
        return

    offset = v_offset(offset)

    # 1) Volume‑Price Correlation
    sma_close    = sma(close_, length=vpc_length)
    vwma_close   = vwma(close_, volume=vol_, length=vpc_length)
    vpc          = vwma_close - sma_close

    # 2) Volume‑Price Ratio
    sma_c_short  = sma(close_, length=vpr_length)
    vwma_c_short = vwma(close_, volume=vol_, length=vpr_length)
    vpr          = vwma_c_short / sma_c_short.replace(0, np.nan)

    # 3) Volume Multiplier
    sma_v_short  = sma(vol_, length=vm_short)
    sma_v_long   = sma(vol_, length=vm_long)
    vm           = sma_v_short / sma_v_long.replace(0, np.nan)

    # 4) VPCI
    vpci = vpc * vpr * vm

    # 5) dynamic window length as nullable Int64
    raw_len = (vpci + 3).round()
    raw_len = raw_len.replace([np.inf, -np.inf], np.nan)
    dyn_len = raw_len.astype("Int64")

    # 6) the factor series we’ll BB on
    factor = low_ * (1 / vpc.replace(0, np.nan)) * (1 / vpr.replace(0, np.nan))

    # 7) build AVSL with dynamic windows
    result = Series(index=factor.index, dtype="float64")
    for i in range(len(result)):
        L = dyn_len.iat[i]
        if pd.isna(L) or L <= 0:
            result.iat[i] = np.nan
        else:
            start = max(0, i - int(L) + 1)
            win   = factor.iloc[start : i + 1]
            mean_ = win.mean()
            std_  = win.std()
            band  = scalar * (vpci.iat[i] * vm.iat[i])
            result.iat[i] = mean_ - band * std_

    # apply offset & fill
    if offset != 0:
        result = result.shift(offset)
    if "fillna" in kwargs:
        result.fillna(kwargs["fillna"], inplace=True)

    result.name     = f"AVSL_{vpc_length}_{vpr_length}_{vm_short}_{vm_long}"
    result.category = "volatility"
    return result
