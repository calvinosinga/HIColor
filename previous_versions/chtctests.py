"""
A file that gathers data on the following:

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
import time
import h5py as hp
from io import open
import resource
grid = (2048,2048,2048)
LUM_MIN, LUM_THRESH = -16, -20 #detection minimum and threshold for breaking into dim/bright bins, from Swanson
def isred(gr, rband):#color definition as given in Swanson
    return gr> .9 - .03*(rband+23) 

SNAP_TO_Z = {99:0, 50:1} #can be used to convert snapshot number to its corresponding redshift
FILENO = 448 #number of chunk files in each groupcat file
PATH = '/mnt/a/calvin/' #base path to folder where inputs and outputs will be stored
BOXSIZE = 75.0 #Mpc/h, size of simulation (length along one side)

start = time.time()
ram = 0
def create_fields(input_path, output_path, snapno,fileno):
    """
    INPUTS:
    This method runs through the subhalo and halo data in TNG in input_path and extracts
    the desired properties and creates an hdf5 file containing them, at output_path. 

    snapno is the snapshot number (i.e. redshift) for the file.
    fileno is the number of file chunks that the TNG data has been split into

    OUTPUTS:
    saves fields_[snapno].hdf5 at output_path/output
    saves missingfiles.txt at output_path/output
    """
    print("creating fields")
    edges = np.linspace(0,BOXSIZE*1000, grid[0]) #definitions of bins
    missingfiles = [] # check to see if some files are empty (due to error in downloading)
    #each of the following are fields as described, binned by position of corresponding subhalo
    #galaxies = np.zeros(grid, dtype=np.float32) #solely subhalo masses
    #count = np.zeros(grid, dtype=np.int32) #the count of subhalos stored in each bin
    red_field = np.zeros(grid, dtype=np.float32) #masses of red galaxies, color defined by isred(...) method
    blue_field = np.zeros(grid, dtype=np.float32)# masses of blue galaxies
    #red_count = np.zeros(grid, dtype=np.int32) #subhalo count in each bin for red galaxies
    #blue_count = np.zeros(grid, dtype=np.int32)#subhalo count in each bin for blue galaxies
    color = []#for color-magnitude plot
    mag = []
    nondetection = np.zeros(grid, dtype=np.float32)# Below luminosity minimum as defined by LUM_MIN 
    dim = np.zeros(grid, dtype=np.float32)# Below luminosity threshold as defined by LUM_THRESH
    bright = np.zeros(grid, dtype=np.float32)# Above luminosity threshold as defined by LUM_THRESH
    total_mass=np.zeros(grid, dtype=np.float32) #All mass, detectable or not
    #group_mass=np.zeros(grid, dtype = np.float32) #Mass within FoF Halos

    # now starting the loop to compute the fields
    missing_files = open(output_path+'missing_files_'+unicode(snapno)+'.txt', 'w') #logs if a file is empty
    for i in range(fileno):
        print(i)
        haskey = True
        hasgroupkey = True
        hasfile = True
        try:
            f = hp.File(input_path+'fof_subhalo_tab_0'+unicode(snapno)+'.'+unicode(i)+'.hdf5','r')
        except IOError:
            hasfile = False
        if hasfile:
            try: #if a file is empty, raises KeyError when accessed. This handles that exception.
                pos = f['Subhalo']['SubhaloCM']
                photo = f['Subhalo']['SubhaloStellarPhotometrics']
                mass = f['Subhalo']['SubhaloMass']
            except KeyError:
                haskey=False
                missing_files.write(unicode(i))
            #making the fields using the groupcat
            try:
                gpos = f['Group']['GroupPos']
                gmass = f['Group']['GroupMass']
            except KeyError:
                hasgroupkey = False
            #If subhalo keytest passed...
            if haskey:
                bins = np.digitize(pos,edges)
                for j,b in enumerate(bins):
                    rmag = photo[j][5]
                    gmag = photo[j][4]
                    color.append(gmag-rmag)
                    mag.append(rmag)
                    total_mass[b[0],b[1],b[2]]+=mass[j]
                    if rmag<=LUM_MIN:
                        # if rmag is significant enough to be observed by (Swanson et al), include it in blue/red
                        galaxies[b[0],b[1],b[2]] += mass[j]
                        count[b[0],b[1],b[2]] +=1
                        if isred(gmag-rmag,rmag):
                            red_field[b[0],b[1],b[2]]+= mass[j]
                            red_count[b[0],b[1],b[2]]+=1
                        else:
                            blue_field[b[0],b[1],b[2]] += mass[j]
                            blue_count[b[0],b[1],b[2]] += 1

                        if rmag <= LUM_THRESH:
                            bright[b[0],b[1],b[2]] += mass[j]
                        else:
                            dim[b[0],b[1],b[2]] += mass[j]
                    else:
                        nondetection[b[0],b[1],b[2]] += mass[j]
            # If group keytest passed...
            if hasgroupkey:
                bins = np.digitize(gpos,edges)
                for j,b in enumerate(bins):
                    if 1024 in b: # Throws error -> a ptl lying outside bounds
                        outstring=unicode(i) + ' has a ptl lying outside simulation, ' + unicode(j)
                        missing_files.write(outstring)
                        print(outstring)
                    else:
                        group_mass[b[0],b[1],b[2]]+= gmass[j]

            f.close()
        # loop ends, saving data
        ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        w= hp.File(output_path+'/fields_'+unicode(snapno)+'.hdf5','w')
        w.create_dataset("galaxies", data=galaxies)
        w.create_dataset("count", data=count)
        w.create_dataset("red", data=red_field)
        w.create_dataset("blue", data=blue_field)
        w.create_dataset("red count", data=red_count)
        w.create_dataset("blue count", data=blue_count)
        w.create_dataset("nondetection", data=nondetection)
        w.create_dataset("bright", data=bright)
        w.create_dataset("dim", data=dim)
        w.create_dataset("color", data=color)
        w.create_dataset("magnitude", data=mag)
        w.create_dataset("total mass", data=total_mass)
        w.create_dataset("group mass", data=group_mass)
        w.close()


def ptl_fields(input_path, output_path, snapno, fileno):
    print("creating fields")
    edges = np.linspace(0,BOXSIZE*1000, grid[0]) #definitions of bins
    missingfiles = [] # check to see if some files are empty (due to error in downloading)
    #each of the following are fields as described, binned by position of corresponding subhalo
    galaxies = np.zeros(grid, dtype=np.float32) #solely subhalo masses
    count = np.zeros(grid, dtype=np.int32) #the count of subhalos stored in each bin
    red_field = np.zeros(grid, dtype=np.float32) #masses of red galaxies, color defined by isred(...) method
    blue_field = np.zeros(grid, dtype=np.float32)# masses of blue galaxies
    red_count = np.zeros(grid, dtype=np.int32) #subhalo count in each bin for red galaxies
    blue_count = np.zeros(grid, dtype=np.int32)#subhalo count in each bin for blue galaxies
    color = []#for color-magnitude plot
    mag = []
    nondetection = np.zeros(grid, dtype=np.float32)# Below luminosity minimum as defined by LUM_MIN 
    dim = np.zeros(grid, dtype=np.float32)# Below luminosity threshold as defined by LUM_THRESH
    bright = np.zeros(grid, dtype=np.float32)# Above luminosity threshold as defined by LUM_THRESH
    total_mass=np.zeros(grid, dtype=np.float32) #All mass, detectable or not
    group_mass=np.zeros(grid, dtype = np.float32) #Mass within FoF Halos
    for i in range(fileno):
        print(i)
        haskey = True
        hasgroupkey = True
        hasfile = True
        try:
            f = hp.File(input_path+'fof_subhalo_tab_0'+unicode(snapno)+'.'+unicode(i)+'.hdf5','r')
        except IOError:
            hasfile = False
        if hasfile:
create_fields(PATH+'chtctests_input/', PATH+'chtctests_output/', 99, FILENO)
stop = time.time()
logfile = open(PATH+'chtctests_output/log.txt')
logfile.write('subhalo runtime: ' + unicode(stop-start))
logfile.write('\n subhalo RAM usage: ' + unicode(ram))

start = time.time()
ptl_fields()
stop = time.time()
logfile.write('particle runtime: ' + unicode(stop-start))
logfile.write('\n particle RAM usage: '+ unicode(ram))