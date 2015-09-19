
#!/usr/bin/env bash
set -o verbose

soname=autotrans_controller.so
SOURCE='shift_controller.c autotrans_controller.c'

# gcc -c -Wall ./$SOURCE
# Create SO
gcc -Wall -shared -Wl,-soname,$soname -o ./$soname -fPIC $SOURCE 
