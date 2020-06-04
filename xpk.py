import h5py as hp
import numpy as np
import sys
from Pk_library import XPk

filename = sys.argv[1]
fieldname = sys.argv[2]
xfilename = sys.argv[3]
xfieldname = sys.argv[4]
savepk1 = sys.argv[5]
savepk2 = sys.argv[6]
savexpk = sys.argv[7]
BOXSIZE = 75.0 #Mpc/h
f = hp.File(filename,'r')
g = hp.File(xfilename,'r')
field = f[fieldname][:]
flags = f['flags']

xfield = f[xfieldname][:]
if 'flags' in list(g.keys()):
    xflags = f['flags']
else:
    xflags = 'not applicable'
print(flags)
print(xflags)
field = np.divide(field,BOXSIZE**3) #converts to a density
avg = np.mean(field)
field = np.divide(field,avg); field = np.add(field,-1)
xfield = np.divide(xfield,BOXSIZE**3) #converts to a density
avg = np.mean(xfield)
xfield = np.divide(xfield,avg); xfield = np.add(xfield,-1)
res = XPk([field,xfield],BOXSIZE, axis = 0, MAS=['NGP','NGP']) #need to change the mass assignment scheme -> digital?
pk1 = np.transpose([res.k3D, res.Pk[:,0,0]])
pk2 = np.transpose([res.k3D, res.Pk[:,0,1]])
xpk = np.transpose([res.k3D, res.XPk[:,0,0]])
np.savetxt(savepk1, pk1)
np.savetxt(savepk2, pk2)
np.savetxt(savexpk, xpk)