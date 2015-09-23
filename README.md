S3CAMX:

Falsification of closed loop control systems:
  S3CAM + Symbolic Execution

This release is meant to be accompanied by a conference publication.

Dependencies

#Manual install

-python 2.7x

Refer: https://www.mathworks.com/help/matlab/matlab_external/undefined-variable-py-or-function-py-command.html#buialof-67

The python distribution must be compiled with 
./configure --enable-shared 
and if using pyenv, https://github.com/yyuu/pyenv, then must set 
export CONFIGURE_OPTS='--enable-shared --enable-unicode=ucs4'
before issuing
pyenv install 2.7.3


-z3py [optional, required for symex] 
  from https://github.com/Z3Prover/z3

-graph-tool  [optional, will replace networkx in the future]
  Takes very very long to compile: 4+ hrs
  Requires recent version of boost
  All in all, time consuming


#Python Packages
use pip install <...>

-scipy
-numpy
-blessings
-networkx
-matplotlib
-tqdm.py
-pyparsing.py

#matlabengineforpython [Python -> Matlab]

-matlab
-matlab/engine

