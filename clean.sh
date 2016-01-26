#!/bin/bash

echo 'deleting pyc and klee outputs'
echo 'delete? press ctrl-c to cancel'
ls *.pyc
read
rm *.pyc
echo 'delete? press ctrl-c to cancel'
ls klee-out-*
read
rm -rf klee-out-*
rm klee-last
#rm *.o
echo 'removing python byte code files: tstc, pyc, pyo...'
find ./|grep --color=never '\.tstc$'|xargs rm
find ./|grep --color=never '\.pyc$'|xargs rm
find ./|grep --color=never '\.pyo$'|xargs rm
