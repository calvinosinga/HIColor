"""
Combine.py takes any four files (their filenames are given through command line) and combines
their respective fields. The run arg determines whether to use the subhalo or particle implementation.

this as compared to combine_fields.py which is currently just for ptl fields


todo

create code that finds the needed filename based on cml arguments
handle empty files
handle IOError

"""

import numpy as np
import h5py as hp
import sys
run = sys.argv[1]
first = sys.argv[2]
second = sys.argv[3]
third = sys.argv[4]
fourth = sys.argv[5]
output = sys.argv[6]
#the run arg will determine whether or not we want the ptl implementation or the subhalo implementation
#first, second, third, fourth are the filenames for the fields that we want to combine.
#output will give the output filename.
grid = (2048,2048,2048)

def get_mass(key,path):
    try:
        f=hp.File(path,'r')
        print()
    except IOError:
        print('files not found')
        return np.zeros(grid)
    else:
        try:
            mass = f[key]
        except KeyError:
            print(key+' field not found - creating substitute')
            return np.zeros(grid)
        else:
            return mass
def get_field(key,path):
    try:
        f=hp.File(path,'r')
        print()
    except IOError:
        print('files not found')
        return []
    else:
        try:
            field = f[key]
        except KeyError:
            print(key+' field not found - creating substitute')
            return []
        else:
            return field
if run == 'ptl':
    total = get_mass("mass",first)
    m = get_mass("mass",second)
    total=np.add(total,m)
    m = get_mass("mass",third)
    total=np.add(total,m)
    m = get_mass("mass",fourth)
    total = np.add(total,m)
    w = hp.File(output,'w')
    w.create_dataset("mass",data=total)

if run == 'subhalo':
    keys = ['red','blue','dim','bright','nondetection']
    ls = ['magnitude','color']
    w.hp.File(output, 'w')
    for k in keys:
        total = get_mass(k,first)
        m = get_mass(k,second)
        total = np.add(total,m)
        m = get_mass(k,third)
        total = np.add(total, m)
        m = get_mass(k,fourth)
        total = np.add(total,m)
        w.create_dataset(k,data=total)
    for l in ls:
        total = get_field(l,first)
        m = get_field(l,second)
        total.extend(m)
        m = get_field(l,third)
        total.extend(m)
        m=get_field(l,fourth)
        total.extend(m)
        w.create_dataset(l,data=total)
    

        
