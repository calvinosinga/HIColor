"""
todo
split into more parts -> field by field basis
handle missing files
handle missing keys -> happens on jupyterlab version as well
figure out how to see how that propagates when combining the fields
removing dim/bright runs, just color.
"""
import numpy as np
import h5py as hp
import sys
########## INPUTS #################
grid = (2048,2048,2048)
CHUNK = sys.argv[1]
RUN = sys.argv[2]
LUM_MIN = -16 #detection minimum from Swanson
SNAPSHOT = sys.argv[3]
COLORDEF = sys.argv[4]
BOXSIZE = 75000 #kpc/h
###################################

def isred(gr, rband):#color definition as given in Swanson
    return gr> .9 - .03*(rband+23)
    

flags = np.zeros(3, dtype=np.int32)
err = 'there was no error'
try:
    f = hp.File('fof_subhalo_tab_0'+str(SNAPSHOT)+'.'+str(CHUNK)+'.hdf5','r')
except IOError:
    err='failed to open file for ' + str(CHUNK)
    print(err)
    flags[0]=1
else:
    has_key = True
    field = np.zeros(grid, dtype=np.float32)
    try:
        pos = f['Subhalo']['SubhaloCM'] #kpc/h
        mass = f['Subhalo']['SubhaloMass']
        photo = f['Subhalo']['SubhaloStellarPhotometrics']
    except KeyError:
        err='chunk '+str(CHUNK)+ '\'s subhalo data was empty'
        flags[1]=1
        has_key=False
    if has_key:
        edges = np.linspace(0,BOXSIZE, grid[0]-1) #definitions of bins
        bins = np.digitize(pos,edges)
        for j,b in enumerate(bins):
            rmag = photo[j][5]
            gmag = photo[j][4]
            if RUN=='red':
                if rmag<=LUM_MIN and isred(gmag-rmag,rmag):
                    field[b[0],b[1],b[2]]+= mass[j]
            elif RUN=='blue':
                if rmag<=LUM_MIN and not isred(gmag-rmag,rmag):
                    field[b[0],b[1],b[2]]+= mass[j]
            elif RUN=='nondetection':
                if not rmag<=LUM_MIN:
                    field[b[0],b[1],b[2]]+= mass[j]     
    w = hp.File(RUN+str(CHUNK)+'_'+str(COLORDEF)+'.hdf5', 'w')
    w.create_dataset(RUN,data=field)   
    w.create_dataset('flags',data=flags)
    print(flags)
    print(err)
    