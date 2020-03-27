import numpy as np
import h5py as hp
import sys
########## INPUTS #################
grid = (2048,2048,2048)
CHUNK = sys.argv[1]
LUM_MIN, LUM_THRESH = -16, -20 #detection minimum and threshold for breaking into dim/bright bins, from Swanson
SNAPSHOT = 99
COLOR = sys.argv[2] #splitting blue/red/color so RAM/disk demand is smaller -> waiting on queue is taking longer than
#actually running the code otherwise
BOXSIZE = 75 #Mpc/h
def isred(gr, rband):#color definition as given in Swanson
    return gr> .9 - .03*(rband+23)
###################################
f = hp.File('fof_subhalo_tab_0'+str(SNAPSHOT)+'.'+str(CHUNK)+'.hdf5','r')

has_key = True
col = np.zeros(grid)
color = []
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
        gmag = photo[j][4]
        if COLOR=='color':
            color.append(gmag-rmag)
        else:
            if rmag<=LUM_MIN:
                # if rmag is significant enough to be observed by (Swanson et al), include it in blue/red
                if isred(gmag-rmag,rmag) and COLOR=='red':
                    col[b[0],b[1],b[2]]+= mass[j]
                elif not isred(gmag-rmag,rmag) and COLOR=='blue':
                    col[b[0],b[1],b[2]] += mass[j]
        
w = hp.File('color_'+str(SNAPSHOT)+'_'+str(CHUNK)+'_'+str(COLOR)+'.hdf5', 'w')
if COLOR == 'color':
    w.create_dataset('color',data=color)
else:
    w.create_dataset(COLOR, data=col)