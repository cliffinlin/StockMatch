# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 22:51:21 2017

@author: Admin
"""
import numpy as np
import matplotlib.pyplot as plt
import operator
import seaborn as sns
import statsmodels.api as sm
import tushare as ts

from datetime import date
from statsmodels.tsa.stattools import coint

def zscore(series):
    return (series - series.mean()) / np.std(series)

#print(ts.__version__)

##金融行业:
#code_name_dict = {'600000': '浦发银行', '600015': '华夏银行', '600016': '民生银行', '600030': '中信证券', '600036': '招商银行', '600109': '国金证券', '600291': '西水股份', '600369': '西南证券', '600643': '爱建集团', '600705': '中航资本', '600816': '安信信托', '600830': '香溢融通', '600837': '海通证券', '600958': '东方证券', '600999': '招商证券', '601009': '南京银行', '601099': '太平洋', '601166': '兴业银行', '601169': '北京银行', '601198': '东兴证券', '601288': '农业银行', '601318': '中国平安', '601328': '交通银行', '601336': '新华保险', '601377': '兴业证券', '601398': '工商银行', '601555': '东吴证券', '601601': '中国太保', '601628': '中国人寿', '601688': '华泰证券', '601788': '光大证券', '601818': '光大银行', '601901': '方正证券', '601939': '建设银行', '601988': '中国银行', '601998': '中信银行', '000001': '平安银行', '000166': '申万宏源', '000415': '渤海金控', '000563': '陕国投Ａ', '000686': '东北证券', '000712': '锦龙股份', '000728': '国元证券', '000750': '国海证券', '000776': '广发证券', '000783': '长江证券', '002142': '宁波银行', '002500': '山西证券', '002673': '西部证券', '002736': '国信证券'}
#code_name_dict = {'601818': '光大银行', '601328': '交通银行'}
code_name_dict = {'601018': '宁波港', '601766': '中国中车', '603333': '明星电缆', '601985': '中国核电', '600026': '中远海能', '600115': '东方航空', '601866': '中远海发', '600157': '永泰能源',  '600795': '国电电力', '000883': '湖北能源', '000969': '安泰科技', '601328': '交通银行', '600470': '六国化工', '601818': '光大银行',  '002160': '常铝股份', '000825': '太钢不锈', '000421': '南京公用','600660': '福耀玻璃'}

sns.set_style('whitegrid',{'font.sans-serif':['simhei','Arial']})

start = "2016-1-1"
end = date.today().strftime("%Y-%m-%d")
ktype = 'D'
price_type = "close"

code_stock_dict = {}

n = len(code_name_dict)
pvalue_matrix = np.ones((n, n))

code_list = list(code_name_dict.keys())
name_list = list(code_name_dict.values())

matched_code_dict = {}
matched_name_dict = {}

matched_code_list = []
matched_name_list = []

print("loading stock...")
max_data_len = 0
for code in code_name_dict:
    if ktype == 'M' or ktype == 'W' or ktype == 'D':
        stock = ts.get_hist_data(code, start, end, ktype)[::-1]
    else:
        stock = ts.get_k_data(code, start, end, ktype)[::-1]

    code_stock_dict[code] = stock
#    print(stock)
    print(code_name_dict[code], len(stock))
    
    data_len = len(list(stock[price_type]))
    if data_len > max_data_len:
        max_data_len = data_len

print("max_data_len =" , max_data_len)

for i in range(n):
    for j in range(i+1, n):
        code1 = code_list[i]
        name1 = name_list[i]
        stock1 = code_stock_dict[code1]
        
        code2 = code_list[j]
        name2 = name_list[j]
        stock2 = code_stock_dict[code2]
        
        data_len1 = len(stock1)
        data_len2 = len(stock2)
        if (data_len1 != data_len2):
            print(data_len1, data_len2)
            continue
        
        result = coint(stock1[price_type], stock2[price_type])
        pvalue = result[1]
        pvalue_matrix[i, j] = pvalue
        
        print(name_list[i], name_list[j], pvalue)
        
        if pvalue < 0.05:
            matched_code_dict[code1 + ',' + code2] = pvalue
            matched_name_dict[name1 + ',' + name2] = pvalue

matched_code_list = sorted(matched_code_dict.items(), key=operator.itemgetter(1))
matched_name_list = sorted(matched_name_dict.items(), key=operator.itemgetter(1))
print(matched_name_list)

sns.heatmap(pvalue_matrix, xticklabels=name_list, yticklabels=name_list, cmap='RdYlGn_r', mask = (pvalue_matrix == 1))

n = len(matched_code_list)
for i in range(n):
    code1, code2, pvalue = str(matched_code_list[i]).replace('(', '').replace(')', '').replace('\'', '').split(",")
    
    if ktype == 'M' or ktype == 'W' or ktype == 'D':
        stock1 = ts.get_hist_data(code1, start, end, ktype)[::-1]
        stock2 = ts.get_hist_data(code2, start, end, ktype)[::-1]
    else:
        stock1 = ts.get_k_data(code1, start, end, ktype)[::-1]
        stock2 = ts.get_k_data(code2, start, end, ktype)[::-1]
            
    X = []
    x = stock1[price_type]
    y = stock2[price_type]
    X = sm.add_constant(x)
    result = (sm.OLS(y,X)).fit()
#    print(result.summary())
    
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(x, y, 'o', label="data" + " " + ktype + " " + str(matched_name_list[i]))
    ax.plot(x, result.fittedvalues, 'r', label="OLS" + " " + str(result.params))
    ax.legend(loc='best')
