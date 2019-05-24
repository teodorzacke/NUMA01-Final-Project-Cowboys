#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 19:16:43 2019

@author: teodor
"""

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

tdf, hdf, ddf, wdf = pd.read_pickle("/home/teodor/conclusive/tdf.pkl"),pd.read_pickle("/home/teodor/conclusive/hdf.pkl"),pd.read_pickle("/home/teodor/conclusive/ddf.pkl"),pd.read_pickle("/home/teodor/conclusive/wdf.pkl")

#def inint(df, start, stop):
if "DateTime" in hdf.columns:
    hdf.set_index('DateTime',inplace=True)
ttdf = hdf["2015-03-01":"2015-03-09"].reset_index()
fig, ax = plt.subplots()
plt.bar([i for i in ttdf.DateTime], [i for i in ttdf.Data], width=len(ttdf) * 0.0001)
plt.grid()  
fig.autofmt_xdate()
ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    
    
def amint(df, start, stop):
    if "DateTime" in df.columns:
        df.set_index('DateTime',inplace=True)
        ttdf = df[start:stop]
        return ttdf.Data.sum()
    else:
        return df.Data[start:stop].sum()
    
#plt.bar([i for i in hdf.DateTime], [i for i in hdf.Data], width = 0.5)
