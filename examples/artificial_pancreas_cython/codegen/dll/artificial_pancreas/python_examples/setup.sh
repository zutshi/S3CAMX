#!/bin/bash
# setup.sh
# Make the "myext" Python Module ("myext.so")
CC="gcc"   \
CXX="g++"   \
CFLAGS="-I../ -I./"   \
LDFLAGS="-L /home/zutshi/work/RA/cpsVerification/HyCU/S3CAMX/master/examples/artificial_pancreas_cython/codegen/dll/artificial_pancreas/ "   \
    python setup.py build_ext --inplace

# DOES NOT TACK ON THE LIBRARY FOR SOME REASON: complains of missing
# symbols!
# DID it manually as follow
# g++ -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-Bsymbolic-functions -Wl,-z,relro -L./ -L./ -I../ -I./ build/temp.linux-x86_64-2.7/artificial_pancreas.o -o ./artificial_pancreas.so -L./ ../artificial_pancreas.so
