# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 07:36:07 2020

@author: maf011
"""


# Alveolar gas equation: P((alv))O2 = ( Patm-Ph2o)*FiO2 - PCO2 / r

# This code explores how P(A)O2 changes with FiO2 and PaCO2



import numpy as np
import matplotlib.pyplot as plt
np.printoptions(precision=3)

#%% AtmPressures in Uppsala
#from https://www.smhi.se/data/meteorologi/ladda-ner-meteorologiska-observationer#param=airPressure,stations=all,stationid=97520

dt=([('date','|S10'),('time','|S10'),('hPa','f8')])
pressure=np.genfromtxt('AtmPressUppsala.csv',dtype=dt,skip_header=10,
                       usecols=(0,1,2),delimiter=';')
a=pressure['hPa']

plt.hist(pressure['hPa'],bins=50)
plt.show()

mean, std = np.mean(a), np.std(a)



#%% creating a matrix 

RQ=0.75
Pwater=47*(101.3/760)
Patm = 101.2     #to compare, 4000m Patm= 60KPa, 9000m Patm= 30KPa
                 #record low/high Patm ever recorded are 87-108.38
                # or mean 1012hPa, +/-2std (988.11-1024.29 hPa)

FxCO2=np.zeros((50,50))

#FiO2 first row (axis=0).  PCO2 first column (axis=1)

FxCO2[0,:]=np.linspace(0.21,0.3,num=50)

FxCO2[:,0]=np.linspace(3,10,num=50)

for i in range (1,50):      
    for j in range (1,50):
        
        #Calculates PA O2 for every FiO2 and PaCO2
        FxCO2[i,j] = FxCO2[0,i] * (Patm - Pwater) - FxCO2[j,0] / RQ
        
            
        
#%%
            

#%% plotting
       

print ("""

""")

fig=plt.figure('Bayes',figsize=(8,4),facecolor=('0.9'),edgecolor='black')

ax=fig.add_subplot(1,1,1)

for i in range (1,50,10):
    start=1
    for j in range (1,50):    #to start plotting where P(A|B)<=1
        if FxCO2[i,j]> 0:
            break
        else:
            start=j+1
            
    lab='FiO2=' + str(np.around(FxCO2[0,i],decimals=2))
    ax.plot(FxCO2[start:,0],FxCO2[i,start:], label=lab)
    
    ax.set_ylabel('O2 alveolar partial pressure (KPa)')
    ax.set_xlabel('PaCO2 (KPa)')
    ax.set_title('Alveolar gas equation PAO2 =  (Patm-Pwater)*FiO2 - PaCO2/R')
    ax.legend(loc=1)

plt.show()





