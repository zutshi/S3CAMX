
#!/usr/bin/env bash
set -o verbose

soname=autotrans_controller.so
SOURCE=autotrans_controller.c

# gcc -c -Wall ./$SOURCE
# Create SO
gcc -c shift_controller.c -fPIC
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC ./shift_controller.c ./$SOURCE 
