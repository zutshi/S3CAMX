#!/bin/bash

cd ./examples
for d in *
do
    cd $d
    dir_name=${PWD##*/}
    echo "Compiling $dir_name..."
    ./compile.sh
    ls *.so
    tar -xf ./paths/controller.pickled.tar.gz -C ./paths/
    tar -xf ./paths/controller.tar.gz -C ./paths/
    cd ..
done
