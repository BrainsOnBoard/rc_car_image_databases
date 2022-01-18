import numpy as np
import sys
sys.path.append('../..')
import navbench as nb
import matplotlib.pyplot as plt
import pandas as pd
import os
from tools import unroll

files= os.listdir(".")
data= []
for i in files:
    if i[:4] == '2021':
        data.append(i)

sz= int(np.ceil(np.sqrt(len(data))))
fig, ax= plt.subplots(sz,sz,sharex= True, sharey= True)
py= 0
px= 0
degree= 1
for dname in data:
    db2= pd.read_csv(dname+'/database_entries_processed.csv')
    t= db2["Timestamp [ms]"].to_numpy(copy=True)
    h= db2["Heading [degrees]"].to_numpy(copy=True)
    gps_h= db2["gps_h deg {}".format(degree)].to_numpy(copy=True)
    uh= unroll(-h) # IMU recorded heading appears to be clockwise?!? - so taking the negative here
    gps_h= unroll(gps_h)
    dh = np.diff(uh)  
    idx= np.array(range(dh.shape[0]),dtype=int)[abs(dh) > 15]
    nh= uh.copy() 
    for i in idx:
        print(i)
        print(uh[i:i+2])
        df= uh[i+1]-uh[i]
        nh[i+1:]= (nh[i+1:]-df)
    mn= np.mean(gps_h)
    uh= uh-np.mean(uh)+mn
    nh= nh-np.mean(nh)+mn
    db2["corrected IMU heading [degrees]"]= nb.normalise180(nh)
    ax[py,px].plot(t,uh,lw=1)
    ax[py,px].plot(t,nh,lw=1)
    ax[py,px].plot(t,gps_h,lw=1)
    ax[py,px].set_title(dname,fontsize=8)
    px+= 1
    if px >= sz:
        py+= 1
        px = 0
    db2.to_csv(dname+'/database_entries_processed.csv',index=False)
plt.savefig("figures/corrected_heading",dpi=300)
plt.show()
