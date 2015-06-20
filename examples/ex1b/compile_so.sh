#!/usr/bin/env bash
set -o verbose

soname=ex1b_controller.so
SOURCE=ex1b_controller.c

# Create SO
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC ./$SOURCE
