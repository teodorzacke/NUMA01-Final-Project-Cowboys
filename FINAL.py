# -*- coding: utf-8 -*-
"""
Created on Fri May 24 18:00:18 2019
@author: stina
"""
from  scipy import *
from  matplotlib.pyplot import *
import numpy as np
from astral import *
from datetime import date
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
import datetime
import matplotlib.dates as mdates
import os
    
# STEG ETT! Läs in koden

#df = pd.read_csv("/home/teodor/Documents/birds/bird_jan25jan16.txt", delim_whitespace=True, names=("Date", "Time", "Data"))

# Steg två! Gör om datumen till datetime-objekt.

def merge_columns(df, col_1 ="Date", col_2 ="Time", col_new ="DateTime"): #Defining and renaming the columns.
    df[col_new] = df[col_1] + " " + df[col_2] #Defining col_new as the merge of the other two columns. We have " " because we want a space between the columns.
    del df[col_1] #Deleting the columns...
    del df[col_2]
    return(df)
   
def toDate(df): #Making the column into datetime object.
    merge_columns(df)
    df["DateTime"] = pd.to_datetime((df["DateTime"]),utc=True, format=("%Y-%m-%d %H:%M:%S.%f"))
    df.DateTime = df.DateTime.dt.tz_convert('Europe/Stockholm') #Setting local timezone.
    return df
    

# Steg tre: Kolla om det finns en tidsskillnad mellan två rader och om det gör det, fyll i.
def tidsskillnad(vardelis, tidlista):

    for i in range(len(tidlista) - 1):
        if (tidlista[i+1].minute - tidlista[i].minute >= 3): #Om tidsindexen som är före är 3 minuter "större" än den nuvarande indexen så adderar vi två minuter och lägger till som ny rad.
            avgie = (vardelis[i+1] + vardelis[i]) / 2 #Det vi gör här är att vi fyller i vår "Data" column med medelvärdet av [i] och [i+1].
            timie = (tidlista[i] + datetime.timedelta(minutes = 2)) #Här så adderar vi 2 minuter till vårt tidsindex.
            vardelis.insert(i+1, avgie)
            tidlista.insert(i+1, timie)
    return vardelis, tidlista

# Steg fyra: Behandla datan genom att ta hitta extrema skillnader mellan tidigare och efterkommande värden.
def extremlish(vardelis):
    for i in range(1,len(vardelis)-1): # -1 för att vi kan inte gämföra något med sista värdet. ([i-1]>[i] och [i+1]>[i] och ( [i+1]==[i-1] eller [i+1]-1 == [i-1] ) betyder: Om vårt index är mindre än förra och nästa index och dessa två index är lika med varandra eller nästa index är förraindex+1 så;)
        if vardelis[i - 1] > vardelis[i] and vardelis[i + 1] > vardelis[i] and (vardelis[i+1] == vardelis[i-1] or vardelis[i+1] - 1 == vardelis[i - 1]):
            vardelis[i] = (vardelis[i-1] + vardelis[i+1]) / 2 #gör vi att vårt index blir medelvärdet av förra och nästa index.
    return vardelis

# Steg fem: Hitta differensen mellan värde och nästkommande värde.

def diffus(vardelis, tidlista):
    tdf = pd.DataFrame(columns = ["Data", "DateTime"])
    tdf.Data = vardelis
    tdf.DateTime = tidlista
    tdf.Data = tdf.Data.diff() #Vi gjorde en ny dataframe. Och sätter Data till differansen av indexen (alltså typ differansen av [i-1] med [i])
    tidlista = [i for i in tdf.DateTime]
    vardelis = [i for i in tdf.Data] #Gör det för alla.
    
    for i in range(1,len(vardelis)): #Fixar vissa datafel:
        if vardelis[i] < 0 or vardelis[i] >= 20: #Om differansen är 20 eller över så sätter vi differansen till 0 (på grund av "biologiska fel")
            vardelis[i] = 0
        elif vardelis[i] >= 4: #Om differansen är mellan 4 och 20 så sätter vi differansen till 4.
            vardelis[i] = 4
    
    tdf.Data = vardelis
    tdf.DateTime = tidlista
    tdf.Data.iloc[0] = 0 #Sätter differansen på första raden till noll eftersom den inte kan gämföra med någon tidigare rad.
    tdf.Data = tdf.Data.astype(int) #För martin sa det var finare...
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
        if data[i] != 0: #Om data inte är noll adderar vi detta värde till s.
            s += data[i]
        if inp == "hour" and (time[i].hour != time[i+1].hour and (time[i].minute <= 2 or time[i].minute >= 58)):
            nytime.append(time[i+1]) #Om nästa index (för timme) är annorlunda än detta index och minutrarna är mellan intervallet av en timme så lägger vi in nästa intervall och s.
            nydata.append(s)
            s = 0 #Återställer countern. Så att nästa iteration får data för bara den timmen.
        elif inp == "day" and (time[i].day != time[i+1].day and (time[i].minute <= 2 or time[i].minute >= 58)) and (time[i].hour <= 1 or time[i].hour >= 23): #exakt samma sak fast för intervallet dag.
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

#Slänger in alla våra previously definerade funktioner och spottar ut dataframes för data per ; timme, dag, vecka och 2minut.
def snoppyboppy(path):
    df = pd.read_csv(path, delim_whitespace=True, names=("Date", "Time", "Data"))
    df = toDate(df) #Importerar till datetime obj.
    
    tidlista = [i for i in df.DateTime] #Ny column för DateTime.
    vardelis = [i for i in df.Data]
    
    vardelis, tidlista = tidsskillnad(vardelis, tidlista) #Importerar vår tidsfunktion.
    vardelis = extremlish(vardelis) #Importerar vår funktion för extrema dataskillnader.
    tdf = diffus(vardelis, tidlista) #Importerar funktionen som gör om till "diff"
    hdf, ddf, wdf = timint(tdf, "hour"), timint(tdf, "day"), timint(tdf, "week") #Importerar vår funtion för våra indelningar mellan dag vecka månad.
    return hdf, ddf, wdf, tdf


#Gör en lista med alla tider för soluppgång och solnedgång.
def whatThatSunDo(df):
    location = Location(info = ('ICA Kvantum, Södra Dalby', 'Sweden', 55.717, 13.343, 'Europe/Stockholm', 0))
    location.timezone = 'Europe/Stockholm'
    timezone = location.timezone
    solar_depression = 'civil'
    print('Information for %s' % location.name)
    print('Timezone: %s' % timezone)
    print('Latitude: %.3f; Longitude: %.3f' % (location.latitude, location.longitude))
    #Skapat en location (med tidszon) för att plocka soluppgång och solnedgångs värden från.
    
    rise = []
    if not "DateTime" in df: #Försäkrar oss om att vi inte har "DateTime" som vår index (då detta används i vissa delar av vår kod). Så vi återställer den till vanlig index.
        df = df.reset_index()
    sett = []
    sun = location.sun(date=df.DateTime[0].date()) #Sätter och kollar första datum för vi saknar ett värde i vår lista.
    rise.append(sun['dawn']) #Appendar första datumet till våra listor.
    sett.append(sun['dusk'])
    for i in range(1, df.shape[0]): #Börjar på 1 och kör i en range hela df listan (så df-1).
        if df.DateTime[i-1].day != df.DateTime[i].day: #Kollar om i-1 är en annan dag gämfört med i.
            sun = location.sun(date=df.DateTime[i].date()) #Appendar vår location med sun fucntionen som jag tror finns i astral. Sätter alla datum till datumen från vår df.
            sunrise = sun['dawn'] #Astrals function för att kolla sunrise och sunset för olika datum.
            rise.append(sunrise) #Appendar till våra listor för alla datum i df.
            sunset = sun['dusk']
            sett.append(sunset)
#            print(df.DateTime[i].day)
#            print('Sunrise: {} Sunset: {}'.format(sunrise, sunset))
    sun = location.sun(date=(df.iloc[-1].DateTime + timedelta(days = 1)).date()) #gör ett nytt datum som är sista datumet för vi behöver en extra. Så sista datumet i listan + en dag.
    rise.append(sun['dawn'])#Appendar sista datumet i listorna.
    sett.append(sun['dusk'])
    return list(zip(sett,rise)) #Vi zippar ihop dessa till en ny lista med tuples.

#Fixar så att vi kan visa all data i plots med nattid som gråa bars. Välj df för h,d,w,t. night=True för att visa natt-bars. Justera width om det behövs. :)
    
def KENT_AGENT(df, start, stop, night=None):
    ddf = pd.read_pickle("./ddf.pkl")
    ddf.set_index("DateTime", inplace=True)
    if "DateTime" in df.columns: #Om "DateTime" inte är vårt index så gör vi den till det. (För index räknas inte som column!)
        df.set_index('DateTime',inplace=True)
    ttdf = df[start:stop].reset_index() #Vi behöver en temporär temporär indexerad dataframe som vi sedan kan skapa en lista av (xlist).
    fig, ax = plt.subplots()
    xlist = [i for i in ttdf.DateTime]
    barWidth = np.min(np.diff(mdates.date2num(xlist))) #Ändrar på barWidth. len() för då blir bredden i procent av x-axeln.
    if night == True:
        span = whatThatSunDo(ttdf)
        for i in range(len(span)-1): #Raden under kollar från span[i][0] vilket är solnedgång i rad [i] och span[i+1][1] vilket är soluppgång för nästa dag(rad). (Första bracketen säger vilken index i DateTime saken och andra är om det är solupp eller solner.) 
            plt.axvspan(span[i][0], span[i+1][1], facecolor = "grey", alpha = 0.5) #axvspan är funktionen för att fylla i mellan solnedgång och soluppgång.
        plt.axvspan(xlist[0], span[0][1], facecolor = "grey", alpha = 0.5)
    plt.bar(xlist, [i for i in ttdf.Data], width=barWidth) #Plottar vår Data från ttdf. Med DateTime som x-axel.
    plt.xticks(rotation = -45)

def plot(start, stop, night):
    dstart = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    dstop = datetime.datetime.strptime(stop, "%Y-%m-%d %H:%M:%S")
    if dstop - dstart <= datetime.timedelta(days = 7):
        KENT_AGENT(hdf, start, stop, night)
    elif dstop - dstart > datetime.timedelta(days = 7) and dstop - dstart < datetime.timedelta(months = 182):
        KENT_AGENT(ddf, start, stop, night)
    else:
        KENT_AGENT(wdf, start, stop, night)

#Om du inte har dessa filer på din dator så kommer du kunna skapa dem i en vald path. Du behöver bara göra detta en gång! Vilket gör att vår kod är mycket snabbare! :D    
if os.path.isfile("./tdf.pkl") and os.path.isfile("./hdf.pkl") and os.path.isfile("./ddf.pkl") and os.path.isfile("./wdf.pkl"):
    tdf, hdf, ddf, wdf = pd.read_pickle("./tdf.pkl"), pd.read_pickle("./hdf.pkl"), pd.read_pickle("./ddf.pkl"), pd.read_pickle("./wdf.pkl")
else:
    print("Enter your file path.")
    inp = input()
    hdf, ddf, wdf, tdf = snoppyboppy(inp)
    hdf.to_pickle("./hdf.pkl")
    ddf.to_pickle("./ddf.pkl")
    wdf.to_pickle("./wdf.pkl")
    tdf.to_pickle("./tdf.pkl")
