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
result = sys.argv[6]
#the run arg will determine whether or not we want the field, or color/mag implementation
#first, second, third, fourth are the filenames for the fields that we want to combine.
#result will give the result filename.
grid = (2048,2048,2048)

def get_mass(key,path):
    try:
        f=hp.File(path,'r')
    except IOError:
        print('files not found')
        return np.zeros(grid, dtype=np.float32), np.zeros(3)
    else:
        try:
            mass = f[key]
            flags = f['flags']
        except KeyError:
            print(key+' field not found - creating substitute')
            return np.zeros(grid, dtype=np.float32), np.zeros(3)
        else:
            return mass,flags
# if "_and_" in run:
#     runs = run.split("_and_")
#     total = np.zeros(grid)
#     totflags = np.zeros(3)
#     for r in runs:
#         field,fldflags = get_mass(r,first)
#         sum1 = np.sum(field)
#         print(r+' field:' + str(sum1))
#         total = np.add(total,field)
#         totflags = np.add(totflags,fldflags)
#     w = hp.File(result,'w')
#     w.create_dataset(run,data=total)
#     w.create_dataset("flags",data=totflags)
#     print(totflags)

total,totflags = get_mass(run,first)
sum1 = np.sum(total)
print('first field: ' + str(sum1))
m,fl = get_mass(run,second)
totflags=np.add(totflags,fl)
sum2 =np.sum(m)
print('second field: ' + str(sum2))
total=np.add(total,m)
tot1 = np.sum(total)
print('first sum should be' + str(sum1+sum2)+', is: ' +str(tot1))
m,fl = get_mass(run,third)
sum3 = np.sum(m)
totflags=np.add(totflags,fl)
print('third field: ' + str(sum3))
total=np.add(total,m)
tot2=np.sum(total)
print('second sum should be ' + str(sum1+sum2+sum3)+', is: ' +str(tot2))
m,fl = get_mass(run,fourth)
totflags=np.add(totflags,fl)
sum4=np.sum(m)
print('third field: ' + str(sum4))
total = np.add(total,m)
tot3 = np.sum(total)
print('last sum should be '+str(sum1+sum2+sum3+sum4)+', is: '+ str(tot3))
w = hp.File(result,'w')
w.create_dataset(run,data=total)
w.create_dataset("flags",data=totflags)
print(totflags)

# if run == 'subhalo':
#     keys = ['red','blue','dim','bright','nondetection']
#     ls = ['magnitude','color']
#     w.hp.File(result, 'w')
#     for k in keys:
#         total = get_mass(k,first)
#         m = get_mass(k,second)
#         total = np.add(total,m)
#         m = get_mass(k,third)
#         total = np.add(total, m)
#         m = get_mass(k,fourth)
#         total = np.add(total,m)
#         w.create_dataset(k,data=total)
#     for l in ls:
#         total = get_field(l,first)
#         m = get_field(l,second)
#         total.extend(m)
#         m = get_field(l,third)
#         total.extend(m)
#         m=get_field(l,fourth)
#         total.extend(m)
#         w.create_dataset(l,data=total)
    

# def get_field(key,path):
#     try:
#         f=hp.File(path,'r')
#     except IOError:
#         print('files not found')
#         return []
#     else:
#         try:
#             field = f[key]
#         except KeyError:
#             print(key+' field not found - creating substitute')
#             return []
#         else:
#             return field
# if run == 'magnitude' or run == 'color':
#     """
#     Since these are lists rather than np arrays
#     """
#     total = get_field(run,first)
    
#     m = get_field(run,second)
    
#     total.extend(m)
#     m = get_field(run,third)
#     total.extend(m)
#     m = get_field(run,fourth)
#     total.extend(m)
#     w = hp.File(result,'w')
#     w.create_dataset(run,data=total)

        
