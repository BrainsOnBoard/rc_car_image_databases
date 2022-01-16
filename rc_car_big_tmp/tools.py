import numpy as np

def Euclid(x1, y1, x2, y2):
    return np.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def point_dist(px, py, x, y):
    d= Euclid(x, y, px, py)
    return np.min(d)

def trajectory_dist(x1, y1, x2, y2):
    d= 0
    for px, py in zip(x1,y1):
        d+= point_dist(px, py, x2, y2)
    for px, py in zip(x2,y2):
        d+= point_dist(px, py, x1, y1)
    return d

def rad_to_deg(a):
    return a/(2*np.pi)*360

def deg_to_rad(a):
    return a/360*(2*np.pi)

def unroll(a):
    la= np.copy(a)
    for i in range(len(la)-1):
        if abs(abs(la[i]-la[i+1])-360) < 25:
            # we are jumping across
            if la[i] > la[i+1]:
                la[i+1:]+= 360
            else:
                la[i+1:]-= 360
    return la
