#!/bin/bash

INCLUDES=/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/klee/klee/include/

/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/klee/llvm-gcc4.2-2.9-x86_64-linux/bin/llvm-gcc -I $INCLUDES --emit-llvm -c -g ./continuous_kobuna_FP.c 
/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/klee/llvm-gcc4.2-2.9-x86_64-linux/bin/llvm-gcc -I $INCLUDES --emit-llvm -c -g ./ert_main.c
/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/klee/llvm-gcc4.2-2.9-x86_64-linux/bin/llvm-gcc -I $INCLUDES --emit-llvm -c -g ./demo_controller.c

/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/klee/llvm-2.9/Release+Asserts/bin/llvm-ld -r ./demo_controller.o ert_main.o continuous_kobuna_FP.o -o kobunasan.o

/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/klee/klee/Release+Asserts/bin/klee -smtlib-human-readable --write-pcs --use-query-log=all:pc ./kobunasan.o #--emit-all-errors ./kobunasan.o 

# -const-array-op -optimizet
./kleewrap.py --int-arr ./klee-last/test*.ktest
