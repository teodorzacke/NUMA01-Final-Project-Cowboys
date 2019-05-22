#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:02:02 2019

@author: teodor
"""

#plottus
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
import datetime
import matplotlib.dates as mdates

df = pd.read_csv("/home/teodor/Documents/birds/testfile.txt", delim_whitespace=True, names=("Date", "Time", "Data"))

dota = pd.DataFrame(columns=["Time", "Data"])
dota.Time = df.Time
df.Data = df.Data.diff()

for i in range(1,len(df.Data)):
    if df.Data[i] < 0 or df.Data[i] >= 20:
        df.Data.iloc[i] = 0
    elif df.Data[i] >= 4:
        df.Data.iloc[i] = 4

df.Data.iloc[0] = 0
df.Data = df.Data.astype(int)
print(df)


def merge_columns(df, col_1 ="Date", col_2 ="Time", col_new ="DateTime"):
    df[col_new] = df[col_1] + " " + df[col_2]
    del df[col_1]
    del df[col_2]
    return(df)
    
merge_columns(df)
df["DateTime"] = pd.to_datetime((df["DateTime"]),utc=True, format=("%Y-%m-%d %H:%M:%S.%f"))



df.set_index('DateTime',inplace=True)
#
##plot df
#fig, ax = plt.subplots(figsize=(150,70))
#ax.bar(df.index, df['Data'], width=0.005)
#
##set ticks every week
#ax.xaxis.set_major_locator(mdates.DayLocator())
##set major ticks format
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%D'))
#plt.xticks(rotation='vertical')
##plt.figure
##plt.bar(range(len(df.Data)),[i for i in df.Data])