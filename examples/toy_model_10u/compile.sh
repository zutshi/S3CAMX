
#!/usr/bin/env bash
set -o verbose

soname=toy_model_10u_controller.so
SOURCE=toy_model_10u_controller.c

# gcc -c -Wall ./$SOURCE
# Create SO
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC ./$SOURCE
