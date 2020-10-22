# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 21:45:22 2020

@author: marti
"""
#How to download a file from a URL. I copied this exemple from stackoverflow
#download weather forecast for Uppsala in csv format from weather visual crossing. 
#my username my name, my password Mvdbt3116 

import requests, os
import http.client
import pandas as pd
from matplotlib import pyplot as plt
from datetime import *

#%% To understand...
"""
1mm rainfall is equivalent to 1 L per square meter
https://en.wikipedia.org/wiki/Rain#:~:
text=One%20millimeter%20of%20rainfall%20is,8%2Din)%20metal%20varieties.
"""



#%%  Plan when to open the valve for watering

#watering 1 min 07.00 and 1min 19.00, assuming 1 L / min.

valve='closed'

#while True:

delta=timedelta(seconds=30)  #just to check if while loop works, in the future while True
nu=datetime.now()
while nu+delta>datetime.now():
    
    now = datetime.now()
    now_string = datetime.strftime( now, '%I%M%S') #I for 12h format
    
    
    
    if now_string == '062500':
        print ('now')
        http.client.HTTPConnection._http_vsn = 10
        http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
        
       
        url='https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?aggregateHours=1&combinationMethod=aggregate&contentType=csv&unitGroup=metric&locationMode=single&key=4ABWPS4DREDJACGPF47FVM3NK&dataElements=default&locations=uppsala'
        print("Downloading...")
        resp = requests.get(url)
        with open('weather.csv', 'wb') as output:
            output.write(resp.content)
        print("Done!")
        print ()
        
        df=pd.read_csv('weather.csv',header=0,  usecols=[1,5,6], nrows=24)
        
        df['date_time'] = pd.to_datetime (df['Date time'])
        
        df.drop ('Date time', axis=1, inplace= True)
        df.set_index(['date_time'], inplace=True)
        
        valve='open'
        open_during=timedelta(seconds=1)   #opened just 5s for checking,  60s
        while now + open_during > datetime.now():
            valve='open'
            print ('valve opened', datetime.now())
            
        valve='closed'; print ('closing valve')
           
        
    else:
        pass