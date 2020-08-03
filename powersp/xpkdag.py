from io import open
f = open('powersp/xpk.dag','w')

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


pks = ["red","blue","nondetection","subhalo","detection","delta_m"]
varnam = ["file1","key1","file2","key2","pk1","pk2","xpk"]

for i in pks:
    varvals = ["delta_HI_final.hdf5","delta_HI",i+'_final.hdf5',i,"delta_HIpk.txt",i+"pk.txt","delta_HI_"+i+"_xpk.txt"]
    job(("delta_HI_"+i+"_xpk").upper(),varnam,varvals,"xpk.sub")



his = []
for i in range(9):
    his.append("benhi_"+str(i)+".hdf5")
runs = ['GD14_map','GD14_vol','GK11_map','GK11_vol','K13_map','K13_vol','L08_map','S14_map','S14_vol']
for i in range(len(his)):
    for j in range(len(pks)):
        varvals = [his[i],"hi",pks[j]+"_final.hdf5",pks[j],runs[i]+"pk.txt",pks[j]+"pk.txt",runs[i]+"_"+pks[j]+"_xpk.txt"]
        job((runs[i]+"_"+pks[j]+"_xpk").upper(),varnam,varvals,"xpk.sub")
