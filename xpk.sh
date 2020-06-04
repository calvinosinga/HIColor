#!/bin/bash
tar -xzf python27.tar.gz
tar -xzf packages.tar.gz
export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/packages
export HOME=$PWD

cp /staging/cosinga/output/$1.gz ./
cp /staging/cosinga/output/$3.gz ./

gunzip $1.gz
gunzip $3.gz

python analysis.py $1 $2 $3 $4 $5 $6 $7

rm $1
rm $3