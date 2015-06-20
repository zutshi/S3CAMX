llvm-gcc -I ../../include --emit-llvm -c -g $1.c
klee -smtlib-human-readable --write-pcs --use-query-log=all:pc $1.o
#cat ./klee-last/test*.smt2
ktest-tool --write-ints ./klee-last/test00000*.ktest
