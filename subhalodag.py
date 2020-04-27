"""
Creates the dag file that will be used for the subhalo files.
"""
from io import open
f=open("subhalo.dag", 'w')
ss='99'
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

runs = ["bright","dim","nondetection", "red","blue", "magnitude", "color"]
n = 448
for r in runs:
    varnames = ["chunk","run","ss"]
    for i in range(n):
        varvals = [str(i),r,ss]
        job(r+str(i),varnames,varvals, "subhalo.sub")
    varnames = ["run","file0","file1","file2","file3","output"]
    for i in range(int(n/4)):
        varvals = [r]
        pars = []
        for j in range(4):
            pars.append(r+str(4*i+j))
            varvals.append(r+str(4*i+j)+".hdf5")
        varvals.append(r+str(i)+"_combine0.hdf5")
        job(r+str(i)+"_combine0",varnames,varvals,"combine.sub")
        parch(pars,[r+str(i)+"_combine0"])
    for i in range(int(n/16)):
        varvals = [r]
        pars = []
        for j in range(4):
            pars.append(r+str(4*i+j)+"_combine0")
            varvals.append(r+str(4*i+j)+"_combine0.hdf5")
        varvals.append(r+str(i)+"_combine1.hdf5")
        job(r+str(i)+"_combine1",varnames,varvals, "combine.sub")
        parch(pars,[r+str(i)+"_combine1"])
    for i in range(int(n/64)):
        varvals = [r]
        pars = []
        for j in range(4):
            pars.append(r+str(4*i+j)+"_combine1")
            varvals.append(r+str(4*i+j)+"_combine1.hdf5")
        varvals.append(r+str(i)+"_combine2.hdf5")
        job(r+str(i)+"_combine2",varnames,varvals, "combine.sub")
        parch(pars,[r+str(i)+"_combine2"])
    varvals = [r]
    pars = []
    for j in range(4):
        pars.append(r+str(j)+"_combine2")
        varvals.append(r+str(j)+"_combine2.hdf5")
    varvals.append(r+"_combine3.hdf5")
    job(r+"_combine3",varnames,varvals, "combine.sub")
    parch(pars,[r+"_combine3"])

    varvals = [r]
    pars = []
    for j in range(3):
        pars.append(r+str(4+j))
        varvals.append(r+str(4+j)+"_combine2.hdf5")
    varvals.append(r+"_combine3.hdf5")
    varvals.append(r+"_final.hdf5")
    pars.append(r+"_combine3")
    job(r+"_final",varnames,varvals, "combine.sub")
    parch(pars,[r+"_final"])
