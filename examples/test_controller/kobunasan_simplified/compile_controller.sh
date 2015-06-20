#!/usr/bin/env bash
#set -o verbose

soname=test_controller.so

# Check compilation
for arg in "$@"
do
    gcc -c -Wall ./$arg.c
done

for arg in "$@"
do
    newargs="$newargs $arg.c"
done
# Create SO
echo "gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC $newargs"
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC $newargs
