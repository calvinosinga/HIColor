#!/bin/bash
#SBATCH --share
#SBATCH --mail-user=cosinga@umd.edu
#SBATCH --mail-type=ALL
#SBATCH -t 01:00
#SBATCH -n 1
#SBATCH --mem=550

cd /homes/cosinga/lstr
. ~/.profile

module load python/2.7.8

python /homes/cosinga/HIColor/hiptl/hiptl.py
