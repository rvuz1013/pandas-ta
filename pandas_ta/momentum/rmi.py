# -*- coding: utf-8 -*-
from pandas import Series
from ..overlap import ema
from pandas_ta._typing import DictLike, Int
from pandas_ta.maps import Imports
from pandas_ta.utils import (
    v_offset,
    v_scalar,
    v_pos_default,
    v_series,
    v_talib,
    v_int
)

def rmi(
    close: Series, length: Int = None,
    talib: bool = None, offset: Int = None,
    momentum: Int = None, scalar: Int = None,
    **kwargs: DictLike
) -> Series:
    """

    """
    # Validate
    length = v_pos_default(length, 14)
    momentum = v_int(momentum, 5)
    close = v_series(close, length)

    if close is None:
        return

    mode_tal = v_talib(talib)
    scalar = v_scalar(scalar, 100)
    offset = v_offset(offset)

    # Calculate changes in momentum based on closing price
    momentum_change = close.diff(momentum)

    gain = momentum_change.clip(lower=0)
    loss = -momentum_change.clip(upper=0)

    # Smooth gains and losses using EMA
    avg_gain = ema(gain, length=length)
    avg_loss = ema(loss, length=length)

    # Calculate RMI using modified relative strength equation
    rs = avg_gain / avg_loss
    rmi = scalar - (scalar / (1 + rs))

    # Offset
    if offset != 0:
        rmi = rmi.shift(offset)

    # Fill
    if "fillna" in kwargs:
        rmi.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    rmi.name = f"RMI_{length}"
    rmi.category = "momentum"

    return rmi
