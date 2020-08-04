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

import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std

np.printoptions(precision=3)
pd.options.mode.chained_assignment = None   #prevent uncomfortable warning messages


#%% Temperatures in Uppsala
#from https://www.smhi.se/data/meteorologi/ladda-ner-meteorologiska-observationer#param=airtemperatureInstant,stations=all,stationid=97520
# 2 weather stations in Uppsala, near Engelska parken. "old" until 1985 and "new" after.

df_new=pd.read_csv('TempUppsala_new.csv',header=9, usecols=(0,1,2),delimiter=';')
df_new.rename(columns={'Datum':'date', 'Tid (UTC)':'time', 'Lufttemperatur':'temp'}, inplace=True)

df_old=pd.read_csv('TempUppsala_old.csv',header=9, usecols=(0,1,2),delimiter=';')
df_old.rename(columns={'Datum':'date', 'Tid (UTC)':'time', 'Lufttemperatur':'temp'}, inplace=True)



df_new.date=pd.to_datetime(df_new.date)
df_new.time=pd.to_datetime(df_new.time, format='%H:%M:%S')

df_old.date=pd.to_datetime(df_old.date)
df_old.time=pd.to_datetime(df_old.time, format='%H:%M:%S')

df=pd.concat([df_old,df_new]).reset_index( drop=True)  #concatenate old+new single DF
#data from 1922-1931 missing!!!!


df_date=df.groupby(df.date).mean().reset_index()  #mean daily obs/ day



df_year=df_date.groupby(df_date.date.dt.year).mean().reset_index()  #mean year obs
df_year.temp[(df_year.date==1922) | (df_year.date==1879)] = 4.5  #according to another source

#years with no data at all
dif= df_year.date.iloc[-1]- df_year.date.iloc[0]
dif_len=dif-len(df_year)
 
#years with insufficient data
year_count=df_date.groupby(df_date.date.dt.year).count()
years_incomplete=year_count[year_count.temp < 365].index.tolist()


#%% Linear regression analysis

mymodel=sm.OLS(df_year.temp, df_year.date)

myresults=mymodel.fit()

print (myresults.summary())


#%% Plots

print ('Years with less than 365 days measured: ', years_incomplete)
print ('{} whole years  missing'.format(dif_len))

fig=plt.figure()

ax=fig.add_subplot(1,1,1)

#ax.plot(df_year.temp[(df_year['date']>1870) & (df_year['date']<2020)])
ax.plot(df_year.temp, label= 'MAT')
ax.plot(df_year.date * myresults.params[0], ls="-", label= 'T = year x 0.0032')

ax.grid(axis='y')
ax.set_ylabel('Temp C')

plt.legend(loc=2)
ti='Mean annual temperatures (MAT) in Uppsala'
plt.title(ti)


ax_labels=[int(x)  for x in df_year.date[::10]]
ax.set_xticks(range(0,len(df_year.temp),10))
ax.set_xticklabels(ax_labels,rotation=45)
plt.show()    #evolution of mean annual temperatures since 1944

print("""
      Obs!!!
      Omnibus,skewness, kurtosis...points data not normally distributed.
      Though R2 fine nonlinear regression should be used.
      Actually the line looks too flat compared to temp line.
      Short: linear regression model not reliable""")


