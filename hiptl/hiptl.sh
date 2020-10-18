#!/bin/bash
#SBATCH --share
#SBATCH --mail-user=cosinga@umd.edu
#SBATCH --mail-type=ALL
#SBATCH -t 00:30
#SBATCH -n 1
#SBATCH +60

cd /homes/cosinga/lstr
. ~/.profile

module load python/2.7.8

python /homes/cosinga/HIColor/hiptl/hiptl.py
