# -*- coding: utf-8 -*-
"""
code for programming outdoors watering system based on weather forecast.
Forecast is downloaded from visualcrossing (usern my name, pw Mvdbt3116) in csv.
"""


import requests, os
import http.client
import pandas as pd
from datetime import *
from time import sleep

#%% To understand...
"""
1mm rainfall is equivalent to 1 L per square meter
https://en.wikipedia.org/wiki/Rain#:~:
text=One%20millimeter%20of%20rainfall%20is,8%2Din)%20metal%20varieties.
"""

#%%function to get a datafrane

def get_df():
    
    http.client.HTTPConnection._http_vsn = 10
    http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
    url='https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?aggregateHours=1&combinationMethod=aggregate&contentType=csv&unitGroup=metric&locationMode=single&key=4ABWPS4DREDJACGPF47FVM3NK&dataElements=default&locations=uppsala'
    
    print("Downloading...")
    resp = requests.get(url)
    with open('weather.csv', 'wb') as output:
        output.write(resp.content)
    print("Done!")
    
    df=pd.read_csv('weather.csv',header=0,  usecols=[1,5,6], nrows=24)
    
    df['date_time'] = pd.to_datetime (df['Date time'])
    
    df.drop ('Date time', axis=1, inplace= True)
    
    #df.set_index(['date_time'], inplace=True)
    df.rename( columns={'Chance Precipitation (%)':'prob_rain', 
                        'Precipitation':'pred_rain'}, inplace=True)
    return df

#%%    

logging = open ('log_watering.csv', 'a')
logging.write('date_time,predicted_rain,valve_status\n')

df= get_df()

#%% Getting the string to write in the file

def str_to_log(h):
    
    for i in df.date_time:   #finds time stamp to write in file
            if i.hour == h:
                time_str=str(i)
                rain_cell=  df.pred_rain[ df.date_time == i]
                rain_str= str(  rain_cell.values[0]  )  #!!Obs. how to extract value in a variable
   
    str_to_write= time_str + ',' + rain_str + ',' + valve + '\n'
    
    return str_to_write
    
    
    
#%%  Plan when to open the valve for watering

#watering 1 min 07.00 and 1min 19.00, assuming 1 L / min.

valve='closed'

#while True:

delta=timedelta(hours=2)  #just to check if while loop works, in the future while True
nu=datetime.now()
while nu+delta>datetime.now():
    
    now = datetime.now()
   
    now_string = datetime.strftime( now, '%I%M%S') #I for 12h format
    
    if now.minute != 0 and now.second == 0 and now.hour !=12: 
       
        my_str = str_to_log (now.hour)
        
        logging.write(my_str) 
        
        sleep(1)
        
        print (valve, datetime.now());sleep(1) #!!!!!!!!!!!!!borrame
    
    
    
    elif now_string == '070000':
        
        df = get_df()
        
        #calculates the total rainfall next 12 hours
        
        rain_next_12 = df.pred_rain[1:13].sum()  #not 0:12 cause df from 1 hour before
        
       
        
        if rain_next_12 >1 : 
            
            valve = "holding closed" ; print (valve, datetime.now())
            
            my_str = str_to_log (now.hour)
            
            logging.write(my_str)
            
            sleep (1)
            
            valve = 'closed'
            
            print (valve, datetime.now());sleep(1) #!!!!!!!!!!!!!borrame
        
        else: 
            open_during = timedelta(seconds=60)   
            
            valve='opening'; print (valve, datetime.now())
            
            my_str = str_to_log (now.hour)
            
            logging.write(my_str)
            
            print (valve, datetime.now());sleep(1) #!!!!!!!!!!!!!borrame
            
            
            while now + open_during > datetime.now():
                
                pass
                #print ('valve opened', datetime.now())
            
            
            valve='closed'; print (valve, datetime.now())
        
        
    else:
        
        print (valve, datetime.now());sleep(1) #!!!!!!!!!!!!!borrame
        
        pass

#%% closing log file
        
logging.close()