#!/usr/bin/env bash
set -o verbose

soname=afc.so
SOURCE=afc.c

# gcc -c -Wall ./$SOURCE
# Create SO
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC ./$SOURCE
#llvm-gcc -emit-llvm -c -g controller.c
