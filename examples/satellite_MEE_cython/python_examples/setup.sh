#!/bin/bash
# setup.sh
# Make the "myext" Python Module ("myext.so")
CC="gcc"   \
CXX="g++"   \
CFLAGS="-I/home/zutshi/work/RA/cpsVerification/HyCU/S3CAMX/parameteric/examples/satellite_MEE_cython/codegen/dll/satellite_MEE -I./"   \
LDFLAGS="-L/home/zutshi/work/RA/cpsVerification/HyCU/S3CAMX/parameteric/examples/satellite_MEE_cython/codegen/dll/satellite_MEE/ "   \
    python setup.py build_ext --inplace
