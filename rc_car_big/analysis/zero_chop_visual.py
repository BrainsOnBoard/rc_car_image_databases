import numpy as np
import sys
sys.path.append('../../..')
import navbench as nb
import matplotlib.pyplot as plt
import pandas as pd
import os

min_move= 0.5
pt_dist= 20

files= os.listdir(".")
data= []
for i in files:
    if i.startswith('unwrapped_2021'):
        data.append(i)

manual_cut= {
    "unwrapped_20210303_150314": [(131, 11304)],
    "unwrapped_20210303_153749": [(125, 10379)],
    "unwrapped_20210308_122125": [(151, 9700)],
    "unwrapped_20210308_124836": [(148, 4209),(4338, 5336),(5367,8885),(8906,9044),(9074,10333)],
    "unwrapped_20210322_155544": [(383, 9851)],
    "unwrapped_20210322_170743": [(117,7479),(7608,9310)],
    "unwrapped_20210414_151116": [(127,9157)],
    "unwrapped_20210420_135721": [(339,6294),(6326,6759),(6781,7138),(7163,7174),(7209,7834),(7853,8256),(8280,8371),(8389,10026)],
    "unwrapped_20210420_141940": [(86,9410)],
    "unwrapped_20210422_134815": [(135,10000)], # endpoint not real here as it doesn't go to the tree!!!
    "unwrapped_20210426_162152": [(50,3673)],
    "unwrapped_20210426_164219": [(69,3129)], # this one stops prematurely
    "unwrapped_20210511_151514": [(199,1377),(1414,3635),(3925,10357)],
    "unwrapped_20210511_153933": [(112, 10099)],
    "unwrapped_20210525_141844": [(154,8764)]
    }
    
    

plt.figure()      
for dname in data:
    db= pd.read_csv(dname+'/database_entries.csv',sep=r',',skipinitialspace=True)
    x= db["X [mm]"].to_numpy(copy=True)
    y= db["Y [mm]"].to_numpy(copy=True)
    i= 0
    while i < len(x)-1 and (np.isnan(y[i]) or y[i] > 5638423000):
        i=i+1
    fstp= i
    segments= manual_cut[dname]
    dt= np.mean(np.diff(db["Timestamp [ms]"]))
    print("dt= {}".format(dt))
    if len(segments) == 1:
        db2= db[segments[0][0]:fstp]
    else:
        db2= db[segments[0][0]:segments[0][1]]
        for strt, stp in segments[1:]:
            if stp < fstp:
                idx= len(db2)
                db2= db2.append(db[strt:stp],ignore_index = True)
                t= db2["Timestamp [ms]"][idx-1]
                t2= db2["Timestamp [ms]"][idx]
                db2.loc[idx:,"Timestamp [ms]"] -= (t2-t)-dt
            else:
                if strt < fstp:
                    idx= len(db2)
                    db2= db2.append(db[strt:fstp],ignore_index = True)
                    t= db2["Timestamp [ms]"][idx-1]
                    t2= db2["Timestamp [ms]"][idx]
                    db2.loc[idx:,"Timestamp [ms]"] -= (t2-t)-dt
    xn= db2["X [mm]"].to_numpy(copy=True)
    yn= db2["Y [mm]"].to_numpy(copy=True)
    #plt.scatter(xn,yn,s=0.1)
    plt.plot(db2.loc[:,"Timestamp [ms]"])
    db2.to_csv(dname+'/database_entries_processed.csv',index=False)
plt.show()
