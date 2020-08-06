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
from scipy import stats

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


#concatenate old+new single DF.       data from 1922-1931 missing!!!!
df=pd.concat([df_old,df_new]).reset_index( drop=True)  

# 3 observations/day. They are summarized in df_date so just one / day
df_date=df.groupby(df.date).median().reset_index()  #median daily obs/ day


#median temperature / year
df_year=df_date.groupby(df_date.date.dt.year).median().reset_index()
df_year.temp[(df_year.date==1922) | (df_year.date==1879)] = 4.5  #according to another source

#years with no data at all
years = np.arange(1863,2021)

years_in_df= np.array(df_year.date)

missing=np.isin(years, years_in_df)

missing_years = years[~missing]
    
dif= df_year.date.iloc[-1]- df_year.date.iloc[0]
dif_len=len(missing_years)
 
#years with insufficient data
year_count=df_date.groupby(df_date.date.dt.year).count()
years_incomplete=year_count[year_count.temp < 365].index.tolist()

#drop years in df_years with incomplete data

n=df_year.date.isin(years_incomplete)

to_drop=df_year.date[n].index.tolist()
                     
df_year.drop( to_drop, axis=0, inplace= True)




#%% Linear regression analysis for year

mymodel=sm.OLS(df_year.temp, df_year.date)

myresults=mymodel.fit()

print (myresults.summary())



#%% Plots for annual evolution

print ('\n \n Years missing: ', missing_years,'\n')
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
ti='median annual temperatures (MAT) in Uppsala'
plt.title(ti)


ax_labels=[int(x)  for x in df_year.date[::10]]
ax.set_xticks(range(0,len(df_year.temp),10))
ax.set_xticklabels(ax_labels,rotation=45)
plt.show()    #evolution of median annual temperatures since 1944

print("""
      Obs!!!
      Omnibus,skewness, kurtosis...points data not normally distributed.
      Though R2 fine nonlinear regression should be used.
      Actually the line looks too flat compared to temp line.
      Short: linear regression model not reliable""")


#%% Comparing each month, whole serie vs last years
df_monthly=df_date.groupby(df.date.dt.month).median()

months=['jan','feb','mar','apr','maj','jun','jul','ago','sep','oct','nov','dec']

df_monthly['std']=0
for i in range (1,13):
    df_monthly.temp.loc[i]=np.median(df_date.temp[(df_date.date.dt.month==i)])
    df_monthly['std'].loc[i]=np.std(df_date.temp[(df_date.date.dt.month==i)])
    
last=2000
df_monthly_21=df_date[df_date.date.dt.year > last]
df_monthly_21_b=df_monthly_21.groupby(df_monthly_21.date.dt.month).median()

df_monthly_21_b['std']=0

for i in range (1,13):
    df_monthly_21_b.temp.loc[i]=np.median(df_date.temp[
        (df_date.date.dt.month==i)][df_date.date.dt.year>last])
    
    df_monthly_21_b['std'].loc[i]=np.std(df_date.temp[
        (df_date.date.dt.month==i)][df_date.date.dt.year>last])


#%% Plotting evolution by month, with std bars
fig2=plt.figure()

ax2=fig2.add_subplot(1,1,1)


#Obs!...0.04 added to improve visualization so markers and error bars don't superimpose.
ax2.errorbar(df_monthly.index -0.04, df_monthly.temp, marker='o', ls='',
             yerr=df_monthly['std'], capsize=3, label='whole serie')

ax2.errorbar(df_monthly_21_b.index +0.04, df_monthly_21_b.temp, marker='o', ls='',
             yerr=df_monthly_21_b['std'] , capsize=3, label = 'After 2000')



ax2.grid(axis='y')
ax2.set_ylabel('Temp C')


ti='median temp(daytime) by moth since 1863  in Uppsala'
plt.title(ti)
plt.legend(loc=2)

#ax2_labels=[int(x)  for x in df_year.date[::10]]
ax2.set_xticks(range(1,13))
ax2.set_xticklabels(months)
plt.show()   

#%% Statiscal significance of monthly differences 2000s - whole serie

#Wilcoxon rank sum (non normally distributed, independient variables)

month_stats=np.zeros((12,3))

for i in range(0,12):
    y=df_date.temp[(df_date.date.dt.month==i+1) & (df_date.date.dt.year > 2000)]
    x=df_date.temp[(df_date.date.dt.month==i+1)]
    s, p= stats.ranksums(x,y)
    month_stats[i][0]= i+1
    month_stats[i][1]= np.median(y)-np.median(x)
    month_stats[i][2]= p
    
print ('Wilkoxons sum rank test')
print ('\nMonth     dif/month        p')

aa=0
for ii in month_stats:
    aa=aa+1
    print ('{}         {:.2f}        {:.4f}'.format(months[aa-1], ii[1], ii[2] ) )
    