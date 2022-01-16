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

dists= []
odists= []
# measure pairwise distances between trajectories
for i in range(len(data)-1):
    dname1= data[i][:]
    db1= pd.read_csv(dname1+'/database_entries_processed.csv')        
    for j in range(i+1,len(data)):
        dname2= data[j][:]
        db2= pd.read_csv(dname2+'/database_entries_processed.csv')    
        x1= db1["fitted x deg 1"].to_numpy(copy=True)
        y1= db1["fitted y deg 1"].to_numpy(copy=True)
        x2= db2["fitted x deg 1"].to_numpy(copy=True)
        y2= db2["fitted y deg 1"].to_numpy(copy=True)
        dists.append(trajectory_dist(x1, y1, x2, y2))
        odists.append(trajectory_dist(x1-x1[0], y1-y1[0], x2-x2[0], y2-y2[0]))
        print("raw: {}, same start: {}".format(dists[-1],odists[-1]))

print(np.mean(dists))
print(np.mean(odists))
