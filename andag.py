from io import open
f = open('analysis.dag','w')

"""
JOBS:
STEP 1:
combine blue+red=detected
combine blue+red+nondetection = subhalos
separate paco's fields into hi/ptl
compare paco and benedikt distributions

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
    for p in parents:
        f.write(str(p)+" " )
    f.write("CHILD ")
    for c in children:
        f.write(str(c)+" ")
    f.write("\n")

varnam = ["run","file0","file1","file2","file3","result"]
varval = ["\"red-blue\"","\"red_final.hdf5\"","\"blue_final.hdf5\"","zeros.hdf5","zeros.hdf5","\"detection.hdf5\""]
job("COMBINE_DETECTION", varnam,varval,"combine.sub")
varval = ["\"red-blue-nondetection\"","\"red_final.hdf5\"","\"blue_final.hdf5\"","\"nondetection_final.hdf5\"","\"zeros.hdf5\"","\"subhalos.hdf5\""]
job("COMBINE_SUBHALO", varnam,varval,"combine.sub")


