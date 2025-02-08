import numpy as np
import talib

close = np.random.random(100)
output = talib.SMA(close, 10)

print(output)

from talib import MA_Type

upper, middle, lower = talib.BBANDS(close, matype=MA_Type.T3)

output = talib.MOM(close, timeperiod=5)
print(output)