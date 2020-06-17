#!/bin/bash
tar -xzf python27.tar.gz
tar -xzf packages.tar.gz
export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/packages
export HOME=$PWD

cp /staging/cosinga/output/$1.gz ./

gunzip $1.gz

python compare.py $1

mv $1_dist.txt /staging/cosinga/storage