# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 15:44:28 2017

@author: Admin
"""
import numpy as np
import pandas as pd

from statsmodels.tsa.stattools import coint

import matplotlib.pyplot as plt
from datetime import date

import tushare as ts

def zscore(series):
    return (series - series.mean()) / np.std(series)

start = "2016-1-1"
end = date.today().strftime("%Y-%m-%d")

stock1 = ts.get_hist_data('601169', start, end)[::-1]
stock2 = ts.get_hist_data('601998', start, end)[::-1]

stock1[['close']].plot()
stock2[['close']].plot()

score, pvalue, _ = coint(stock1[['close']], stock2[['close']])
print("score =", score, "pvalue =", pvalue)

diff_series= stock2[['close']] - stock1[['close']]
diff_series.plot()

zscore(diff_series).plot()
plt.axhline(0, color='black', linestyle='-')
plt.axhline(1.0, color='red', linestyle='--')
plt.axhline(-1.0, color='green', linestyle='--')


industry_classified = ts.get_industry_classified()
industry_list = []
industry_dict = {}
industry = ""

for row in industry_classified.itertuples():
    if len(industry_list) == 0:
        print("\n")
        industry = row.c_name
        industry_list.append(row.c_name)

    if row.c_name in industry_list:
        industry = row.c_name
    else:
        print(industry, ":")
        print(industry_dict)

        industry_list.append(row.c_name)
        industry_dict = {}

    industry_dict[row.code] = row.name

print(industry_list)


start = "2016-1-1"
end = date.today().strftime("%Y-%m-%d")

stock_map = {'600000': '浦发银行', '600015': '华夏银行', '600016': '民生银行', 
             '600036': '招商银行', '601009': '南京银行', '601166': '兴业银行',
             '601169': '北京银行', '601288': '农业银行', '601328': '交通银行',
             '601398': '工商银行', '601818': '光大银行', '601939': '建设银行',
             '601988': '中国银行', '601998': '中信银行'}

code_list = list(stock_map.keys());
name_list = list(stock_map.values());

for i in range(len(stock_map)):
    stock = ts.get_hist_data(code_list[i], start, end)
    print(name_list[i], len(stock))

