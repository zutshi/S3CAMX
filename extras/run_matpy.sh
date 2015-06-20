# To compile, use
mex -g -v py.cpp -I/usr/include/python2.7 -L/usr/lib -DLIBPYTHON=/usr/lib/python2.7/config/libpython2.7.so '-lpython2.7 -ldl -Xlinker -export-dynamic' -compatibleArrayDims


#To run use

export FFTW_VERSION=/usr/lib/libfftw3.so.3
export BLAS_VERSION=/usr/lib/libblas.so.3gf
export LAPACK_VERSION=/usr/lib/lapack/liblapack.so.3gf
export LAPACK_VERBOSITY=1

LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6:/lib/x86_64-linux-gnu/libgcc_s.so.1:/usr/lib/x86_64-linux-gnu/libgfortran.so.3:/usr/lib/libblas/libblas.so.3gf:/usr/lib/liblapack.so.3gf matlab -nodisplay -nodesktop

#LD_PRELOAD=/home/zutshi/MATLAB/R2013a/sys/os/glnxa64/libstdc++.so.6:/home/zutshi/MATLAB/R2013a/sys/os/glnxa64/libgcc_s.so.1:/home/zutshi/MATLAB/R2013a/sys/os/glnxa64/libgfortran.so.3:/usr/lib/libblas/libblas.so.3gf:/usr/lib/liblapack.so.3gf matlab -nodisplay -nodesktop



