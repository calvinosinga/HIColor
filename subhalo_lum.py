import numpy as np
import h5py as hp
import sys
########## INPUTS #################
grid = (2048,2048,2048)
CHUNK = sys.argv[1]
LUM_MIN, LUM_THRESH = -16, -20 #detection minimum and threshold for breaking into dim/bright bins, from Swanson
SNAPSHOT = 99
BOXSIZE = 75 #Mpc/h
def isred(gr, rband):#color definition as given in Swanson
    return gr> .9 - .03*(rband+23)
###################################
f = hp.File('fof_subhalo_tab_0'+str(SNAPSHOT)+'.'+str(CHUNK)+'.hdf5','r')
has_key = True
dim = np.zeros(grid)
bright = np.zeros(grid)
nondetection = np.zeros(grid)
magnitude = []
try:
    pos = f['Subhalo']['SubhaloCM']
    mass = f['Subhalo']['SubhaloMass']
    photo = f['Subhalo']['SubhaloStellarPhotometrics']
except KeyError:
    print('chunk was empty')
    has_key=False
if has_key:
    edges = np.linspace(0,BOXSIZE*1000, grid[0]) #definitions of bins
    bins = np.digitize(pos,edges)
    for j,b in enumerate(bins):
        rmag = photo[j][5]
        #gmag = photo[j][4]
        magnitude.append(rmag)
        if rmag<=LUM_THRESH:
            bright[b[0],b[1],b[2]] += mass[j]
        elif rmag<=LUM_MIN:
            dim[b[0],b[1],b[2]] += mass[j]
        else:
            nondetection[b[0],b[1],b[2]] += mass[j]
w = hp.File('lumin_'+str(SNAPSHOT)+'_'+str(CHUNK)+'.hdf5', 'w')
w.create_dataset("nondetection", data=nondetection)
w.create_dataset("bright", data=bright)
w.create_dataset("dim", data=dim)
w.create_dataset("luminosity", data=magnitude)
print('data size of magnitude')
print(str(sys.getsizeof(magnitude)))
print('data size of one of the fields:')
print(str(sys.getsizeof(bright)))