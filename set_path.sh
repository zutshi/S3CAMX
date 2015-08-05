
Z3_PATH=/home/zutshi/work/RA/cpsVerification/HyCU/z3_github/z3_installation/lib/python2.7/dist-packages
PY2Z3_PATH=/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/
CURR_PATH=/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/branches/RB-0.75

#export PATH+=:/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/klee/llvm-gcc4.2-2.9-x86_64-linux/bin/
#export PATH+=:/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/klee/llvm-2.9/Release+Asserts/bin/
#export PATH+=:/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/klee/klee/Release+Asserts/bin/
#export PYTHONPATH=/home/zutshi/work/RA/cpsVerification/HyCU/z3-4.3.2.70192b66e931-x64-ubuntu-12.04/bin/

# stable z3 version? Being used currently
#export PYTHONPATH+=:/home/zutshi/work/RA/cpsVerification/HyCU/z3-cee7dd39444c9060186df79c2a2c7f8845de415b/build

# bleeding edge github checkout
export PYTHONPATH+=:$Z3_PATH

export PYTHONPATH+=:$PY2Z3_PATH
export PYTHONPATH+=:$CURR_PATH/path_crawler_helpers/
