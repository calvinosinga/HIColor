#!/bin/bash
tar -xzf python27.tar.gz
tar -xzf packages.tar.gz
export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/packages
export HOME=$PWD

cp /staging/cosinga/output/$1.gz ./
cp /staging/cosinga/output/$2.gz ./

gunzip $1.gz
gunzip $2.gz

python hi.py $1 $2 $3

gzip benhi_$3.hdf5
mv benhi_$3.hdf5.gz /staging/cosinga/output
rm $1
rm $2