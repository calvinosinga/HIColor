import numpy as np
import h5py as hp
import sys
print("started python file")
name = sys.argv[1]
f = hp.File(name,'r')
keys = list(f.keys())
dat = f[keys[0]]
print(dat.shape)
mid = int(dat.shape[0]/2.0)
dat = dat[mid-30:mid+30,:,:]
dat = np.sum(dat,axis=0)
print(np.mean(dat))
w = hp.File(name+'_dist.hdf5','w')
w.create_dataset('slice',data=dat)
print("finished python file")