#!/bin/bash

#SBATCH --share 
#SBATCH --mail-user=cosinga@umd.edu
#SBATCH --mail-type=ALL
#SBATCH --t 01:00
#SBATCH	--ntasks= 2
#SBATCH	--mem-per-core=550
#SBATCH	--account = astronomy-hi
#SBATCH --job-name = hiptlbatchtest
#SBATCH --output = hiptlbatchtest.out

module load parallel

srun = "srun --share -N1 -n1"

parallel = "parallel --delay 0.2 -j $SLURM_NTASKS --joblog hiptltask.log
--resume"

$parallel "$srun ./hiptl.sh arg1:{1} > hiptl.sh.{1}" ::: {1:2}
