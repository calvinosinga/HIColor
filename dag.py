"""
This creates the dag file that I will use to run and distribute the workflow of the project.


todo:
add Diemer analysis
adjust subhalo part for the fact I'm now doing a field-by-field basis
change VARS to filenames
add throttling thing
add output filename
"""
from io import open
f = open('snapshot.dag', 'w')

ss = '99'
n= 448
joblist = []
for i in range(n):
    name = 'SUBHALO_'+str(i)
    joblist.append(name)
    f.write('JOB '+name+' subhalo.sub\n')
    f.write('VARS '+name+' runnumber=\"'+str(i)+'\"\n')
for i in range(n):
    name = 'PTL_'+str(i)
    joblist.append(name)
    f.write('JOB '+name+' ptl.sub\n')
    f.write('VARS '+name+' runnumber=\"'+str(i)+'\"\n')


for i in range(n/4): #112
    name = 'SUBHALO_COMBINE1_'+str(i)
    joblist.append(name)
    f.write('JOB '+name+' combine.sub\n')
    varname = 'chunk1=\"'+str(i)+'\"'+'chunk2=\"'+str(i+1)+'\"'+'chunk3=\"'+str(i+2)+'\"'+'chunk4=\"'+str(i+3)+'\"'
    varname = 'base=\"subhalo\" '+varname
    f.write('VARS '+name+' ' + varname)
    chunks = [i,i+1,i+2,i+3]
    for j in chunks:
        parents += 'SUBHALO_'+str(j)+' '
    f.write('PARENT '+ parents + 'CHILD '+ name+'\n')
for i in range(n/4):
    name = 'PTL_COMBINE1_'+str(i)
    joblist.append(name)
    f.write('JOB '+name+' combine.sub\n')
    varname = 'chunk1=\"'+str(i)+'\"'+'chunk2=\"'+str(i+1)+'\"'+'chunk3=\"'+str(i+2)+'\"'+'chunk4=\"'+str(i+3)+'\"'
    varname = 'base=\"ptl\" '+varname
    f.write('VARS '+name+' ' + varname)
    chunks = [i,i+1,i+2,i+3]
    for j in chunks:
        parents += 'PTL_'+str(j)+' '
    f.write('PARENT '+ parents + 'CHILD '+ name+'\n')

####### SECOND COMBINATION SEQUENCE #########################
for i in range(n/16): #28
    name = 'SUBHALO_COMBINE2_'+str(i)
    joblist.append(name)
    f.write('JOB '+name+' combine.sub\n')
    varname = 'chunk1=\"'+str(i)+'\"'+'chunk2=\"'+str(i+1)+'\"'+'chunk3=\"'+str(i+2)+'\"'+'chunk4=\"'+str(i+3)+'\"'
    varname = 'base=\"subhalo_combine1\" '+varname
    f.write('VARS '+name+' ' + varname)
    chunks = [i,i+1,i+2,i+3]
    for j in chunks:
        parents += 'SUBHALO_COMBINE1_'+str(j)+' '
    f.write('PARENT '+ parents + 'CHILD '+ name+'\n')
for i in range(n/16):
    name = 'PTL_COMBINE2_'+str(i)
    joblist.append(name)
    f.write('JOB '+name+' combine.sub\n')
    varname = 'chunk1=\"'+str(i)+'\"'+'chunk2=\"'+str(i+1)+'\"'+'chunk3=\"'+str(i+2)+'\"'+'chunk4=\"'+str(i+3)+'\"'
    varname = 'base=\"ptl_combine1\" '+varname
    f.write('VARS '+name+' ' + varname)
    chunks = [i,i+1,i+2,i+3]
    for j in chunks:
        parents += 'PTL_COMBINE1_'+str(j)+' '
    f.write('PARENT '+ parents + 'CHILD '+ name+'\n')
########## COMBINE SEQUENCE 3 ########################
for i in range(n/16/4): #28
    name = 'SUBHALO_COMBINE3_'+str(i)
    joblist.append(name)
    f.write('JOB '+name+' combine.sub\n')
    varname = 'chunk1=\"'+str(i)+'\"'+'chunk2=\"'+str(i+1)+'\"'+'chunk3=\"'+str(i+2)+'\"'+'chunk4=\"'+str(i+3)+'\"'
    varname = 'base=\"subhalo_combine2\" '+varname
    f.write('VARS '+name+' ' + varname)
    chunks = [i,i+1,i+2,i+3]
    for j in chunks:
        parents += 'SUBHALO_COMBINE2_'+str(j)+' '
    f.write('PARENT '+ parents + 'CHILD '+ name+'\n')
for i in range(n/16/4):
    name = 'PTL_COMBINE3_'+str(i)
    joblist.append(name)
    f.write('JOB '+name+' combine.sub\n')
    varname = 'chunk1=\"'+str(i)+'\"'+'chunk2=\"'+str(i+1)+'\"'+'chunk3=\"'+str(i+2)+'\"'+'chunk4=\"'+str(i+3)+'\"'
    varname = 'base=\"ptl_combine2\" '+varname
    f.write('VARS '+name+' ' + varname)
    chunks = [i,i+1,i+2,i+3]
    for j in chunks:
        parents += 'PTL_COMBINE2_'+str(j)+' '
    f.write('PARENT '+ parents + 'CHILD '+ name+'\n')
########## COMBINE SEQUENCE 4 #########################
# here we have 7, the plan is to combine 4 -> then combine remaining 4 (3+newly combine one)
name = 'SUBHALO_COMBINE4'
joblist.append(name)
f.write('JOB '+name+' combine.sub\n')
varname = 'chunk1=\"1\"'+'chunk2=\"2\"'+'chunk3=\"3\"'+'chunk4=\"4\"'
varname = 'base=\"subhalo_combine3\" '+varname
f.write('VARS '+name+' ' + varname)
chunks = [1,2,3,4]
for j in chunks:
    parents += 'SUBHALO_COMBINE3_'+str(j)+' '
f.write('PARENT '+ parents + 'CHILD '+ name+'\n')

name = 'PTL_COMBINE4'
joblist.append(name)
f.write('JOB '+name+' combine.sub\n')
varname = 'chunk1=\"1\"'+'chunk2=\"2\"'+'chunk3=\"3\"'+'chunk4=\"4\"'
varname = 'base=\"ptl_combine3\" '+varname
f.write('VARS '+name+' ' + varname)
chunks = [1,2,3,4]
for j in chunks:
    parents += 'PTL_COMBINE3_'+str(j)+' '
f.write('PARENT '+ parents + 'CHILD '+ name+'\n')

############## FINAL COMBINE SEQUENCE #############################

name = 'SUBHALO_FINAL'
joblist.append(name)
f.write('JOB '+name+' combine.sub\n')
varname = 'chunk1=\"0\"'+'chunk2=\"1\"'+'chunk3=\"2\"'+'chunk4=\"3\"'
varname = 'base=\"subhalo_final\" '+varname
f.write('VARS '+name+' ' + varname)
chunks = [4,5,6]
parents = 'SUBHALO_COMBINE4 '
for j in chunks:
    parents += 'SUBHALO_COMBINE3_'+str(j)+' '
f.write('PARENT '+ parents + 'CHILD '+ name+'\n')

name = 'PTL_FINAL'
joblist.append(name)
f.write('JOB '+name+' combine.sub\n')
varname = 'chunk1=\"0\"'+'chunk2=\"1\"'+'chunk3=\"2\"'+'chunk4=\"3\"'
varname = 'base=\"ptl_final\" '+varname
f.write('VARS '+name+' ' + varname)
chunks = [4,5,6]
parents = 'PTL_COMBINE4 '
for j in chunks:
    parents += 'PTL_COMBINE3_'+str(j)+' '
f.write('PARENT '+ parents + 'CHILD '+ name+'\n')

######## PK #########################################################
f.write('JOB ANALYSIS analysis.sub\n')
f.write('PARENT PTL_FINAL SUBHALO_FINAL CHILD ANALYSIS')
