
#!/usr/bin/env bash
set -o verbose

soname=mrs_controller.so
SOURCE=mrs_controller.c

# gcc -c -Wall ./$SOURCE
# Create SO
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC ./$SOURCE
