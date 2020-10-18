import numpy as np
import matplotlib.pyplot as plt
import h5py as hp
print("completed imports")
base = '/lustre/diemer/illustris/hih2/'
f = hp.File(base+"hih2_particles_099.0.hdf5")
print(list(f.keys()))

print("finished opening file")
