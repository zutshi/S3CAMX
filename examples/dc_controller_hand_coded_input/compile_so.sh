#!/usr/bin/env bash
set -o verbose

soname=dc_controller_with_input.so
SOURCE=dc_controller_with_input.c

# gcc -c -Wall ./$SOURCE
# Create SO
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC ./$SOURCE
