#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 15:52:45 2019

@author: teodor
"""
import pandas as pd
import numpy as np

data = pd.read_csv("/home/teodor/Documents/birds/testfile.txt", delim_whitespace=True, names=("Date", "Time", "Data"))

dota = pd.DataFrame(columns=["Time", "Data"])
dota.Time = data.Time
print(data)
for i in range(len(data.Data)-1):
    if data.Data[i+1] - data.Data[i] < 0 or data.Data[i+1] - data.Data[i] >= 20:
        dota.Data.loc[i+1] = 0
    elif data.Data[i+1] - data.Data[i] >= 4:
        dota.Data.loc[i+1] = 4
    else:
        dota.Data.loc[i+1] = data.Data[i+1] - data.Data[i]

print(dota)