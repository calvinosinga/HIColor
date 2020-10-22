#!/bin/bash

cd /homes/cosinga/lstr
. ~/.profile

module load python/2.7.8

python /homes/cosinga/HIColor/hiptl/hiptl.py $1

