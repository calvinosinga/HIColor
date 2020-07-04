import numpy as np
import h5py as hp
import sys

filename = sys.argv[1]
BOXSIZE=75.0 #Mpc/h
f = hp.File(filename,'r')
keys = list(f.keys())

for k in keys:
    w = hp.File(k+"_paco.hdf5",'w')
    dat = f[k][:]
    dat += 1; dat = dat*BOXSIZE**3
    w.create_dataset(k,data=dat)
