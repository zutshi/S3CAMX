#!/usr/bin/env bash
#set -o verbose

soname=$1

# Check compilation
for arg in "${@:2}"
do
    gcc -g -c -Wall ./$arg.c
done

for arg in "${@:2}"
do
    newargs="$newargs $arg.c"
done
# Create SO
#echo "gcc -g -shared -Wl,-soname,$soname -o ./$soname.so -fPIC $newargs"
gcc -g -shared -Wl,-soname,$1 -o ./$1.so -fPIC $newargs
#gcc -g -shared -Wl,-soname,$1 -o ./$1.so -fPIC ./$1.c
