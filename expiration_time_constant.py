# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

v0=450
tau_list=[0.5, 0.6, 0.7]
tau=0.7
tmax=3

t=np.linspace(0,tmax,100)
v=np.zeros((100,3))

for i in range(0,3):
    v[:,i] = v0* np.exp(-t /tau_list[i])

fig=plt.figure()
ax=fig.add_subplot(1,1,1)


ax.plot(t,v)
ax.hlines(0,xmin=0, xmax=tmax,ls=':',color='g')

ntau=tmax//tau +1
xt=np.arange(0,ntau,step=1,dtype='int')
ax.set_xticks(xt*tau)
ax.set_xticklabels(xt)



secax = ax.secondary_xaxis('top')  #look documentation
#secax.
secax.set_xlabel('Time in seconds')
ax.set_xlabel('n x tau')

plt.vlines(tau,ymin=-0.4,ymax=v0* np.exp(-tau/tau))
plt.hlines(v0* np.exp(-tau/tau),0,tau)
plt.show()


#%%
stacked=np.stack((t,v),axis=1)
plt.plot(stacked[:,0],stacked[:,1])  #and you get the same...



