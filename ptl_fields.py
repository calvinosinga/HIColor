"""
Create the total mass field using the particle snapshots
"""
import numpy as np
import h5py as hp
import sys
########## INPUTS #################
grid = (2048,2048,2048)
chunk = sys.argv[1]
snapshot = 99
BOXSIZE = 75 #Mpc/h
###################################

f= hp.File("snap_0"+str(snapshot)+'.'+str(chunk)+".hdf5",'r')
keys = list(f.keys())
edges = np.linspace(0,BOXSIZE*1000, grid[0])
total = np.zeros(grid)
for k in keys:
    if "Part" in k and "3" not in k:
        mass = f[k]['Masses']
        pos = f[k]['Coordinates']
        bins = np.digitize(pos,edges)
        for ptl,b in enumerate(bins):
            total[b[0],b[1],b[2]]+=mass[ptl]
w = hp.File('ptl_'+str(snapshot)+'_'+str(chunk)+'.hdf5', 'w')
w.create_dataset("mass", data=total)





