import numpy as np
import h5py as hp
import sys

first = int(sys.argv[1])
second = int(sys.argv[2])
process = str(first)
first = [str(first*2),str((first*2+1))]
second = [str(second*2),str((second*2+1))]
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

total = get_mass('subtotal1_ptl_99_'+first[0]+'_'+first[1]+'.hdf5')
print(sys.getsizeof(total))
sf = get_mass('subtotal1_ptl_99_'+second[0]+'_'+second[1]+'.hdf5')
print(sys.getsizeof(sf))
total = np.add(total,sf,dtype=np.float32)
print('finished adding, new file:')
print(sys.getsizeof(total))
w = hp.File('subtotal2_ptl_'+process+'.hdf5','w')
w.create_dataset("mass",data=total)
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
