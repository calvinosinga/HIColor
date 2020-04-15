"""
A file that tests submitting multiple jobs at once. It also gathers data on the following:

1. Runtime
2. Size of the output
3. Size of the output compressed (tar.gz)
4. Disk space needed (sum of input + output)
5. RAM needed

I will test these on 2 example a) subhalo chunks, and 2 example b) particle chunks.

Then I will need to test those same 5 things on the second part of the run, which will be 
computing the power spectra from those fields.
"""


import numpy as np
import h5py as hp
from Pk_library import Pk
import os
grid = (2048,2048,2048)
BOXSIZE=75

FILENO = 447
edges = np.linspace(0,BOXSIZE*1000, grid[0]) #definitions of bins
for i in range(FILENO):
    has_file = True
    try:
        f = hp.File('fof_subhalo_tab_099.0'+unicode(i)+'.hdf5', 'r')
        print(unicode(i) + " was found in the home directory")
    except:
        has_file=False
    if has_file:
        total_mass = np.zeros(grid)
        has_key = True
        try:
            pos = f['Subhalo']['SubhaloCM']
            mass = f['Subhalo']['SubhaloMass']
        except:
            has_key = False
        if has_key:
            bins = np.digitize(pos,edges)
            for j,b in enumerate(bins):
                total_mass[b[0],b[1],b[2]]+=mass[j]
w = hp.File('fields.hdf5','w')
w.create_dataset("mass", data=total_mass)

w.close()
f.close()
w=hp.File('fields.hdf5','w')
mass = w['mass']
pk = Pk(mass, BOXSIZE, axis=0, MAS='CIC')
tpk = np.transpose([pk.k3D, pk.Pk[:,0]])
np.savetxt("pk.txt", tpk)