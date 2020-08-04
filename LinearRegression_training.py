#!/usr/bin/env python
# coding: utf-8

# In[52]:



import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.sandbox.regression.predstd import wls_prediction_std

np.random.seed(9876789)

#%% simulate data. np_array with x values and y = x^2


nsample=100

x = np.linspace(0, 10, 100)

X = np.column_stack((x, x**2))  #another column with a constant will be added to allow OLS
beta = np.array([1, 0.1, 10])
e = np.random.normal(size=nsample)


# add_constant adds a column with constant (where line intersects y). 
#Don´t understnad quite well y=np.dot...   but!
# X and y have same length (100), so every X row gives an y

X = sm.add_constant(X)
#print (X)
y = np.dot(X, beta) + e
#print (y)

# Model itself


model = sm.OLS(y, X)
results = model.fit()

ymodel=[]
xmodel=[]
for i in range(0,100):
    mcount=1.3875+i*(-.1356)+(i*10.0212)
    ymodel.append(mcount)
    xmodel.append(i)
    
#print (ymodel)

plt.scatter(xmodel,ymodel)
plt.show()

print(results.summary())

print ('\nParameters of interest !!!!!!')
print('Parameters: ', results.params)
print('R2: ', results.rsquared)


# In[72]:


#Pruebo con un modelo imaginario de una dimensión. Pulso (dependiente) y temperatura (independiente)
temp=np.array([36.2,37.0,37.5,37.7,38.0,38.5,39.2,40.2])
pulse=np.array([65,73,84,91,100,105,102,108])
plt.scatter(temp,pulse)
plt.show()
mymodel=sm.OLS(temp,pulse)
myresults=mymodel.fit()
print (myresults.summary())


# In[75]:


#Ahora añado variable presion arterial. Pulso (dependiente) y temperatura (independiente)
temp=np.array([36.2,37.0,37.5,37.7,38.0,38.5,39.2,40.2,36.5,37,37.2,37.3,37.9,38.7,39.1,40.1])
pulse=np.array([65,73,84,91,100,105,102,108,67,82,92,97,110,107,102,125])
MAP=np.array([75,78,81,75,77,91,83,78,62,64,59,55,68,71,54,51])

MX=np.column_stack((pulse,MAP))
MX=sm.add_constant(MX)
print (MX)
plt.scatter(pulse,temp)
plt.show()
mymodel=sm.OLS(temp,MX)
myresults=mymodel.fit()
print (myresults.summary())

