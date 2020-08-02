# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 08:00:01 2020

@author: marti
"""


# Uppsala. Temperatures variation since 1944 (Uppsala's airport)



import numpy as np
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
np.printoptions(precision=3)

#%% Temperatures in Uppsala
#from https://www.smhi.se/data/meteorologi/ladda-ner-meteorologiska-observationer#param=airtemperatureInstant,stations=all,stationid=97530

df=pd.read_csv('TempUppsala.csv',header=9, usecols=(0,1,2),delimiter=';')
df.rename(columns={'Datum':'date', 'Tid (UTC)':'time', 'Lufttemperatur':'temp'}, inplace=True)

df.date=pd.to_datetime(df.date)
df.time=pd.to_datetime(df.time, format='%H:%M:%S')

df_date=df.groupby(df.date).mean().reset_index()

df_year=df_date.groupby(df_date.date.dt.year).mean().reset_index()
#df_year.set_index('date')




#%% Plots



plt.plot(df_year.temp[(df_year['date']>1944) & (df_year['date']<2020)])
plt.grid(axis='y')
ti='Mean annual temperatures'
plt.title(ti)


#plt.set_xtick(range(0,len(df_year)))
#plt.set_xticklabels(df_year['date'],rotation=45)
plt.show()    #evolution of mean annual temperatures since 1944


