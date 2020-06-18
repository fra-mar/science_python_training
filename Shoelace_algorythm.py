#!/usr/bin/env python
# coding: utf-8

# In[1]:


#training with numpy showlace algorithm.

#It's an equation to solve the area of simple polygons (no holes, no sides overlapping)
#here I use for convinience symmetrical polygons...but I could add some randomness to make them irregular...
#The exercise is to do it without python loops

#see https://en.wikipedia.org/wiki/Shoelace_formula

import numpy as np
from random import *

from matplotlib import pyplot as plt

np.set_printoptions(precision=3,floatmode='unique') #Will write floats with just 3 decimals


# In[2]:


#polygon with n sides   I add some randomness for fun
radius=100
n=input ('Polygon...how many sides? \n')
n=int(n)
coordinates=np.zeros(n+1,dtype=[('x','f8'),('y','f8')])

interval=2*np.pi/n  #radians

rndx=np.random.normal(0,100/n,n+1)  # 100/n to limit randomness (overlapping) with higher number of sides
rndy=np.random.normal(0,100/n,n+1)
for i in range(0,n):
    coordinates[i][0]=radius*np.cos(i*interval)   +rndx[i]
    coordinates[i][1]=radius*np.sin(i*interval)   +rndy[i]
coordinates[-1]=coordinates[0]
#print (coordinates)

plt.figure(figsize=(6,6))
plt.plot(coordinates['x'],coordinates['y'],ls='--',marker='o')
plt.show()



#calculate coordinates if 0 at the center.


# In[3]:


#calculate s1 and s2 by slicing
xS1=coordinates['x'][:-1]
yS1=coordinates['y'][1:]
S1_array=xS1*yS1
S1=np.sum(S1_array)

xS2=coordinates['x'][1:]
yS2=coordinates['y'][:-1]
S2_array=xS2*yS2
S2=np.sum(S2_array)

area=(S1-S2)/2

print (str(area), 'squared units')
area_circle= np.pi*(radius**2)
print ('compare with area circle radius=',radius,' :', area_circle )

