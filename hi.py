import numpy as np
import h5py as hp
import sys

filename = sys.argv[1]
idname = sys.argv[2]
run = sys.argv[3] #since making a bunch of fields isn't feasible, do one at a time
BOXSIZE=75.0 #Mpc/h
grid = (2048,2048,2048)
f = hp.File(filename, 'r')
g = hp.File(idname,'r')
keys = list(f.keys())
klist = []
pos = g['coordinates']
for k in keys:
    if 'm_hi' in k:
        klist.append(k)
k = klist[int(run)]
hi = f[k]
pos= np.divide(pos,1000) #converts to Mpc/h
edges = np.linspace(0,BOXSIZE,grid[0])
bins = np.digitize(pos,edges)
mass = np.zeros(grid)
for subh,b in enumerate(bins):
    if b[0]==2048:
        b[0]=2047
    if b[1]==2048:
        b[1]=2047
    if b[2]==2048:
        b[2]=2047
    mass[b[0],b[1],b[2]]+=hi[subh]
w = hp.File("benhi_"+run+".hdf5",'w')
w.create_dataset("hi",data=mass)