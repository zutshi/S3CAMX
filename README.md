#S3CAMX: S3CAM + Symbolic Execution

S3CAM uses simulations and symboolic execution to find falsifications to safety properties of Hybrid Systems. Please refer to the below publications for details:

- Zutshi, Sankaranarayanan, Deshmukh, Jin.
        "Symbolic-Numeric Reachability Analysis of Closed-Loop Control Software"
        Proceedings of the 19th International Conference on Hybrid Systems: Computation and Control. ACM, 2016.


- Zutshi, Deshmukh, Sankaranarayanan, Kapinski.
        "Multiple shooting, cegar-based falsification for hybrid systems."
        Proceedings of the 14th International Conference on Embedded Software. ACM, 2014.

##Dependencies

### Needed to run S3CAMX
The S3CAMX package has several dependencies:

- Python 2.7.x and its packages: required to run S3CAMX.
				[https://www.python.org/downloads/]
- MATLAB R2015b (and Simulink): required to simulate systems which use Matlab based simulators: AFC.
				[http://www.mathworks.com/downloads/]
- Pathcrawler: Required to generate offline symbolic paths (for symbolic execution).
				[http://pathcrawler-online.com/doWelcome#about]
- Z3: Required for running symbolic execution of the controller (**included** in this distribution).
				[https://z3.codeplex.com/]
- S-Taliro 1.6: Needed to reproduce comparison results (**included** in the distribution)
				[https://sites.google.com/a/asu.edu/s-taliro/s-taliro]

##Installation
The installation was tested on 
- Ubuntu 12.04 and 14.04
- Python 2.7.9
- MATLAB R2015b
 
- Install Python 2.7.x
The Python build must be configured with the option --enable-shared.
This is not the case with the default Python installation found in both Ubuntu 12.04 and 14.04 and hence a different local installation is required. This is needed to interface Matlab with Python [Matlab -> Python], which is used to generate test results by S-Taliro on systems with simulators in Python.
For more details, refer to: [--enable-shared](https://www.mathworks.com/help/matlab/matlab_external/undefined-variable-py-or-function-py-command.html#buialof-65)<br><br>
e.g. if using [pyenv](https://github.com/yyuu/pyenv), then CONFIGURE\_OPTS must be set as below
`export CONFIGURE_OPTS='--enable-shared --enable-unicode=ucs4'`
before issuing
`pyenv install 2.7.x`

- Install pip using get-pip.py (**included**)
 				[https://bootstrap.pypa.io/get-pip.py]
`python get-pip.py`

- Python Packages
To install the packages along with their dependencies, execute the commands below (preferably in the same order).
	- scipy
	`sudo -H pip install scipy`
	- numpy
	`sudo apt-get install libatlas-base-dev gfortran`
	`sudo -H pip install numpy`
	- blessings
	`sudo -H pip install blessings`
	- networkx
	`sudo -H pip install networkx`
	- matplotlib
	`sudo apt-get install python-matplotlib` [tries to automatically resolve matplotlib's dependencies]
	`sudo -H pip install matplotlib`
	- tqdm
	`sudo -H pip install tqdm`
	- pyparsing
	`sudo -H pip install pyparsing`
	- sh
	`sudo -H pip install sh`

- Matlab R2015b or higher
> **Note:**
>  The version R2015b is required and earlier versions will not work due to missing features.

Requires the below toolboxes:
	- Simulink


Then in Matlab, specify the path of python: e.g. pyversion <path>/bin/python

~~sudo apt-get install python-pip python-dev build-essential~~


###matlabengineforpython [Python -> Matlab]
Refer: [Install MATLAB Engine for Python](https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html)
- matlab
- matlab/engine


## RUNNING S3CAMX

- To configure paths, please update
	- `set_path`
	- `startup.m`
- Start and share minimal Matlab session (optional):
	- Open a terminal and type
	`matlab& -nojvm -nodisplay -nosplash`
	- In Matlab, type the below to share the matlab engine
	`matlab.engine.shareEngine('<engine_name>')`

- To simulate a system run, use
`./secam.py -f <system path> -s <number of simulations>`

- To run S3CAM, use
`./secam.py -f <system path> -c`

- To run S3CAMX, use
`./secam.py -f <system path> -x pathcrawler -r trace -t tree`

- A shared Matlab engine can be provided as below.
`./secam.py -f <system path> [options] --meng <engine_name>`
This engine will be used to simulate systems which use Matlab simulators. If it is nto provided, a Matlab engine will be started. A shared engine is preferred as launching a new Matlab engine is time consuming.
