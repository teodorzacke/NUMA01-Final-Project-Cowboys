#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 15:05:31 2019

@author: Teodor Zacke
"""

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
import datetime
import matplotlib.dates as mdates

# STEG ETT! Läs in koden

#df = pd.read_csv("/home/teodor/Documents/birds/bird_jan25jan16.txt", delim_whitespace=True, names=("Date", "Time", "Data"))

# Steg två! Gör om datumen till datetime-objekt.

def merge_columns(df, col_1 ="Date", col_2 ="Time", col_new ="DateTime"):
    df[col_new] = df[col_1] + " " + df[col_2]
    del df[col_1]
    del df[col_2]
    return(df)
   
def toDate(df):
    df
    merge_columns(df)
    df["DateTime"] = pd.to_datetime((df["DateTime"]),utc=True, format=("%Y-%m-%d %H:%M:%S.%f"))
    df.DateTime = df.DateTime.dt.tz_convert('Europe/Stockholm')
    return df
    

# Steg tre: Kolla om det finns en tidsskillnad mellan två rader och om det gör det, fyll i.
def tidsskillnad(vardelis, tidlista):

    for i in range(len(tidlista) - 1):
        if (tidlista[i+1].minute - tidlista[i].minute >= 3):
            avgie = (vardelis[i+1] + vardelis[i]) / 2
            timie = (tidlista[i] + datetime.timedelta(minutes = ((tidlista[i+1].minute - tidlista[i].minute)/2)))
            vardelis.insert(i+1, avgie)
            tidlista.insert(i+1, timie)
    return vardelis, tidlista

# Steg fyra: Behandla datan genom att ta hitta extrema skillnader mellan tidigare och efterkommande värden.
def extremlish(vardelis):
    for i in range(1,len(vardelis)-1):
        if vardelis[i - 1] > vardelis[i] and vardelis[i + 1] > vardelis[i] and (vardelis[i+1] == vardelis[i-1] or vardelis[i+1] - 1 == vardelis[i - 1]):
            vardelis[i] = (vardelis[i-1] + vardelis[i+1]) / 2
    return vardelis

# Steg fem: Hitta differensen mellan värde och nästkommande värde.

def diffus(vardelis, tidlista):
    tdf = pd.DataFrame(columns = ["Data", "DateTime"])
    tdf.Data = vardelis
    tdf.DateTime = tidlista
    tdf.Data = tdf.Data.diff()
    tidlista = [i for i in tdf.DateTime]
    vardelis = [i for i in tdf.Data]
    
    for i in range(1,len(vardelis)):
        if vardelis[i] < 0 or vardelis[i] >= 20:
            vardelis[i] = 0
        elif vardelis[i] >= 4:
            vardelis[i] = 4
    
    tdf.Data = vardelis
    tdf.DateTime = tidlista
    tdf.Data.iloc[0] = 0
    tdf.Data = tdf.Data.astype(int)
    return tdf
#print(tdf)

# Steg sex: Sortera i intervall av timmar, dagar, månader.

def timint(df, inp):
    data = [i for i in df.Data]
    time = [i for i in df.DateTime]
    nydata = []
    nytime = []
    s = 0
    for i in range(len(data)-1):
        if data[i] != 0:
            s += data[i]
        if inp == "hour" and (time[i].hour != time[i+1].hour and (time[i].minute <= 2 or time[i].minute >= 58)):
            nytime.append(time[i+1])
            nydata.append(s)
            s = 0
        elif inp == "day" and (time[i].day != time[i+1].day and (time[i].minute <= 2 or time[i].minute >= 58)) and (time[i].hour <= 1 or time[i].hour >= 23):
            nytime.append(time[i+1])
            nydata.append(s)
            s = 0
        elif inp == "week" and (time[i].week != time[i+1].week and (time[i].minute <= 2 or time[i].minute >= 58)) and (time[i].hour <= 1 or time[i].hour >= 23) and (time[i].weekday()  == 6):
            nytime.append(time[i+1])
            nydata.append(s)
            s = 0
    dodi = pd.DataFrame(columns = ["Data","DateTime"])
    dodi.Data = nydata
    dodi.DateTime = nytime
    return dodi

def snoppyboppy(path):
    df = pd.read_csv(path, delim_whitespace=True, names=("Date", "Time", "Data"))
    df = toDate(df)
    
    tidlista = [i for i in df.DateTime]
    vardelis = [i for i in df.Data]
    
    vardelis, tidlista = tidsskillnad(vardelis, tidlista)
    vardelis = extremlish(vardelis)
    tdf = diffus(vardelis, tidlista)
    hdf, ddf, wdf = timint(tdf, "hour"), timint(tdf, "day"), timint(tdf, "week")
    return hdf, ddf, wdf, tdf
    
hdf, ddf, wdf, tdf = snoppyboppy("/home/teodor/Documents/birds/bird_jan25jan16.txt")

def inint(df, start, stop):
    df.set_index('DateTime',inplace=True)
    ttdf = df[start:stop].reset_index()
    df = df.reset_index()
    plt.bar([i for i in ttdf.DateTime], [i for i in ttdf.Data], width = 0.5)
    plt.xticks(rotation = -45)
    
    

