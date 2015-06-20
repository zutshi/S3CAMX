#!/usr/bin/env bash
set -o verbose

# Create SO
gcc -shared -Wl,-soname,csim_test_controller -o ./csim_test_controller.so -fPIC ./csim_test_controller.c
