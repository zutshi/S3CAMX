#S3CAMX: S3CAM + Symbolic Execution

This release is meant to be accompanied by a conference publication.

##Dependencies

###Requires Manual install

- python 2.7x

Required for Matlab -> Python interface used to generate test results by S-Taliro
Refer: [enable shared](https://www.mathworks.com/help/matlab/matlab_external/undefined-variable-py-or-function-py-command.html#buialof-67)

The python distribution must be compiled with 
./configure --enable-shared 
and if using [pyenv](https://github.com/yyuu/pyenv), then must set 
export CONFIGURE\_OPTS='--enable-shared --enable-unicode=ucs4'
before issuing
pyenv install 2.7.3

Then in Matlab, specify the path of python: e.g. pyversion <path>/bin/python


- z3py [optional, required for symex] 
  from https://github.com/Z3Prover/z3

- graph-tool  [optional, will replace networkx in the future]
  Takes very very long to compile: 4+ hrs
  Requires recent version of boost
  All in all, time consuming


###Python Packages
install [pip](https://bootstrap.pypa.io/get-pip.py)

Required Python Packages:
- scipy
- numpy
- blessings
- networkx
- matplotlib
- tqdm
- pyparsing

To install the packages along with their dependencies, execute the commands below (preferably in the same order).
sudo apt-get install python-pip python-dev build-essential
sudo pip install numpy
sudo apt-get install libatlas-base-dev gfortran
sudo pip install scipy
sudo pip install blessings
sudo pip install matplotlib
(
Note: 
If the matplotlib installation throws an error because of missing dependencies, try this:
sudo apt-get install python-matplotlib
sudo pip install matplotlib
)
sudo pip install networkx
sudo pip install tqdm
sudo pip install pyparsing


###matlabengineforpython [Python -> Matlab]
Refer: [Install MATLAB Engine for Python](https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html)
- matlab
- matlab/engine


##Update Local Paths

- update set\_path
- update startup.m
