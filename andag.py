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

varnam = ["run","file0","file1","file2","file3","result"]
varval = ["red_and_blue","red_final.hdf5","blue_final.hdf5","zeros.hdf5","zeros.hdf5","detection_final.hdf5"]
job("COMBINE_DETECTION", varnam,varval,"combine.sub")
varval = ["\"red_and_blue_and_nondetection\"","red_final.hdf5","blue_final.hdf5","nondetection_final.hdf5","zeros.hdf5","subhalo_final.hdf5"]
job("COMBINE_SUBHALO", varnam,varval,"combine.sub")


xpks = ["red","blue","nondetection","subhalo","detection","delta_HI","delta_m"]
varnam = ["file1","key1","file2","key2","pk1","pk2","xpk"]
detch =[]
subch = []
for i in xpks:
    for j in xpks:
        if not i==j:
            varvals=[i+'_final.hdf5',i,j+'_final.hdf5',j,i+"pk.txt",j+"pk.txt",i+'-'+j+'pk.txt']
            jobname = i+'_'+j
            job(jobname.upper(),varnam,varvals,"xpk.sub")
            if i == "detection" or j=="detection":
                detch.append(jobname.upper())
            if i == "subhalo" or j=="subhalo":
                subch.append(jobname.upper())

parch("COMBINE_DETECTION",detch)
parch("COMBINE_SUBHALO", subch)
