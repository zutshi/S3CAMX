
Z3_PATH=/home/re/RE_secam/z3_libs/
PY2Z3_PATH=/home/re/RE_secam/
CURR_PATH=$PWD

# bleeding edge github checkout
export PYTHONPATH+=:$Z3_PATH

export PYTHONPATH+=:$PY2Z3_PATH
export PYTHONPATH+=:$CURR_PATH/path_crawler_helpers/
