# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 22:51:21 2017

@author: Admin
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import tushare as ts

from datetime import date
from statsmodels.tsa.stattools import coint

def zscore(series):
    return (series - series.mean()) / np.std(series)


sns.set_style('whitegrid',{'font.sans-serif':['simhei','Arial']})

start = "2016-1-1"
end = date.today().strftime("%Y-%m-%d")

stock1 = ts.get_hist_data('601009', start, end)[::-1]
stock2 = ts.get_hist_data('601818', start, end)[::-1]

stock1[['close']].plot()
stock2[['close']].plot()

x = stock1['close']
y = stock2['close']
X = sm.add_constant(x)
result = (sm.OLS(y,X)).fit()
print(result.summary())

fig, ax = plt.subplots(figsize=(8,6))
ax.plot(x, y, 'o', label="data")
ax.plot(x, result.fittedvalues, 'r', label="OLS")
ax.legend(loc='best')

#(0.2018*stock1["close"]-stock2["close"]).plot()
#plt.axhline((0.2018*stock1["close"]-stock2["close"]).mean(), color="red", linestyle="--")
#plt.xlabel("Time"); plt.ylabel("Stationary Series")
#plt.legend(["Stationary Series", "Mean"])
#
#zscore(0.2018*stock1["close"]-stock2["close"]).plot
#plt.axhline(zscore(0.2018*stock1["close"]-stock2["close"]).mean(), color="black")
#plt.axhline(1.0, color="red", linestyle="--")
#plt.axhline(-1.0, color="green", linestyle="--")
#plt.legend(["z-score", "mean", "+1", "-1"])