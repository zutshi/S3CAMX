
#!/usr/bin/env bash
set -o verbose

soname=spi_controller.so
SOURCE=spi_controller.c

# gcc -c -Wall ./$SOURCE
# Create SO
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC ./$SOURCE
#llvm-gcc -emit-llvm -c -g <>.c
