import numpy as np
import sys
sys.path.append('../../..')
import navbench as nb
import matplotlib.pyplot as plt
import pandas as pd
import os
from tools import deg_to_rad
import matplotlib.image as img

files= os.listdir(".")
data= []
for i in files:
    if i.startswith('unwrapped_2021'):
        data.append(i)

width= 800
height= -800
degree= 1
make_frames= True

for dname in data:
    db2= pd.read_csv(dname+'/database_entries_processed.csv')
    x= db2["X [mm]"].to_numpy(copy=True)
    y= db2["Y [mm]"].to_numpy(copy=True)
    qual= db2["GPS quality"].to_numpy(copy=True)
    fnames= db2["Filename"]
    dirname= dname+"/frames_deg_{}".format(degree)
    os.makedirs(dirname,exist_ok= True)
    xa= db2["fitted x deg {}".format(degree)].to_numpy(copy=True)
    ya= db2["fitted y deg {}".format(degree)].to_numpy(copy=True)
    gps_h= db2["gps_h deg {}".format(degree)].to_numpy(copy=True)
    ch= db2["corrected IMU heading [degrees]"].to_numpy(copy=True)
    gps_h_a= deg_to_rad(gps_h)
    ch_a= deg_to_rad(ch)
    fig, ax= plt.subplot_mosaic([["overview","detail"],["view","view"]])
    ax["overview"].plot(xa,ya, lw=0.2)
    ax["detail"].plot(xa,ya,lw=0.2)
    ax["detail"].scatter(xa,ya,s=0.1)
    ax["detail"].scatter(x,y,s=0.1)
    ax["detail"].quiver(x,y,1000*np.cos(gps_h_a),1000*np.sin(gps_h_a),units='dots',angles='xy',scale_units='xy',scale=25,color='r')
    ax["detail"].quiver(x,y,1000*np.cos(ch_a),1000*np.sin(ch_a),units='dots',angles='xy',scale_units='xy',scale=25,color='g')
    p= plt.Rectangle((xa[0],ya[0]),width,height,facecolor='none',edgecolor='k')
    q= plt.Rectangle((xa[0],ya[0]),width/20,height/20)
    #p.set_transform(ax[0].transAxes)
    ax["overview"].add_patch(p)
    ax["detail"].add_patch(q)
    ax["overview"].set_title(dname,fontsize= 8)
    cmap=plt.get_cmap("RdYlGn")
    if make_frames:
        for i in range(0,len(xa)):
            bx= xa[i]- width/2
            by= ya[i]- height/2
            p.set_xy((bx,by))
            q.set_xy((bx,by))
            #print(qual[i])
            #print(cmap(qual[i]/5.0))
            q.set(facecolor=cmap((qual[i]-1)/4.0))
            ax["detail"].set_xlim(bx,bx+width)
            ax["detail"].set_ylim(by+height,by)
            j= i
            image= img.imread(dname+"/"+fnames[i])
            ax["view"].imshow(image) 
            fig.savefig(dirname + "/" +"frame_{}".format(f'{j:05}')+".png",dpi=300)
            ax["view"].clear()
    else:
        i=0
        image= img.imread(dname+"/"+fnames[i])
        ax["view"].imshow(image) 
        plt.show()
        exit(1)
