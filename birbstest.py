# -*- coding: utf-8 -*-
"""
Created on Wed May 22 14:41:39 2019
@author: stina
"""
from tkinter import *
import tkinter
from tkinter import ttk, messagebox
from  scipy import *
from  pylab import *
from numpy import *
from astral import Astral


import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime
from pytz import timezone
from dateutil.parser import parse
import pandas as pd

from matplotlib.pyplot import figure
figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')

df = pd.read_csv("/Users/rolandmagndahl/Documents/Birds/bird_jan25jan16.txt",
                   delim_whitespace=True, names=("Date", "Time", "Data"))
#pd['Date'] = pd['Date'].astype('datetime64[ns]')
def merge_columns(df, col_1 ="Date", col_2 ="Time", col_new ="DateTime"):
    df[col_new] = df[col_1] + " " + df[col_2]
    del df[col_1]
    del df[col_2]
    return(df)
    
merge_columns(df)
df["DateTime"] = pd.to_datetime((df["DateTime"]),utc=True, format=("%Y-%m-%d %H:%M:%S.%f"))
print(df["DateTime"])
