
#!/usr/bin/env bash
set -o verbose

soname=heat_controller.so
SOURCE=heat_controller.c

#llvm-gcc -emit-llvm -c -g heat_controller.c

# gcc -c -Wall ./$SOURCE
# Create SO
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC ./$SOURCE
