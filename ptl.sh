#!/bin/bash

tar -xzf python27.tar.gz
tar -xzf packages.tar.gz
export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/packages
export HOME=$PWD

cp /staging/cosinga/ptl99/snap_0$2.$1.hdf5.gz ./
gunzip snap_0$2_$1.hdf5.gz

python ptl.py $1 $2
gzip ptl_$2_$1.hdf5
mv ptl_$2_$1.hdf5.gz /staging/cosinga/output
rm snap_0$2.$1.hdf5