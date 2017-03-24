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

stock_map = {'600000': '浦发银行', '600015': '华夏银行', '600016': '民生银行', 
             '600036': '招商银行', '601009': '南京银行', '601166': '兴业银行',
             '601169': '北京银行', '601288': '农业银行', '601328': '交通银行',
             '601398': '工商银行', '601818': '光大银行', '601939': '建设银行',
             '601988': '中国银行', '601998': '中信银行'}

code_list = list(stock_map.keys());
name_list = list(stock_map.values());

n = len(stock_map)
pvalue_matrix = np.ones((n, n))
pairs = []
pairs_min = []

for i in range(n):
    for j in range(i+1, n):
        stock1 = ts.get_hist_data(code_list[i], start, end)[::-1]
        stock2 = ts.get_hist_data(code_list[j], start, end)[::-1]
        
        result = sm.tsa.stattools.coint(stock1['close'], stock2['close'])
        pvalue = result[1]
        pvalue_matrix[i, j] = pvalue
       
        print(name_list[i], name_list[j], pvalue)
        
        pairs.append((name_list[i], name_list[j], pvalue))

        if pvalue < 0.05:
            pairs_min.append((name_list[i], name_list[j], pvalue))

print(pairs_min)
sns.heatmap(pvalue_matrix, xticklabels=name_list, yticklabels=name_list, cmap='RdYlGn_r', mask = (pvalue_matrix == 1))

k = 0
for i in range(n):
    for j in range(i+1, n):
        stock1 = ts.get_hist_data(code_list[i], start, end)[::-1]
        stock2 = ts.get_hist_data(code_list[j], start, end)[::-1]
        print(name_list[i], name_list[j])
                
        X = []
        x = stock1['close']
        y = stock2['close']
        X = sm.add_constant(x)
        result = (sm.OLS(y,X)).fit()
#        print(result.summary())
        
        fig, ax = plt.subplots(figsize=(8,6))
        ax.plot(x, y, 'o', label="data" + " " + str(pairs[k]))
        ax.plot(x, result.fittedvalues, 'r', label="OLS")
        ax.legend(loc='best')
        k +=1