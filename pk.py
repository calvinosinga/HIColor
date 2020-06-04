import h5py as hp
import numpy as np
import sys
from Pk_library import Pk

filename = sys.argv[1]
fieldname = sys.argv[2]
savename = sys.argv[3]
BOXSIZE = 75.0 #Mpc/h
f = hp.File(filename,'r')
field = f[fieldname][:]
flags = f['flags']
print(flags)
field = np.divide(field,BOXSIZE**3) #converts to a density
avg = np.mean(field)
field = np.divide(field,avg); field = np.add(field,-1)
pk = Pk(field,BOXSIZE, axis = 0, MAS='NGP') #need to change the mass assignment scheme -> digital?
tpk = np.transpose([pk.k3D, pk.Pk[:,0]])
np.savetxt(savename,tpk)




