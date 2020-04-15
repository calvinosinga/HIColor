"""
This file creates the DAG file that will combine all of the chunks into a single file
"""
from io import open
f = open('snapshot_99.dag', 'w')

for i in range(448):
    name = 'COLOR_'+str(i)
    f.write('JOB '+name+' subhalo_color.sub\n')
    f.write('VARS '+name+' runnumber=\"'+str(i)+'\"\n')
for i in range(448):
    name='LUMIN_'+str(i)
    f.write('JOB '+name+' subhalo_lum.sub\n')
    f.write('VARS '+name+' runnumber=\"'+str(i)+'\"\n')
for i in range(448/4):
    name='COMBINE1_COLOR_'+str(i)
    f.write('JOB '+name+' combine_chunks.sub\n')
    f.write('VARS ' + name + ' type=\"color1\" runnumber=\"'+str(i)+'\"\n')
    x = (4*i,4*i+1,4*i+2,4*i+3)
    parent = 'PARENT COLOR_'+str(x[0])+' '+'COLOR_'+str(x[1])+' '+'COLOR_'+str(x[2])+' '+'COLOR_'+str(x[3])
    child = ' CHILD ' + name
    f.write(parent+child)
for i in range(448/4):
    name='COMBINE1_LUMIN_'+str(i)
    f.write('JOB '+name+' combine_chunks.sub\n')
    f.write('VARS ' + name + ' type=\"lumin1\" runnumber=\"'+str(i)+'\"\n')

for i in range(112/4):
    name='COMBINE2_COLOR_'+str(i)
    f.write('JOB '+name+' combine_chunks.sub\n')
    f.write('VARS ' + name + ' type=\"color2\" runnumber=\"'+str(i)+'\"\n')
    x = (4*i,4*i+1,4*i+2,4*i+3)
    base = 'COMBINE1_COLOR_'
    parent = 'PARENT '+base+str(x[0])+' '+base+str(x[1])+' '+base+str(x[2])+' '+base+str(x[3])
    child = ' CHILD ' + name
    f.write(parent+child)
for i in range(112/4):
    name='COMBINE2_LUMIN_'+str(i)
    f.write('JOB '+name+' combine_chunks.sub\n')
    f.write('VARS ' + name + ' type=\"lumin2\" runnumber=\"'+str(i)+'\"\n')
for i in range(28/4):
    name='COMBINE3_COLOR_'+str(i)
    f.write('JOB '+name+' combine_chunks.sub\n')
    f.write('VARS ' + name + ' type=\"color3\" runnumber=\"'+str(i)+'\"\n')
    x = (4*i,4*i+1,4*i+2,4*i+3)
    parent = 'PARENT COLOR_'+str(x[0])+' '+'COLOR_'+str(x[1])+' '+'COLOR_'+str(x[2])+' '+'COLOR_'+str(x[3])
    child = ' CHILD ' + name
    f.write(parent+child)
for i in range(28/4):
    name='COMBINE3_LUMIN_'+str(i)
    f.write('JOB '+name+' combine_chunks.sub\n')
    f.write('VARS ' + name + ' type=\"lumin3\" runnumber=\"'+str(i)+'\"\n')

name='COMBINE4_COLOR_1'
f.write('JOB '+name+' combine_chunks.sub\n')
f.write('VARS ' + name + ' type=\"color4\" runnumber=\"'+str(i)+'\"\n')
name='COMBINE4_COLOR_2'
f.write('JOB '+name+' combine_chunks.sub\n')
f.write('VARS ' + name + ' type=\"color4\" runnumber=\"'+str(i)+'\"\n')
for i in range(2):
    name='COMBINE3_LUMIN_'+str(i)
    f.write('JOB '+name+' combine_chunks.sub\n')
    f.write('VARS ' + name + ' type=\"lumin4\" runnumber=\"'+str(i)+'\"\n')
name = 'COMBINE_COLOR_FINAL'
f.write('JOB '+name+' combine_chunks.sub\n')
f.write('VARS ' + name + ' type=\"color5\" runnumber=\"0\"\n')
name = 'COMBINE_LUMIN_FINAL'
f.write('JOB '+name+' combine_chunks.sub\n')
f.write('VARS ' + name + ' type=\"lumin5\" runnumber=\"0\"\n')
f.write('JOB PK pk.sub')
