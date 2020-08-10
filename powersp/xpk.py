import h5py as hp
import numpy as np
import sys
from Pk_library import XPk
print('started python script')
filename = sys.argv[1]
fieldname = sys.argv[2]
xfilename = sys.argv[3]
xfieldname = sys.argv[4]
savepk1 = sys.argv[5]
savepk2 = sys.argv[6]
savexpk = sys.argv[7]
BOXSIZE = 75000.0 #kpc/h
f = hp.File(filename,'r')
g = hp.File(xfilename,'r')
print('loaded files')
gkeys = list(g.keys())
fkeys = list(f.keys())

if 'flags' in gkeys:
    xflags = g['flags']
else:
    xflags = 'not applicable'

if 'flags' in fkeys:
    flags = f['flags']
else:
    flags = 'not applicable'


field = f[fieldname][:]
xfield = g[xfieldname][:]
print('loaded datasets')
print(type(xfield[0,0,0]))
print(flags)
print(xflags)
print(field.shape)
print(xfield.shape)
field = np.divide(field,BOXSIZE**3,dtype=np.float32) #converts to a density
avg = np.mean(field)
field = np.divide(field,avg,dtype=np.float32); field = np.add(field,-1,dtype=np.float32)
print('converted first field to an overdensity')
xfield = np.divide(xfield,BOXSIZE**3,dtype=np.float32) #converts to a density
avg = np.mean(xfield)
xfield = np.divide(xfield,avg,dtype=np.float32); xfield = np.add(xfield,-1,dtype=np.float32)
print('converted second field to an overdensity')
res = XPk([field,xfield],BOXSIZE, axis = 0, MAS=['NGP','NGP'])
pk1 = np.transpose([res.k3D, res.Pk[:,0,0]])
pk2 = np.transpose([res.k3D, res.Pk[:,0,1]])
xpk = np.transpose([res.k3D, res.XPk[:,0,0]])
np.savetxt(savepk1, pk1)
np.savetxt(savepk2, pk2)
np.savetxt(savexpk, xpk)
