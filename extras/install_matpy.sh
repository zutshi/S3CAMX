mex -v py.cpp -I/usr/include/python2.7 '-L/usr/lib/python2.7/config-x86_64-linux-gnu -lpython2.7 -Xlinker -export-dynamic'


mex py.cpp -g -v -I/usr/include/python2.7 -DLIBPYTHON=-L/usr/lib/python2.7/config-x86_64-linux-gnu/libpython2.7.so -lpython2.7 -ldl LDFLAGS='\$LDFLAGS -Xlinker -export-dynamic' -compatibleArrayDims











## doesnt work, but would want to make it work

g++ -c  -I/usr/include/python2.7 -I/home/zutshi/MATLAB/extern/include -I/home/zutshi/MATLAB/simulink/include -DMATLAB_MEX_FILE -ansi -D_GNU_SOURCE -fPIC -fno-omit-frame-pointer -pthread  -DLIBPYTHON=/usr/lib/python2.7/config-x86_64-linux-gnu/libpython2.7.so -DMX_COMPAT_32 -g  "py.cpp"

g++ -g -Xlinker -export-dynamic -o  "py.mexa64"  py.o  -L/usr/lib -lpython2.7 -ldl -Wl,-rpath-link,/home/zutshi/MATLAB/bin/glnxa64 -L/home/zutshi/MATLAB/bin/glnxa64 -lmx -lmex -lmat -lm

# does work
g++ -c  -I/usr/include/python2.7 -I/home/zutshi/MATLAB/extern/include -I/home/zutshi/MATLAB/simulink/include -DMATLAB_MEX_FILE -ansi -D_GNU_SOURCE -fPIC -fno-omit-frame-pointer -pthread  -DMX_COMPAT_32 -O -DNDEBUG  "py.cpp"

g++ -O -pthread -shared -Wl,--version-script,/home/zutshi/MATLAB/extern/lib/glnxa64/mexFunction.map -Wl,--no-undefined -Xlinker -export-dynamic -o  "py.mexa64"  py.o  -L/usr/lib/python2.7/config-x86_64-linux-gnu -lpython2.7 -Xlinker -export-dynamic -Wl,-rpath-link,/home/zutshi/MATLAB/bin/glnxa64 -L/home/zutshi/MATLAB/bin/glnxa64 -lmx -lmex -lmat -lm

## proposed

g++ -c  -I/usr/include/python2.7 -I/home/zutshi/MATLAB/extern/include -I/home/zutshi/MATLAB/simulink/include -DMATLAB_MEX_FILE -ansi -D_GNU_SOURCE -fPIC -fno-omit-frame-pointer -pthread -DLIBPYTHON=/usr/lib/python2.7/config-x86_64-linux-gnu/libpython2.7.so -DMX_COMPAT_32 -O -DNDEBUG  "py.cpp"

g++ -O -pthread -shared -Wl,--version-script,/home/zutshi/MATLAB/extern/lib/glnxa64/mexFunction.map -Wl,--no-undefined -Xlinker -export-dynamic -o  "py.mexa64"  py.o  -L/usr/lib/python2.7/config-x86_64-linux-gnu -lpython2.7 -Xlinker -export-dynamic -ldl -Wl,-rpath-link,/home/zutshi/MATLAB/bin/glnxa64 -L/home/zutshi/MATLAB/bin/glnxa64 -lmx -lmex -lmat -lm

