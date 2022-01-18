import numpy as np
import sys
sys.path.append('../..')
import navbench as nb
import matplotlib.pyplot as plt
import pandas as pd
import os
from tools import deg_to_rad

files= os.listdir(".")
data= []
for i in files:
    if i[:4] == '2021':
        data.append(i)

width= 1.5
height= -1.5
degree= 1
make_frames= False

for dname in data:
    db2= pd.read_csv(dname+'/database_entries_processed.csv')
    x= db2["X [mm]"].to_numpy(copy=True)
    y= db2["Y [mm]"].to_numpy(copy=True)
    dirname= dname+"/frames_deg_{}".format(degree)
    os.makedirs(dirname,exist_ok= True)
    xa= db2["fitted x deg {}".format(degree)].to_numpy(copy=True)
    ya= db2["fitted y deg {}".format(degree)].to_numpy(copy=True)
    gps_h= db2["gps_h deg {}".format(degree)].to_numpy(copy=True)
    ch= db2["corrected IMU heading [degrees]"].to_numpy(copy=True)
    gps_h_a= deg_to_rad(gps_h)
    ch_a= deg_to_rad(ch)
    fig, ax= plt.subplots(1,2)
    ax[0].plot(xa,ya, lw=0.2)
    ax[1].plot(xa,ya,lw=0.2)
    ax[1].scatter(xa,ya,s=0.1)
    ax[1].scatter(x,y,s=0.1)
    ax[1].quiver(x,y,np.cos(gps_h_a),np.sin(gps_h_a),units='dots',angles='xy',scale_units='xy',scale=25,color='r')
    ax[1].quiver(x,y,np.cos(ch_a),np.sin(ch_a),units='dots',angles='xy',scale_units='xy',scale=25,color='g')
    p= plt.Rectangle((xa[0],ya[0]),width,height,facecolor='none',edgecolor='k')
    #p.set_transform(ax[0].transAxes)
    ax[0].add_patch(p)
    ax[0].set_title(dname,fontsize= 8)
    if make_frames:
        for i in range(0,len(xa)):
            bx= xa[i]- width/2
            by= ya[i]- height/2
            p.set_xy((bx,by))
            ax[1].set_xlim(bx,bx+width)
            ax[1].set_ylim(by+height,by)
            j= i
            fig.savefig(dirname + "/" +"frame_{}".format(f'{j:05}')+".png",dpi=300)
    else:
        plt.show()
