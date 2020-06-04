import numpy as np
import h5py as hp
import sys

filename = sys.argv[1]
ids = sys.argv[2]
f = hp.File(filename, 'r')
keys = list(f.keys())
klist = []
for k in keys:
    if 'm_hi' in k:
        klist.append(k)