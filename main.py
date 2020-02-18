"""
This file contains all the methods used in the data analysis, and manages and distributes tasks.

TODO: When getting the density fields, test a few different ways of averaging the mass into densities

Should I be summing rather than using mean for average density

When averaging the HI fields, should I be dividing the fields by 8?

Check for flagged subhalos

Divide by zero warning when calculating blue correlation?

what does the delta_HI represent again? Is it already in overdensities?

Empty files

Are nondetections usually caused by low mass galaxies? -> mass bins

Analyze sampling -> get those 2d histogram plots from paco
"""

import numpy as np
import h5py as hp
from io import open
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from Pk_library import XPk
from Pk_library import Pk
############## INPUTS ######################################
grid = (1024,1024,1024) # change for run on CHTC to (2048,2048,2048)
LUM_MIN, LUM_THRESH = -16, -20 #detection minimum and threshold for breaking into dim/bright bins, from Swanson
def isred(gr, rband):#color definition as given in Swanson
    return gr> .9 - .03*(rband+23) 

SNAP_TO_Z = {99:0, 50:1} #can be used to convert snapshot number to its corresponding redshift
FILENO = 448 #number of chunk files in each groupcat file
PATH = '/mnt/a/calvin/' #base path to folder where inputs and outputs will be stored
BOXSIZE = 75.0 #Mpc/h, size of simulation (length along one side)

#############################################################


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

    # now starting the loop to compute the fields
    missing_files = open(output_path+'missing_files_'+unicode(snapno)+'.txt', 'w') #logs if a file is empty
    for i in range(fileno):
        print(i)
        haskey = True
        hasgroupkey = True
        f = hp.File(input_path+'fof_subhalo_tab_0'+unicode(snapno)+'.'+unicode(i)+'.hdf5','r')
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
    

def hi_fields(input_path, output_path, snapno):
    """
    INPUTS:
    input_path is the path to the folder that stores Paco's fields and the TNG data.
    ouput_path is the path to the folder that will save the averaged fields (2048->grid)
    snapno is the snapshot number

    OUTPUT:
    Saves HI and matter density fields at delta_avg_z=[redshift].hdf5
    """
    print("creating HI fields")
    redshift = SNAP_TO_Z[snapno]
    f= hp.File(input_path+'fields_z='+unicode(redshift)+'.0.hdf5','r')
    w= hp.File(output_path+'delta_avg_z='+unicode(redshift)+'.hdf5', 'w')
    delta = f['delta_HI'][:]
    #local machine can only handle averaging one of the fields at a time, why its split into two
    if grid[0] == 1024: # if the grid is not the usual 2048, then average the field.
        delta = avg_field(delta)
    
    w.create_dataset("HI", data=delta)
    delta = f['delta_m'][:]
    if grid[0] == 1024:
        delta = avg_field(delta)
    w.create_dataset("delta_m", data=delta)
    w.close()
    f.close()


def avg_field(field):
    """
    Averages a (2048,2048,2048) grid to a (1024,1024,1024) grid. Helper method for hi_fields(...)
    """
    evens = field[::2]
    odds = field[1::2]
    subtot = np.add(evens,odds)
    evens = subtot[:,::2,:]
    odds = subtot[:,1::2,:]
    subtot = np.add(evens,odds)
    evens = subtot[:,:,::2]
    odds = subtot[:,:,1::2]
    subtot=np.add(evens,odds)
    subtot /= 8.0
    return subtot


def color_magnitude(filename,plot_path, snapno):
    """
    This method generates the color-magnitude plot. This will be used to get an idea of the distribution of subhalos
    within TNG.
    INPUTS:
    filename is the path to the FILE (not the folder) that contains the color and magnitude information.
    plot_path is the folder in which the plots will be saved.
    snapno is the snapshot number.

    OUTPUTS:
    color_magnitude_bins_[snapno] is a scatter plot that displays the divisions between the subhalo population
    into nondetections, red and blue galaxies based on Swanson et al.
    """
    print("color magnitude plots started")
    f = hp.File(filename, 'r')
    col = np.array(f["color"][:])
    mag = np.array(f["magnitude"][:])
    plt.hist(col, bins=20, density=True, stacked=True)
    plt.title("color bimodality")
    plt.xlabel("color (g-r)")
    plt.ylabel("percentage of total="+unicode(len(col)))
    plt.savefig(plot_path+"color_bimodality_z="+unicode(snapno))
    plt.clf()
    plt.hist2d(col,mag, bins=50, range=((-.5,1),(-30,-5)), cmin=50)
    y=np.linspace(-35,0)
    x= .9-.03*(y+23)
    plt.plot(x, y, color='r')
    plt.title("Color-Magnitude plot")
    plt.xlabel("color (g-r)")
    plt.ylabel("magnitude")
    plt.colorbar()
    plt.savefig(plot_path+'color_magnitude_bins_'+unicode(snapno))
    plt.clf()
    # The following is making a plot to see how the sample is split among the three groups

    red = []
    magred = []
    blu = []
    magblu = []
    nondet = []
    magnon = []
    detected = []
    count = 0
    for i in range(len(col)):
        if mag[i]<LUM_MIN:
            detected.append(col[i])
            if isred(col[i],mag[i]):
                red.append(col[i])
                magred.append(mag[i])
            else:
                blu.append(col[i])
                magblu.append(mag[i])
        else:
            nondet.append(col[i])
            magnon.append(mag[i])
            if mag[i]>-5:
                count+=1
    plt.scatter(red, magred, label='red galaxies', color= 'r',s=.25)
    plt.scatter(blu, magblu, label='blue galaxies', color='b', s=.25)
    plt.scatter(nondet, magnon, label='nondetections, with '+unicode(count)+' off plot', color='k', s=.25)
    plt.ylim(-5,-30)
    plt.ylabel('luminosity (magnitude)')
    plt.xlabel('color (g-r)')
    plt.legend()
    plt.title('Color-Magnitude plots using cuts from Swanson')
    plt.savefig(plot_path+'color_magnitude_Swanson_z='+unicode(snapno))
    plt.clf()

    #making same plot as the first one, looking for color bimodality, except removing the dim subhalos
    detected = np.array(detected)
    
    plt.hist(detected, bins=20, density=True, stacked=True)
    plt.title("detectable sources color bimodality (total =" + unicode(len(detected)))
    plt.xlabel("color (g-r)")
    plt.ylabel("percentage")
    plt.savefig(plot_path+"color_bimodality_bright_sources_z="+unicode(snapno))
    plt.clf()

      
def field_pk(field_path, pk_path, snapno):
    """
    Calculates the cross-power spectra between hi and each of the properties stored 
    """
    print("calculating power spectra")
    redshift = SNAP_TO_Z[snapno]
    f = hp.File(field_path+'delta_avg_z='+unicode(redshift)+'.hdf5','r')
    g = hp.File(field_path+'fields_'+unicode(snapno)+'.hdf5','r')
    print(list(f.keys()))
    print(list(g.keys()))
    dhi = f['HI'][:]
    dhi /= np.mean(dhi, dtype = np.float32); dhi -= 1
    dhi = np.float32(dhi)
    f.close()
    keys = list(g.keys())

    for k in keys: #for each property, calculate the desired spectra
        if not ('count' in str(k)) and (g[k]).shape==grid: #if it has count in the key, if wrong dim, it is not meant for pk
            print(k)
            prop = g[k][:]
            print(prop.dtype)
            avg_density = np.sum(prop, dtype=np.float32)/75**3
            prop = prop* grid[0]**3/(75**3) #turning the property mass bins into densities
            print(prop.dtype)
            prop = prop/avg_density; prop -= 1 #now getting overdensities CHECK
            print(prop.dtype)
            prop = np.float32(prop)
            print(prop.dtype)
            pk = XPk([prop,dhi],BOXSIZE, axis = 0, MAS = 'CIC')
            np.savetxt(pk_path+'Pk_'+str(k)+'_z='+unicode(redshift)+'.0.txt',np.transpose([pk.k3D, pk.Pk[:,0,0]]))
            np.savetxt(pk_path+'Pk2D_'+str(k)+'_z='+unicode(redshift)+'.0.txt',np.transpose([pk.kpar, pk.kper, pk.Pk2D[:,0]]))
            np.savetxt(pk_path+'Pk_HI_cross_' + str(k)+'_z='+unicode(redshift)+'.0.txt', np.transpose([pk.k3D, pk.XPk[:,0,0]]))
            np.savetxt(pk_path+'Pk2D_HI_cross_'+str(k)+'_z='+unicode(redshift)+'.0.txt', np.transpose([pk.kpar, pk.kper, pk.PkX2D[:,0]]))
    

def color_1Dpk(pk_path, plot_path, snapno):
    """
    Plots the power spectrum of red/blue galaxies
    """
    print("color power spectrum")
    redshift = SNAP_TO_Z[snapno]
    rpk, _, rpkx, _ = load_pk('red', redshift, pk_path)
    bpk, _, bpkx, _ = load_pk('blue', redshift, pk_path)
    gpk, _, gpx, _ = load_pk('galaxies', redshift, pk_path)
    #comparing red autopk, red-hi Xpk, hi autopk
    plt.plot(rpk[:,0], rpk[:,1], label='red auto')
    plt.plot(rpkx[:,0], rpkx[:,1], label='red-HI cross')
    plt.plot(bpk[:,0], bpk[:,1], label='blue auto')
    plt.plot(bpkx[:,0], bpkx[:,1], label='blue-HI cross')
    plt.plot(gpk[:,0], gpk[:,1], label='galaxies auto')
    plt.plot(gpx[:,0],gpx[:,1], label='galaxies-HI cross')
    #plt.plot(hipk[:,0], hipk[:,1], label='HI auto')
    plt.legend()

    plt.ylabel('P(K) (h Mpc^-1)^3')
    plt.xlabel('k (h Mpc^-1)')
    plt.title('Color Power Spectra')
    plt.yscale('log')
    plt.xscale('log')
    plt.savefig(plot_path+'pk_color_z='+unicode(redshift))
    plt.clf()
    plt.plot(rpkx[:,0], rpkx[:,1], label='red-HI cross')
    plt.plot(bpkx[:,0], bpkx[:,1], label='blue-HI cross')
    plt.plot(gpx[:,0],gpx[:,1], label='galaxies-HI cross')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('P(K) (h Mpc^-1)^3')
    plt.xlabel('k (h Mpc^-1)')
    plt.title('Color Power Spectra')
    plt.legend()
    plt.savefig(plot_path+'xpk_color_z=' +unicode(redshift))
    # plt.xlim(.1,10)
    # plt.ylim(5,10**4)


def load_pk(moniker, redshift, pk_path):
    """
    A helper method for all of the pk plotting routines that loads all the associated power spectra for
    a property specified by moniker and redshift, in addition to the HI power spectrum. pk_path is the basepath 
    to the folder containing the power spectra.
    """
    pk1 = np.loadtxt(pk_path+'Pk_'+moniker+'_z='+unicode(redshift)+'.0.txt')
    pk = np.loadtxt(pk_path+'Pk2D_'+moniker+'_z='+unicode(redshift)+'.0.txt')
    pkx = np.loadtxt(pk_path+'Pk_HI_cross_'+moniker+'_z='+unicode(redshift)+'.0.txt')
    pkxx= np.loadtxt(pk_path+'Pk2D_HI_cross_'+moniker+'_z='+unicode(redshift)+'.0.txt')
    #pkhi = np.loadtxt(pk_path+'Pk_HI_z='+unicode(redshift)+'.0.txt')
    #return pk1, pk, pkx, pkxx, pkhi
    return pk1, pk, pkx, pkxx


def field_occ(f1,f2, is_overden):
    total1 = np.sum(f1)
    total2 = np.sum(f2)
    occ1 = np.sum(f1, axis=(1,2))
    occ2 = np.sum(f2, axis=(1,2))
    if is_overden:
        return occ1,occ2
    else:
        occ1 /= total1; occ2 /= total2
        return occ1, occ2


def plot_occupation(o1,o2, path, name):
    plt.plot(o1, label='my occupation')
    plt.plot(o2, label='paco occupation')
    plt.title(name)
    plt.xlabel('bin index')
    plt.ylabel('occupation percentage')
    plt.legend()
    plt.savefig(path+'occ_'+name)
    plt.clf()


def test_field_occupations(field_path,pk_path, plot_path, snapno):
    """
    Compares the occupations of my fields compared to Paco's
    """
    print('making occupation plots')
    edges = np.linspace(0,BOXSIZE, grid[0])
    f = hp.File(field_path+'fields_'+unicode(snapno)+'.hdf5', 'r')
    g = hp.File(field_path+'delta_avg_z=0.hdf5','r')
    mine = f['group mass'][:]
    paco = g['delta_m'][:]
    mytotal = np.sum(mine)/75**3
    #ptotal = np.sum(paco)/75**3
    zeros = np.zeros(grid)
    test = np.less(paco,zeros)
    test = np.any(test)
    print(test)
    occo,pocco=field_occ(mine,paco, False)
    plot_occupation(occo,pocco, plot_path, 'untouched')
    mine *= 10**10/.6774
    occo,pocco=field_occ(mine,paco, False)
    plot_occupation(occo,pocco, plot_path, 'stellar units')
    mine /= 10**10/.6774
    mine /= (edges[1]-edges[0])**3
    occo,pocco=field_occ(mine,paco, False)
    plot_occupation(occo,pocco, plot_path, 'density')
    occo=occo**2
    plot_occupation(occo,pocco, plot_path, 'density_squared')
    occo = occo**3
    plot_occupation(occo, pocco, plot_path, 'density_cubed')
    denmean = np.mean(mine)
    mine/=denmean; mine-=1
    occo,pocco=field_occ(mine,paco, True)
    pocco /= np.sum(paco)
    plot_occupation(occo,pocco, plot_path, 'overdensity')
    paco /= np.mean(paco); paco-=1
    occo,pocco=field_occ(mine,paco, True)
    plot_occupation(occo,pocco, plot_path, 'both overdensity')
    #ratio = np.divide(occ,pacocc)
    print('calculated from mass: ' + str(mytotal))
    print('calculated from density: '+ str(denmean))


def test_densities(field_path,pk_path, plot_path, snapno):
    print('testing density differences')
    edges = np.linspace(0,BOXSIZE, grid[0])
    f = hp.File(field_path+'fields_'+unicode(snapno)+'.hdf5', 'r')
    g = hp.File(field_path+'delta_avg_z=0.hdf5','r')
    mine = f['total mass'][:]
    paco = g['delta_m'][:]
    mine /= (edges[1]-edges[0])**3
    mine /= np.mean(mine); mine -= 1
    paco /= np.mean(paco); paco -= 1
    paco= np.square(np.square(paco))
    mine= np.square(mine)
    occo,pocco=field_occ(mine,paco, False)
    plot_occupation(occo, pocco, plot_path, 'squaredx2 overdensity')
    dif = occo - pocco
    dif = np.sort(dif)
    plt.plot(dif)
    plt.title('difference in density')
    plt.savefig(plot_path+'differences')


def plot_tested_fields(field_path,pk_path, plot_path, snapno):
    """
    A method trying to locate the source of the error between paco's plot and mine
    """
    print('testing field calculations')
    redshift = SNAP_TO_Z[snapno]
    f = hp.File(field_path+'fields_'+unicode(snapno)+'.hdf5', 'r')
    edges = np.linspace(0,BOXSIZE, grid[0])
    #print(str(edges[-2]) +'  '+ str(edges[-1]))
    my_field = f['group mass'][:]
    print('my fields average mass: ' + str(np.mean(my_field)))
    my_field /= (edges[1]-edges[0])**3
    #my_field *= 1e10/.6774
    print('my fields average density: ' + str(np.mean(my_field)))
    print('Pacos avg density: ' + str(4210649.5))
    my_field /= np.mean(my_field); my_field -= 1
    pk = Pk(my_field,BOXSIZE, axis = 0, MAS='CIC')
    tpk = np.transpose([pk.k3D,pk.Pk[:,0]])
    paco = np.loadtxt(PATH+'Pk_m_z=0.0.txt')
    mine = np.loadtxt(pk_path+'Pk_paco_z=0.0.txt')
    plt.plot(paco[:,0], paco[:,1], label='True power spectrum')
    plt.plot(mine[:,0], mine[:,1], label='True field, my calculation')
    plt.plot(tpk[:,0], tpk[:,1], label='My field, my calculation adjusted')
    plt.legend()

    plt.ylabel('P(K) (h Mpc^-1)^3')
    plt.xlabel('k (h Mpc^-1)')
    plt.title('matter power spectrum')
    plt.yscale('log')
    plt.xscale('log')
    plt.savefig(plot_path+'power spectrum comparison adjusted')


def create_tests(field_path, pk_path, plot_path, snapno):
    print('creating test fields')
    redshift = SNAP_TO_Z[snapno]
    f = hp.File(field_path+'delta_avg_z='+unicode(redshift)+'.hdf5','r')
    dhi = f['HI'][:]
    dm = f['delta_m'][:]
    #print(np.mean(dm))
    #print(np.mean(dhi))
    # avg_hi = np.sum(dhi)/75**3
    # avg_m = np.sum(dm)/75**3
    dhi /= np.mean(dhi); dhi -= 1
    #dhi = np.float32(dhi)
    dm /= np.mean(dm); dm -= 1
    #dm = np.float32(dhi)
    print(np.mean(dm))
    print(np.mean(dhi))
    pk = XPk([dm,dhi],BOXSIZE, axis = 0, MAS = 'CIC')
    # pk1 = np.transpose([pk.k3D,pk.Pk[:,0,0]])
    # paco = np.loadtxt(PATH+'Pk_m_z=0.0.txt')
    # plt.plot(paco[:,0], paco[:,1], label='True power spectrum')
    # plt.plot(pk1[:,0], pk1[:,1], label='True field, my calculation')
    # plt.legend()

    # plt.ylabel('P(K) (h Mpc^-1)^3')
    # plt.xlabel('k (h Mpc^-1)')
    # plt.title('Testing my calculations')
    # plt.yscale('log')
    # plt.xscale('log')
    # plt.savefig(plot_path+'calculation comparison')
    k='paco'
    np.savetxt(pk_path+'Pk_'+str(k)+'_z='+unicode(redshift)+'.0.txt',np.transpose([pk.k3D, pk.Pk[:,0,0]]))
    np.savetxt(pk_path+'Pk2D_'+str(k)+'_z='+unicode(redshift)+'.0.txt',np.transpose([pk.kpar, pk.kper, pk.Pk2D[:,0]]))
    np.savetxt(pk_path+'Pk_HI_cross_' + str(k)+'_z='+unicode(redshift)+'.0.txt', np.transpose([pk.k3D, pk.XPk[:,0,0]]))
    np.savetxt(pk_path+'Pk2D_HI_cross_'+str(k)+'_z='+unicode(redshift)+'.0.txt', np.transpose([pk.kpar, pk.kper, pk.PkX2D[:,0]]))


def main():
    """
    Handles io and params for interactions between the methods. Uncomment all methods to do a full run all at once.
    """
    create_fields(PATH+'input/', PATH+'output/', 99, FILENO)
    test_field_occupations(PATH+'output/', PATH+'power spectrum/',PATH+'plots/', 99)
    color_1Dpk(PATH+'power spectrum/', PATH+'plots/',99)
    
    



main()
