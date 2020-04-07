import numpy as np
import h5py as hp
import sys
first = sys.argv[1]
second = sys.argv[2]
grid = (2048,2048,2048)

def get_mass(path):
    try:
        f=hp.File(path,'r')
        print()
    except IOError:
        print('files not found')
        return np.zeros(grid)
    else:
        try:
            mass = f["mass"]
        except KeyError:
            print('mass field not found - creating substitute')
            return np.zeros(grid)
        else:
            return mass
            

mf = get_mass('ptl_99_'+str(first)+'.hdf5')
sf = get_mass('ptl_99_'+str(second)+'.hdf5')
mf = np.add(mf,sf)
w = hp.File('subtotal1_ptl_'+str(first)+'_'+str(second)+'.hdf5','w')
w.create_dataset("mass",data=mf)
# try:
#     f = hp.File('ptl_99_'+str(first)+'.hdf5', 'r')
#     s = hp.File('ptl_99_'+str(second)+'.hdf5', 'r')
# except IOError:
#     print('files not found')
# else:
#     try:
#         mf = f['mass']
#         sf = f['mass']
#     except KeyError:
#         print('mass field not found - creating substitute')
#     else:
#         total = np.add(mf,sf)
#         w = hp.File('subtotal1_ptl_'+str(first)+'_'+str(second)+'.hdf5','w')
#         w.create_dataset("mass",data=total)
