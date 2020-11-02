#!/bin/sh

#SBATCH --share
#SBATCH --job-name=jobdist
#SBATCH --time=01:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --mail-user=cosinga@umd.edu
#SBATCH --mail-type=ALL
#SBATCH --account=astronomy-hi

cd /homes/cosinga/HIColor

. ~/.profile

module load python/3.7.7
python job_distributor.py
