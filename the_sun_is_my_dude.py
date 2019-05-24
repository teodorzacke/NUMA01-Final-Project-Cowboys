# -*- coding: utf-8 -*-
"""
Created on Fri May 24 12:19:42 2019
@author: stina
"""
from  scipy import *
from  matplotlib.pyplot import *
import numpy as np
import pandas as pd


from astral import *
from datetime import date
from datetime import datetime

df = pd.read_pickle("/Users/rolandmagndahl/Documents/Birds/df.pkl")

location = Location(info = ('ICA Kvantum, Södra Dalby', 'Sweden', 55.717, 13.343, 'Europe/Stockholm', 0))
location.timezone = 'Europe/Stockholm'
timezone = location.timezone
solar_depression = 'civil'

print('Information for %s' % location.name)
print('Timezone: %s' % timezone)
print('Latitude: %.3f; Longitude: %.3f' % (location.latitude, location.longitude))

def whatThatSunDo(df):
    chirre = []
    birre = []
    for i in range(df.shape[0]-1):
        if df.DateTime[i].day != df.DateTime[i+1].day:
            sun = location.sun(date=df.DateTime[i].date())
            sunrise = sun['sunrise']
            chirre.append(sunrise)
            sunset = sun['sunset']
            birre.append(sunset)
            #print('Sunset: {} Sunrise: {}'.format(sunrise, sunset))
    return chirre, birre

whatThatSunDo(df)
