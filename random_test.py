# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 15:44:28 2017

@author: Admin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(100)
x = np.random.normal(0, 1, 500)
y = np.random.normal(0, 1, 500)
X = pd.Series(np.cumsum(x)) + 100
Y = X + y + 30
for i in range(500):
    X[i] = X[i] - i/10
    Y[i] = Y[i] - i/10
plt.plot(X)
plt.plot(Y)
plt.xlabel("Time"); plt.ylabel("Price");
plt.legend(["X", "Y"]);

plt.plot(Y-X);
plt.axhline((Y-X).mean(), color="red", linestyle="--");
plt.xlabel("Time"); plt.ylabel("Price");
plt.legend(["Y-X", "Mean"]);
