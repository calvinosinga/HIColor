import numpy as np
import h5py as hp
import sys
########## INPUTS #################
grid = (2048,2048,2048)
CHUNK = sys.argv[1]
LUM_MIN, LUM_THRESH = -16, -20 #detection minimum and threshold for breaking into dim/bright bins, from Swanson
FIELD = sys.argv[3]
SNAPSHOT = sys.argv[2]
BOXSIZE = 75 #Mpc/h
def isred(gr, rband):#color definition as given in Swanson
    return gr> .9 - .03*(rband+23)
###################################
f = hp.File('fof_subhalo_tab_0'+str(SNAPSHOT)+'.'+str(CHUNK)+'.hdf5','r')
if FIELD == 'color':
    has_key = True
    red = np.zeros(grid)
    blue = np.zeros(grid)
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
            color.append(gmag-rmag)
            if rmag<=LUM_MIN:
                # if rmag is significant enough to be observed by (Swanson et al), include it in blue/red
                if isred(gmag-rmag,rmag):
                    red[b[0],b[1],b[2]]+= mass[j]
                else:
                    blue[b[0],b[1],b[2]] += mass[j]

elif 
w = hp.File('subh_'+str(snapshot)+'_'+str(chunk)+'.hdf5', 'w')
w.create_dataset("red", data=red)
w.create_dataset("blue",data=blue)
w.create_dataset("nondetection", data=nondet)
w.create_dataset("bright", data=bright)
w.create_dataset("dim", data=dim)

                if rmag <= LUM_THRESH:
                    bright[b[0],b[1],b[2]] += mass[j]
                else:
                    dim[b[0],b[1],b[2]] += mass[j]
            else:
                nondet[b[0],b[1],b[2]] += mass[j]