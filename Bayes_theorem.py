# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 07:36:07 2020

@author: maf011
"""


# Bayes theorem P(A|B) = P(B|A) x P(A) / P(B) 

# How P(A|B) changes depending on the probability of P(A) and P(B)

# E.g. what is the probability of having corona (A)..
#... if you have feber(B)

import numpy as np
import matplotlib.pyplot as plt
np.printoptions(precision=3)

#%% creating a matrix 

p_B_A=0.75

AxB=np.zeros((50,50))

#P(A) in axis=0, first row. P(B) in axis=1, first column. My convention

AxB[0,:]=np.linspace(0,0.3,num=50)

AxB[:,0]=np.linspace(0,0.6,num=50)

for i in range (1,50):      
    for j in range (1,50):
        
        #here is the core of the theorem
        AxB[i,j] = AxB[0,i] * p_B_A / AxB[j,0]
        if AxB[i,j] > 1 :
            AxB[i,j]= 0
            
        
#%%
            

#%% plotting
       

# now with focus in P(B)
fig=plt.figure('Bayes',figsize=(8,4),facecolor=('0.9'),edgecolor='black')

ax=fig.add_subplot(1,1,1)

for i in range (1,50,10):
    start=1
    for j in range (1,50):
        if AxB[i,j]> 0:
            break
        else:
            start=j+1
            
    lab='P(A)=' + str(np.around(AxB[0,i],decimals=2))
    ax.plot(AxB[start:,0],AxB[i,start:], label=lab)
    
    ax.set_ylabel('P(A|B) e.g. having Covid19 in the presence of feber')
    ax.set_xlabel('P(B) , e.g. presence of feber in the population')
    ax.set_title('Bayes theorem. P(A|B) = P(B|A) x P(A) / P(B) ')
    ax.legend(loc=1)

plt.show()


