f = open("commands.txt", "w")
fileno = 448
for i in range(fileno):
    if i==fileno-1:
        f.write("python3 /lustre/cosinga/hiptl/hiptl.py " +str(i))
    else:
        f.write("python3 /lustre/cosinga/hiptl/hiptl.py "+str(i)+"\n")
