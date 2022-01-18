import numpy as np
import sys
sys.path.append('../..')
import navbench as nb
import matplotlib.pyplot as plt
import pandas as pd
import os

min_move= 0.5
pt_dist= 20

files= os.listdir(".")
data= []
for i in files:
    if i[:4] == '2021':
        data.append(i)

for dname in data:
    db2= pd.read_csv(dname+'/database_entries.csv')
    t= db2["Timestamp [ms]"].to_numpy(copy=True)
    x= db2["X [mm]"].to_numpy(copy=True)
    y= db2["Y [mm]"].to_numpy(copy=True)

    done= False
    i= 0
    while i < len(x)-(pt_dist+1) and not done:
        cmp= i+10
        while cmp < len(x)-1 and np.isnan(x[cmp]):
            cmp= cmp+1
        if not np.isnan(x[cmp]) and not np.isnan(x[i]): 
            if (np.sqrt((x[cmp]-x[i])*(x[cmp]-x[i])+(y[cmp]-y[i])*(y[cmp]-y[i])) > min_move):
                done= True
        i=i+1
        while i < len(x)-11 and np.isnan(x[i]):
            i=i+1
    start= i
    while i < len(x)-1 and (np.isnan(y[i]) or y[i] > 5638423):
        i=i+1

    stop= i
    print("Chopping: start= {}, stop= {}".format(start,stop))
    db2= db2[:][start:stop]
    db2.to_csv(dname+'/database_entries_processed.csv',index=False)
