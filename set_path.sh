
Z3_PATH=/home/zutshi/work/RA/cpsVerification/HyCU/z3_github/z3_installation/lib/python2.7/dist-packages
PY2Z3_PATH=/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/
CURR_PATH=$PWD

# bleeding edge github checkout
export PYTHONPATH+=:$Z3_PATH

export PYTHONPATH+=:$PY2Z3_PATH
export PYTHONPATH+=:$CURR_PATH/path_crawler_helpers/
