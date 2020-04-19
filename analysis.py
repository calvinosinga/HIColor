import h5py as hp
import numpy as np
import sys
from Pk_library import Pk

fname = sys.argv[1]
keyname = sys.argv[2]
f = hp.File(fname, 'r')
field = f[keyname][:]
BOXSIZE = 75.0
pk = Pk(field,BOXSIZE, axis = 0, MAS='CIC')
tpk = np.transpose([pk.k3D, pk.Pk[:,0]])
np.savetxt(keyname+"_pk.txt",tpk)