# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 15:44:28 2017

@author: Admin
"""
import numpy as np
import pandas as pd

import statsmodels
from statsmodels.tsa.stattools import coint


import matplotlib.pyplot as plt
from nsepy.archives import get_price_history
from datetime import date

import tushare as ts

def zscore(series):
    return (series - series.mean()) / np.std(series)


S1 = get_price_history(stock = 'SBIN', 
                        start = date(2015,1,1), 
                        end = date(2015,10,10))

S2 = get_price_history(stock = 'ICICIBANK', 
                        start = date(2015,1,1), 
                        end = date(2015,10,10))

result = coint(S1[['Close']], S2[['Close']])
score = result[0]
pvalue = result[1]
print("score =", score, "pvalue =", pvalue)

S1[['Close']].plot()
S2[['Close']].plot()

score, pvalue, _ = coint(S1[['Close']], S2[['Close']])
print("score =", score, "pvalue =", pvalue)

diff_series= S2[['Close']] - S1[['Close']]
diff_series.plot()

zscore(diff_series).plot()
plt.axhline(0, color='black')
plt.axhline(1.0, color='red', linestyle='--')
plt.axhline(-1.0, color='green', linestyle='--')
