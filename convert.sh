#!/bin/bash
tar -xzf python27.tar.gz
tar -xzf packages.tar.gz
export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/packages
export HOME=$PWD

cp /staging/cosinga/output/$1.gz ./

gunzip $1.gz

python convert.py $1

gzip delta_hi_paco.hdf5
gzip delta_m_paco.hdf5

mv delta_hi_paco.hdf5.gz /staging/cosinga/output
mv delta_m_paco.hdf5.gz /staging/cosinga/output
