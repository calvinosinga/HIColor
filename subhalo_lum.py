import numpy as np
import h5py as hp
import sys
########## INPUTS #################
grid = (2048,2048,2048)
CHUNK = sys.argv[1]
FIELD = sys.argv[2]
LUM_MIN, LUM_THRESH = -16, -20 #detection minimum and threshold for breaking into dim/bright bins, from Swanson
SNAPSHOT = 99
BOXSIZE = 75 #Mpc/h
def isred(gr, rband):#color definition as given in Swanson
    return gr> .9 - .03*(rband+23)
###################################
f = hp.File('fof_subhalo_tab_0'+str(SNAPSHOT)+'.'+str(CHUNK)+'.hdf5','r')
has_key = True
if FIELD=='magnitude':
    dat = []
else:
    dat = np.zeros(grid)

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
        if FIELD == 'magnitude':
            dat.append(rmag)
        if rmag<=LUM_THRESH and FIELD == 'bright':
            dat[b[0],b[1],b[2]] += mass[j]
        elif rmag<=LUM_MIN and FIELD == 'dim':
            dat[b[0],b[1],b[2]] += mass[j]
        elif FIELD == 'nondetection':
            dat[b[0],b[1],b[2]] += mass[j]
        else:
            print('incorrect field argument - should be bright, dim, nondetection, or magnitude')
w = hp.File('lumin_'+str(SNAPSHOT)+'_'+str(CHUNK)+'_' +FIELD+'.hdf5', 'w')
w.create_dataset(FIELD, data=dat)

