import numpy as np
import h5py as hp
import sys

name = sys.argv[1]
savename = sys.argv[2]
f = hp.File(name,'r')
keys = list(f.keys())
dat = f[keys[0]][:]
mid = int(dat.shape[0]/2.0)
dat = dat[mid-30:mid+30,:,:]
dat = np.sum(dat,axis=0)
np.savetxt(savename,dat)