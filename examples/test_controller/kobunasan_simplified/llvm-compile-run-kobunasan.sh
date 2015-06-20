#!/bin/bash

# Toyota...
#INCLUDES=/home/zutshi/work/KLEE/klee/include
#CC=/home/zutshi/work/KLEE/llvm-gcc4.2-2.9-x86_64-linux/bin/llvm-gcc
#LD=/home/zutshi/work/KLEE/llvm-2.9/Release+Asserts/bin/llvm-ld
#KLEE=/home/zutshi/work/KLEE/klee/Release+Asserts/bin/klee
#KLEEWRAP=/home/zutshi/work/cpsVerification/HyCU/symbSplicing/splicing/kleewrap.py

# Personal Laptop
#INCLUDES=/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/klee/klee/include/
#CC=/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/klee/llvm-gcc4.2-2.9-x86_64-linux/bin/llvm-gcc
#LD=/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/klee/llvm-2.9/Release+Asserts/bin/llvm-ld
#KLEE=/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/klee/klee/Release+Asserts/bin/klee
#KLEEWRAP=/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/kleewrap.py

# Global
INCLUDES=/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/klee/klee/include/
CC=llvm-gcc
LD=llvm-ld
KLEE=klee
KLEEWRAP=../../../kleewrap.py

$CC -I $INCLUDES --emit-llvm -c -g ./continuous_kobuna_simpleFP.c
$CC -I $INCLUDES --emit-llvm -c -g ./ert_main.c
$CC -I $INCLUDES --emit-llvm -c -g ./demo_controller.c

$LD -r ./demo_controller.o ert_main.o continuous_kobuna_simpleFP.o -o kobunasan.o
$LD -r ert_main.o continuous_kobuna_simpleFP.o -o test_controller.o

$KLEE -smtlib-human-readable --write-pcs --use-query-log=all:pc --emit-all-errors ./kobunasan.o
# -const-array-op -optimizet
$KLEEWRAP --int-arr ./klee-last/test*.ktest
