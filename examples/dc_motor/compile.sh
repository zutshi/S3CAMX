#!/usr/bin/env bash
set -o verbose

soname=dc_motor_controller.so
SOURCE=dc_motor_controller.c

# gcc -c -Wall ./$SOURCE
# Create SO
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC ./$SOURCE

#llvm-gcc -emit-llvm -c -g dc_controller_with_input.c
