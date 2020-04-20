import h5py as hp
import numpy as np
import sys
from Pk_library import Pk


f = hp.File('final_ptl_0.hdf5', 'r')
field = f["mass"][:]
BOXSIZE = 75.0
pk = Pk(field,BOXSIZE, axis = 0, MAS='CIC')
tpk = np.transpose([pk.k3D, pk.Pk[:,0]])
np.savetxt("mass_pk.txt",tpk)