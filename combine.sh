#!/bin/bash

tar -xzf python27.tar.gz
tar -xzf packages.tar.gz
export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/packages
export HOME=$PWD

cp /staging/cosinga/output/$2.gz ./
cp /staging/cosinga/output/$3.gz ./
cp /staging/cosinga/output/$4.gz ./
cp /staging/cosinga/output/$5.gz ./

gunzip $2.gz
gunzip $3.gz
gunzip $4.gz
gunzip $5.gz

python combine.py $1 $2 $3 $4 $5 $6

gzip $6
mv $6.gz /staging/cosinga/output
rm $2
rm $3
rm $4
rm $5