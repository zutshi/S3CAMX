#!/usr/bin/env bash
set -o verbose

soname=heater.so
SOURCE=heater.c

# gcc -c -Wall ./$SOURCE
# Create SO
gcc -Wall -shared -Wl,-soname,$soname -o ./$soname -fPIC ./$SOURCE
