# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 15:44:28 2017

@author: Admin
"""

import tushare as ts

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
