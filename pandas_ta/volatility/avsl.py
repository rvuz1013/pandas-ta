# -*- coding: utf-8 -*-
from numpy import nan, inf, where, errstate
from pandas import Series
from pandas_ta.volume import vwma
from pandas_ta._typing import DictLike, Int, Float
from pandas_ta.utils import v_series, v_offset, v_scalar, v_int


def avsl(
    close: Series, low: Series, volume: Series,
    fast_period: Int = 12, slow_period: Int = 26, signal_period: Int = 9,
    scalar: Float = 2.0, offset: Int = None, **kwargs: DictLike
) -> Series:
    """
    """
    # Validate
    close = v_series(close)
    low = v_series(low)
    volume = v_series(volume)
    fast_period = v_int(fast_period, 12)
    slow_period = v_int(slow_period, 26)

    if close is None:
        return

    scalar = v_scalar(scalar, 2.0)
    offset = v_offset(offset)

    # Volume-Weighted and Simple Moving Averages
    vwma_fast = vwma(close, volume, length=fast_period)
    vwma_slow = vwma(close, volume, length=slow_period)

    sma_fast = close.rolling(fast_period).mean()
    sma_slow = close.rolling(slow_period).mean()

    # Guard clause for early-return if moving averages are not ready
    if vwma_fast is None or vwma_slow is None or sma_fast is None or sma_slow is None:
        return Series(index=close.index, dtype="float64", name=f"AVSL_{fast_period}_{slow_period}_{signal_period}")

    # Volume Price Confirmation Indicator (VPCI) components
    vpc = vwma_slow - sma_slow  # Volume Price Confirmation
    vpr = vwma_fast / sma_fast  # Volume Price Ratio
    vm = volume.rolling(fast_period).mean() / volume.rolling(slow_period).mean()  # Volume Multiplier
    vpci = vpc * vpr * vm

    # Deviation based on VPCI
    deviation = scalar * vpci * vm

    # Adjust VPC to avoid division issues
    vpc_adjusted = vpc.copy()
    vpc_adjusted = where((vpc > -1) & (vpc < 0), -1, vpc_adjusted)
    vpc_adjusted = where((vpc >= 0) & (vpc < 1), 1, vpc_adjusted)

    # Price function approximation
    with errstate(divide='ignore', invalid='ignore'):
        adjusted_price = low / (vpc_adjusted * vpr)
    adjusted_price = Series(adjusted_price, index=low.index).replace([inf, -inf], nan)

    # Smoothed adjusted price
    price_function = adjusted_price.rolling(slow_period).mean() / 100

    # Final AVSL calculation
    raw_avsl = low - price_function + deviation
    avsl = raw_avsl.rolling(slow_period).mean()

    # apply offset & fill
    if offset != 0:
        avsl = avsl.shift(offset)
    if "fillna" in kwargs:
        avsl.fillna(kwargs["fillna"], inplace=True)

    avsl.name     = f"AVSL_{fast_period}_{slow_period}_{signal_period}"
    avsl.category = "volatility"
    return avsl
