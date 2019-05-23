#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 14:07:01 2019

@author: teodor
"""
import pandas as pd

df = pd.read_pickle("/home/teodor/hdf.pkl")

def motionperint(data, inp):
    tdata = pd.DataFrame(columns = ["Data", "DateTime"])
    hlist = []
    tlist = []
    s = 0
    for i in range(0,len(data.DateTime)-1):
        if data.Data[i] != 0:
            s += data.Data[i]
        if (inp == "hour" or inp == "h") and (data.DateTime[i].hour != data.DateTime[i+1].hour):
            hlist.append(s)
            tlist.append(data.DateTime[i+1])
            s = 0
            print("ey")
        if (inp == "day" or inp == "d") and (data.DateTime[i].day != data.DateTime[i+1].day):
            hlist.append(s)
            tlist.append(data.DateTime[i+1])
            s = 0
            print("ey")
        if (inp == "month" or inp == "m") and (data.DateTime[i].month != data.DateTime[i+1].month):
            hlist.append(s)
            tlist.append(data.DateTime[i+1])
            s = 0
            print("ey")
        print(100 * i / len(data.DateTime), "%")
    tdata.Data = hlist
    tdata.DateTime = tlist
    if (inp == "hour" or inp == "h"):
        tdata.to_pickle("/home/teodor/hdf.pkl")
    if (inp == "day" or inp == "d"):
        tdata.to_pickle("/home/teodor/ddf.pkl")
    if (inp == "month" or inp == "m"):
        tdata.to_pickle("/home/teodor/mdf.pkl")
    return tdata