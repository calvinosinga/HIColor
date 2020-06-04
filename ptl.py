"""
Create the total mass field using the particle snapshots. 
"""
import numpy as np
import h5py as hp
import sys
########## INPUTS #################
grid = (2048,2048,2048)
chunk = sys.argv[1]
snapshot = sys.argv[2]
# BOXSIZE = 75 #Mpc/h
###################################

flags= np.zeros(3,dtype=np.int32)
try:
    f= hp.File("snap_0"+str(snapshot)+'.'+str(chunk)+".hdf5",'r')
except IOError:
    flags[0]=1 
keys = list(f.keys())
header = dict(f['Header'].attrs)
BOXSIZE = 0.001*header['BoxSize'] #Mpc/h
dkptl = header['MassTable'][1]
nptl = header['NumPart_ThisFile']
edges = np.linspace(0,BOXSIZE, grid[0])
total = np.zeros(grid, dtype=np.float32)
ptlcount = np.zeros(6)

def add_field(file,key,field):
    """
    Just a quick helper method. Adds corresponding mass field to running total.
    """
    count = 0
    has_key = True
    try:
        mass=f[key]["Masses"]
        pos = 0.001*f[key]["Coordinates"][:] #Mpc/h
    except KeyError:
        has_key=False
        flags[1] = 1

    if has_key:
        print('mass for '+str(k)+': '+str(np.sum(mass)))
        print('current running total: '+str(np.sum(field)))
        print('so the new total should be '+ str(np.sum(mass)+np.sum(field)))
        bins = np.digitize(pos,edges)
        for ptl,b in enumerate(bins):
            field[b[0],b[1],b[2]]+=mass[ptl]
            count += 1
        print('the new total is: '+str(np.sum(field))+'\n')

    return field, count
    
      
for k in keys:
    if k=="PartType0":
        total, ptlcount[0] = add_field(f,k,total)
    elif k=="PartType1":
        
        pos = f[k]['Coordinates']
        print('mass for '+str(k)+': '+str(len(pos)*dkptl))
        print('current running total: '+str(np.sum(total)))
        print('so the new total should be '+ str(len(pos)*dkptl+np.sum(total)))
        bins = np.digitize(pos,edges)
        for ptl,b in enumerate(bins):
            total[b[0],b[1],b[2]]+=dkptl
            ptlcount[1]+=1
        print('the new total is: '+str(np.sum(total))+'\n')
    elif k=="PartType4":
        total,ptlcount[4] = add_field(f,k,total)
    elif k=="PartType5":
        total,ptlcount[5] = add_field(f,k,total)
if not nptl == ptlcount:
    flags[2]=1
w = hp.File('ptl_'+str(snapshot)+'_'+str(chunk)+'.hdf5', 'w')
w.create_dataset("mass", data=total)
w.create_dataset("flags", data=flags)
