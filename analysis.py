import h5py as hp
import numpy as np
import sys
from Pk_library import Pk


f = hp.File('final_ptl_0.hdf5', 'r')
field = f["mass"][:]*1e10 #converting to solar masses/h
BOXSIZE = 75.0 #Mpc/h
field=np.divide(field,BOXSIZE**3)# converting to a density
avg = np.mean(field)
field= np.divide(field,avg); field = np.add(field,-1)
pk = Pk(field,BOXSIZE, axis = 0, MAS='CIC')
tpk = np.transpose([pk.k3D, pk.Pk[:,0]])
np.savetxt("mass_pk.txt",tpk)


