#!/bin/bash

cd ./examples
for d in *
do
    cd $d
    dir_name=${PWD##*/}
    echo "Compiling $dir_name..."
    #./compile.sh
    ls *.so
    cd ..
done
