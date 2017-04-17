
#!/usr/bin/env bash
set -o verbose

soname=caratk.so
SOURCE=caratk.c

# Create SO
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC ./$SOURCE
