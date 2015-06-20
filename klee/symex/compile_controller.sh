#!/usr/bin/env bash
set -o verbose

# Check compilation
gcc -c -Wall ./$1.c

# Create SO
gcc -shared -Wl,-soname,$1 -o ./$1.so -fPIC ./$1.c
