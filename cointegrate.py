# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 15:44:28 2017

@author: Admin
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import tushare as ts
import matplotlib.pyplot as plt
from datetime import date

from pandas import DataFrame,Series

def find_cointegrated_pairs(dataframe):
    n = dataframe.shape[1]
    pvalue_matrix = np.ones((n, n))
    keys = dataframe.keys()
    pairs = []
    
    for i in range(n):
        for j in range(i+1, n):
            stock1 = dataframe[keys[i]]
            stock2 = dataframe[keys[j]]
            
            result = sm.tsa.stattools.coint(stock1, stock2)
            pvalue = result[1]
            pvalue_matrix[i, j] = pvalue
            
            if pvalue < 0.05:
                pairs.append((keys[i], keys[j], pvalue))
                
    return pvalue_matrix, pairs
    
start = "2016-1-1"
end = date.today().strftime("%Y-%m-%d")
code_list = ["601818", "601328"]

df1 = pd.DataFrame()
prices_df = pd.DataFrame()

for code in code_list:
    hist_data = ts.get_hist_data(code, start, end)[::-1]
    df1 = pd.DataFrame(data=hist_data["close"], index=hist_data.index, columns=[code])
    prices_df = pd.concat([prices_df, df1], axis = 1)

print(hist_data)
print(df1)
print(prices_df)
#pvalues, pairs = find_cointegrated_pairs(prices_df)
#print(pairs)
#sns.heatmap(1-pvalues, xticklabels=stock_list, yticklabels=stock_list, cmap='RdYlGn_r', mask = (pvalues == 1))
