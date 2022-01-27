import numpy as np
import sys
sys.path.append('../../..')
import navbench as nb
import matplotlib.pyplot as plt
import pandas as pd
import os
from tools import deg_to_rad

def mdist(x1, y1, x2, y2):
    return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)

files= os.listdir(".")
data= []
for i in files:
    if i.startswith('unwrapped_2021'):
        data.append(i)

degree= 1
py= 0
px= 0
start= True
dl= 10
sz= int(np.ceil(np.sqrt(len(data))))
fig, ax= plt.subplots(sz,sz,sharex= True, sharey= True,figsize=(16, 12))
fig2= plt.figure()
for dname in data:
    db2= pd.read_csv(dname+'/database_entries_processed.csv')    
    xa= db2["fitted x deg 1"].to_numpy(copy=True)
    ya= db2["fitted y deg 1"].to_numpy(copy=True)
    ch= db2["corrected IMU heading [degrees]"].to_numpy(copy=True)
    ch_a= deg_to_rad(ch)
    dx= np.diff(xa)
    dy= np.diff(ya)
    dist= np.sqrt(dx*dx+dy*dy)
    xi= np.empty(xa.shape)
    xi[0]= xa[0]
    yi= np.empty(ya.shape)
    yi[0]= ya[0]
    for i in range(1,len(xa)):
        l= dl
        nxi0= xi[i-1]+np.cos(ch_a[i-1])*l
        nyi0= yi[i-1]+np.sin(ch_a[i-1])*l
        dst0= mdist(xa[i], ya[i], nxi0, nyi0)
        while True:
            l+= dl
            nxi1= xi[i-1]+np.cos(ch_a[i-1])*l
            nyi1= yi[i-1]+np.sin(ch_a[i-1])*l
            dst1= mdist(xa[i], ya[i], nxi1, nyi1)
            if (dst1 > dst0):
                break
            dst0= dst1
        l-= dl    
        xi[i]= xi[i-1]+np.cos(ch_a[i-1])*l
        yi[i]= yi[i-1]+np.sin(ch_a[i-1])*l
    ax[py,px].scatter(xa,ya,s=0.1)
    ax[py,px].scatter(xi,yi,s=0.1)
    ax[py,px].set_title(dname,fontsize=8)
    if start:
        xm= np.mean(xi)
        ym= np.mean(yi)
        start= False
    else:
        xi= xi-np.mean(xi)+xm
        yi= yi-np.mean(yi)+ym
    fig2.gca().scatter(xi,yi,s=0.1)
    px+= 1
    if px >= sz:
        py+= 1
        px = 0

fig.savefig("figures/reconstructed_all.png", dpi= 600)
fig2.savefig("figures/reconstructed_compared.png", dpi= 600)
plt.show()
