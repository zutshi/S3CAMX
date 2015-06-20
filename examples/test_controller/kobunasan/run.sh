/home/zutshi/work/KLEE/llvm-gcc4.2-2.9-x86_64-linux/bin/llvm-gcc -I ../../include --emit-llvm -c -g $1.c
/home/zutshi/work/KLEE/klee/Release+Asserts/bin/klee -smtlib-human-readable --write-pcs --use-query-log=all:pc --emit-all-errors $1.o
#cat ./klee-last/test*.smt2
 /home/zutshi/work/KLEE/klee/Release+Asserts/bin/ktest-tool --write-ints ./klee-last/test00000*.ktest
#./kleewrap.py --int-arr ./klee-last/test00000*.ktest
