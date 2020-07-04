from io import open
f = open('analysis.dag','w')

"""
JOBS:
STEP 1:
combine blue+red=detected
combine blue+red+nondetection = subhalos

STEP 2:
xpk for detections,nondetections,subhalos,pacohi,benhix9 models, ptl, red, blue, 
"""

def job(job, names, vals, subfile):
    """
    Creates a job with given name, variable names, and variable values. The variable names/vals must be iterable.
    """
    f.write("JOB "+str(job)+' '+subfile+"\n")
    for i in range(len(names)):
        f.write("VARS "+str(job)+ " "+str(names[i])+"= \""+str(vals[i])+"\"\n")
    
def parch(parents,children):
    f.write("PARENT ")
    f.write(parents+" " )
    f.write("CHILD ")
    for c in children:
        f.write(str(c)+" ")
    f.write("\n")


pks = ["red","blue","nondetection","subhalo","detection","delta_HI","delta_m"]
varnam = ["file","key","pk"]

for i in pks:
    varvals = [i+'_final.hdf5',i,i+"pk.txt"]
    job(i.upper(),varnam,varvals,"pk.sub")



bens = []
for i in range(9):
    bens.append("benhi_"+str(i)+".hdf5")
runs = ['GD14_map','GD14_vol','GK11_map','GK11_vol','K13_map','K13_vol','L08_map','S14_map','S14_vol']
for i in range(len(bens)):
    varvals = [bens[i],"hi",runs[i]+"pk.txt"]
    job(runs[i].upper(),varnam,varvals,"pk.sub")
    # for j in xpks:
    #     varvals = [bens[i],"hi",j+"_final.hdf5",j,runs[i]+"pk.txt",j+"pk.txt",runs[i]+'-'+j+'pk.txt']
    #     jobname = runs[i]+'_'+j
    #     job(jobname.upper(),varnam,varvals,"xpk.sub")