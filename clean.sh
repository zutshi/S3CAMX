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
echo 'removing tstc files too...'
# remove compiled py and tst files with extension: pyc, tstc
find ./|grep --color=never '\.tstc$'|xargs -r rm
find ./|grep --color=never '\.pyc$'|xargs rm
echo 'removing pyo files...'
# remove compiled tst files with extension: tstc
find ./|grep --color=never '\.pyo$'|xargs -r rm
