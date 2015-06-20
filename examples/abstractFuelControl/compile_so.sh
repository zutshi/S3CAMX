#!/usr/bin/env bash
set -o verbose

soname=controller.so
SOURCE=controller.c

# gcc -c -Wall ./$SOURCE
# Create SO
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC ./$SOURCE
