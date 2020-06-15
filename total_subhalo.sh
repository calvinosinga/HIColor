#!/bin/bash
tar -xzf python27.tar.gz
tar -xzf packages.tar.gz
export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/packages
export HOME=$PWD

cp /staging/cosinga/output/blue_final.hdf5.gz
cp /staging/cosinga/output/red_final.hdf5.gz
cp /staging/cosinga/output/nondetection_final.hdf5.gz

gunzip blue_final.hdf5.gz
gunzip red_final.hdf5.gz
gunzip nondetection_final.hdf5.gz

python total_subhalo.py

gzip subhalo_final.hdf5

mv subhalo_final.gz /staging/cosinga/output
rm blue_final.hdf5
rm red_final.hdf5
rm nondetection_final.hdf5