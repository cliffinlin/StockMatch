# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 22:51:21 2017

@author: Admin
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import operator
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
price_type = "open"

stock_dict = {'600000': '浦发银行', '600015': '华夏银行', '600016': '民生银行', 
             '600036': '招商银行', '601009': '南京银行', '601166': '兴业银行',
             '601169': '北京银行', '601288': '农业银行', '601328': '交通银行',
             '601398': '工商银行', '601818': '光大银行', '601939': '建设银行',
             '601988': '中国银行', '601998': '中信银行'}

code_list = list(stock_dict.keys());
name_list = list(stock_dict.values());

n = len(stock_dict)
pvalue_matrix = np.ones((n, n))

matched_code_dict = {}
matched_name_dict = {}

matched_code_list = []
matched_name_list = []

for i in range(n):
    for j in range(i+1, n):
        stock1 = ts.get_hist_data(code_list[i], start, end)[::-1]
        stock2 = ts.get_hist_data(code_list[j], start, end)[::-1]
        
        result = sm.tsa.stattools.coint(stock1[price_type], stock2[price_type])
        pvalue = result[1]
        pvalue_matrix[i, j] = pvalue
        
        print(name_list[i], name_list[j], pvalue)
        
        if pvalue < 0.05:
            matched_code_dict[code_list[i] + ',' + code_list[j]] = pvalue
            matched_name_dict[name_list[i] + ',' + name_list[j]] = pvalue

matched_code_list = sorted(matched_code_dict.items(), key=operator.itemgetter(1))
matched_name_list = sorted(matched_name_dict.items(), key=operator.itemgetter(1))
print(matched_name_list)

sns.heatmap(pvalue_matrix, xticklabels=name_list, yticklabels=name_list, cmap='RdYlGn_r', mask = (pvalue_matrix == 1))

n = len(matched_code_list)
for i in range(n):
    code1, code2, pvalue = str(matched_code_list[i]).replace('(', '').replace(')', '').replace('\'', '').split(",")
    stock1 = ts.get_hist_data(code1, start, end)[::-1]
    stock2 = ts.get_hist_data(code2, start, end)[::-1]
            
    X = []
    x = stock1[price_type]
    y = stock2[price_type]
    X = sm.add_constant(x)
    result = (sm.OLS(y,X)).fit()
#    print(result.summary())
    
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(x, y, 'o', label="data" + " " + str(matched_name_list[i]))
    ax.plot(x, result.fittedvalues, 'r', label="OLS" + " " + str(result.params))
    ax.legend(loc='best')
