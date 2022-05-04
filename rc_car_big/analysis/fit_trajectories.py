import numpy as np
import sys
sys.path.append('../..')
import navbench as nb
import matplotlib.pyplot as plt
import pandas as pd
import os
from tools import rad_to_deg

# function to fit with
fit_fun= np.polynomial.polynomial.Polynomial.fit

def fit_trajectory(t,x,y,z,num_p,degree):
    N= x.shape[0]
    xa= np.zeros(x.shape)
    nx= np.zeros(x.shape)
    ya= np.zeros(y.shape)
    ny= np.zeros(x.shape)
    za= np.zeros(z.shape)
    nz= np.zeros(x.shape)
    ecntr= 0
    for i in range(0,N-num_p+1):
        try:
            lfit= fit_fun(t[i:i+num_p][np.logical_not(np.isnan(x[i:i+num_p]))],x[i:i+num_p][np.logical_not(np.isnan(x[i:i+num_p]))],degree)
        except:
            print("t={}: exception during fitting x".format(t[i]))
            ecntr+= 1
        else:
            xa[i:i+num_p]+= lfit(t[i:i+num_p])
            nx[i:i+num_p]+= np.ones(num_p)
        try:
            lfit= fit_fun(t[i:i+num_p][np.logical_not(np.isnan(y[i:i+num_p]))],y[i:i+num_p][np.logical_not(np.isnan(y[i:i+num_p]))],degree)
        except:
            print("t={}: exception during fitting y".format(t[i]))
            ecntr+= 1
        else:
            ya[i:i+num_p]+= lfit(t[i:i+num_p])
            ny[i:i+num_p]+= np.ones(num_p)
        try:
            lfit= fit_fun(t[i:i+num_p][np.logical_not(np.isnan(z[i:i+num_p]))],z[i:i+num_p][np.logical_not(np.isnan(z[i:i+num_p]))],degree)
        except:
            print("t={}: exception during fitting z".format(t[i]))
            ecntr+= 1
        else:           
            za[i:i+num_p]+= lfit(t[i:i+num_p])
            nz[i:i+num_p]+= np.ones(num_p)
    xa/= nx
    ya/= ny
    za/= nz
    print("{} exceptions".format(ecntr))
    return (xa, ya, za)

def heading(dx,dy):
    res=np.empty(dx.shape)
    idx= dx > 0
    res[idx]= np.arctan(dy[idx]/dx[idx])
    idx= np.logical_and(dx < 0, dy > 0)
    res[idx]= np.pi-np.arctan(-dy[idx]/dx[idx])
    idx= np.logical_and(dx < 0, dy < 0)
    res[idx]= -np.pi+np.arctan(dy[idx]/dx[idx])
    idx= np.logical_and(dx == 0, dy < 0)
    res[idx]= -np.pi/2
    np.logical_and(dx == 0, dy > 0)
    res[idx]= np.pi/2
    return res

files= os.listdir(".")
data= []
for i in files:
    if i[:4] == '2021':
        data.append(i)

degree= 1
num_p= 75
        
for dname in data:
    db2= pd.read_csv(dname+'/database_entries_processed.csv')
    t= db2["Timestamp [ms]"].to_numpy(copy=True)
    x= db2["X [mm]"].to_numpy(copy=True)
    y= db2["Y [mm]"].to_numpy(copy=True)
    z= db2["Z [mm]"].to_numpy(copy=True)
    xa, ya, za= fit_trajectory(t,x,y,z,num_p,degree)
    dx= np.diff(xa)
    dy= np.diff(ya)
    gps_h= heading(dx,dy)
    gps_h= rad_to_deg(gps_h)
    gps_h= nb.normalise180(gps_h)
    gps_h= np.hstack((gps_h,[gps_h[-1]]))
    db2["fitted x deg {}".format(degree)]= xa
    db2["fitted y deg {}".format(degree)]= ya
    db2["fitted z deg {}".format(degree)]= za
    db2["gps_h deg {}".format(degree)]= gps_h
    db2.to_csv(dname+'/database_entries_processed.csv',index=False)
