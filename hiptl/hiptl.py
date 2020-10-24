import numpy as np
import h5py as hp
BASE = '/lustre/diemer/illustris/hih2/'
HOME = '/lustre/cosinga/'
BOXSIZE = 75000 #kpc/h
grid = (2048,2048,2048)
fileno = 448
field = np.zeros(grid, dtype=np.float32)
edges = np.linspace(0,75,grid[0]-1)
for i in range(fileno):
    hih2file = hp.File(BASE + "hih2_particles_099."+str(i)+".hdf5", "r")
    ptlfile = hp.File(**PATH_TO_FILE**)
    mass = ptlfile['PartType0']['Masses'][:]
    pos = ptlfile['PartType']['CenterOfMass'][:]
    f_neut_h = hih2file['PartType0']['f_neutral_h'] # check key
    
    masshi = (1-**MODEL_FRACTION**)*f_neut_h*mass
    del mass
    bins = np.digitize(pos, edges)
    for ptl,b in enumerate(bins):
        field[b[0],b[1],b[2]] += masshi[ptl]

# save field
    
