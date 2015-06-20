#!/usr/bin/env bash
#set -o verbose

soname=dc_controller_without_input.so

# gcc -c -Wall ./dc_controller_without_input.c
# Create SO
echo "gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC $args"
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC dc_controller_without_input.c

soname=dc_controller_with_input.so

# gcc -c -Wall ./dc_controller_with_input.c
# Create SO
echo "gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC $args"
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC dc_controller_with_input.c
