#!/bin/bash

tar -xzf python27.tar.gz
tar -xzf packages.tar.gz
export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/packages
export HOME=$PWD

python subhalo.py $1 $2 $3 $4

gzip $2$1_$4.hdf5
mv $2$1_$4.hdf5.gz /staging/cosinga/output
rm fof_*