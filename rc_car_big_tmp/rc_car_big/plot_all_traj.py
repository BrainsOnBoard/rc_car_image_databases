import numpy as np
import sys
sys.path.append('../..')
import navbench as nb
import matplotlib.pyplot as plt
import pandas as pd
import os
from tools import trajectory_dist

files= os.listdir(".")
data= []
for i in files:
    if i[:4] == '2021':
        data.append(i)

plt.figure()

for dname in data:
    db2= pd.read_csv(dname+'/database_entries.csv')    
    x= db2["X [mm]"].to_numpy(copy=True)
    y= db2["Y [mm]"].to_numpy(copy=True)
    plt.scatter(x,y,s=0.1)
plt.savefig("figures/raw_trajectories_onepanel.png", dpi= 600)
    
plt.figure()
for dname in data:
    db2= pd.read_csv(dname+'/database_entries.csv')    
    x= db2["X [mm]"].to_numpy(copy=True)
    y= db2["Y [mm]"].to_numpy(copy=True)
    plt.scatter(x-x[0],y-y[0],s=0.1)
plt.savefig("figures/raw_trajectories_samex0y0_onepanel.png", dpi= 600)

py= 0
px= 0
sz= int(np.ceil(np.sqrt(len(data))))
fig, ax= plt.subplots(sz,sz,sharex= True, sharey= True)
for dname in data:
    db2= pd.read_csv(dname+'/database_entries.csv')    
    x= db2["X [mm]"].to_numpy(copy=True)
    y= db2["Y [mm]"].to_numpy(copy=True)
    ax[py,px].scatter(x,y,s=0.1)
    ax[py,px].set_title(dname,fontsize=8)
    px+= 1
    if px >= sz:
        py+= 1
        px = 0

plt.savefig("figures/raw_trajectories_manypanel.png", dpi= 600)

plt.figure()
for dname in data:
    db2= pd.read_csv(dname+'/database_entries_processed.csv')    
    x= db2["X [mm]"].to_numpy(copy=True)
    y= db2["Y [mm]"].to_numpy(copy=True)
    plt.scatter(x,y,s=0.1)
plt.savefig("figures/cut_trajectories_onepanel.png", dpi= 600)

plt.figure()
for dname in data:
    db2= pd.read_csv(dname+'/database_entries_processed.csv')    
    x= db2["X [mm]"].to_numpy(copy=True)
    x= x-x[0]
    y= db2["Y [mm]"].to_numpy(copy=True)
    y= y-y[0]
    plt.scatter(x,y,s=0.1)
plt.savefig("figures/cut_trajectories_samex0y0_onepanel.png", dpi= 600)

plt.figure()
for dname in data:
    db2= pd.read_csv(dname+'/database_entries_processed.csv')    
    xa= db2["fitted x deg 1"].to_numpy(copy=True)
    ya= db2["fitted y deg 1"].to_numpy(copy=True)
    plt.scatter(xa,ya,s=0.1)
plt.savefig("figures/fitted_trajectories_onepanel.png", dpi= 600)

plt.figure()
for dname in data:
    db2= pd.read_csv(dname+'/database_entries_processed.csv')    
    xa= db2["fitted x deg 1"].to_numpy(copy=True)
    xa= xa - xa[0]
    ya= db2["fitted y deg 1"].to_numpy(copy=True)
    ya= ya - ya[0]
    plt.scatter(xa,ya,s=0.1)
plt.savefig("figures/fitted_trajectories_samex0y0_onepanel.png", dpi= 600)

plt.show()


