import numpy as np
import h5py as hp
import sys

first = sys.argv[1]
second = sys.argv[2]
third= sys.argv[3]
fourth = sys.argv[4]
fifth= sys.argv[5]
sixth = sys.argv[6]
seventh = sys.argv[7]
eighth= sys.argv[8]
process = sys.argv[9]
grid = (2048,2048,2048)

def get_mass(path):
    try:
        f=hp.File(path,'r')
    except IOError:
        print('files not found')
        return np.zeros(grid, dtype=np.float32)
    else:
        try:
            mass = f["mass"][:].astype(np.float32)
        except KeyError:
            print('mass field not found - creating substitute')
            return np.zeros(grid, dtype=np.float32)
        else:
            print('correctly found the mass')
            return mass

total = get_mass('subtotal1_ptl_'+first+'_'+second+'.hdf5')
print(sys.getsizeof(total))
sf = get_mass('subtotal1_ptl_'+third+'_'+fourth+'.hdf5')
total = np.add(total,sf,dtype=np.float32)
del sf
sf = get_mass('subtotal1_ptl_'+fifth+'_'+sixth+'.hdf5')
total = np.add(total,sf, dtype=np.float32)
del sf
sf = get_mass('subtotal1_ptl_'+seventh+'_'+eighth+'.hdf5')
total = np.add(total,sf,dtype=np.float32)
del sf
print('finished adding, new file:')
print(sys.getsizeof(total))
w = hp.File('subtotal2_ptl_'+process+'.hdf5','w')
w.create_dataset("mass",data=total)

