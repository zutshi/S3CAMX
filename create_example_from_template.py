#!/usr/bin/python
# -*- coding: utf-8 -*-

import fileOps as f
import sys
import err

plant_str = '''
# Must satisfy the signature
# [t,X,D,P] = sim_function(T,X0,D0,P0,I0);

import numpy as np
from scipy.integrate import ode

import matplotlib.pyplot as PLT


class SIM(object):
    def __init__(self, plt, pvt_init_data):
        pass

    def sim(self, TT, X0, D, P, U, I, property_checker, property_violated_flag):
        # atol = 1e-10
        rtol = 1e-5

        num_dim_x = len(X0)
        plot_data = [np.empty(0, dtype=float), np.empty((0, num_dim_x), dtype=float)]

        # tt,YY,dummy_D,dummy_P
        solver = ode(dyn).set_integrator('dopri5', rtol=rtol)

        Ti = TT[0]
        Tf = TT[1]
        T = Tf - Ti

        if property_checker:
            violating_state = [()]
            solver.set_solout(solout_fun(property_checker, violating_state, plot_data))  # (2)

        solver.set_initial_value(X0, t=0.0)
        solver.set_f_params(U)
        X_ = solver.integrate(T)

        if property_checker is not None:
            if property_checker(Tf, X_):
                property_violated_flag[0] = True

        dummy_D = np.zeros(D.shape)
        dummy_P = np.zeros(P.shape)
        ret_t = Tf
        ret_X = X_
        ret_D = dummy_D
        ret_P = dummy_P

        # TODO: plotting needs to be fixed
        #PLT.plot(plot_data[0] + Ti, plot_data[1][:, 0])
        #PLT.plot(plot_data[0] + Ti, plot_data[1][:, 1])
        #PLT.plot(plot_data[1][:, 0], plot_data[1][:, 1])
        ##PLT.plot(plot_data[0] + Ti, np.tile(U, plot_data[0].shape))

        return (ret_t, ret_X, ret_D, ret_P)


# State Space Modeling Template
# dx/dt = Ax + Bu
# y = Cx + Du
def dyn(t, x, u):
    #u = np.matrix([u[0], 0.0]).T
    #x = np.matrix(x).T
    #X_ = A*x + B*u
    #return np.array(X_.T)
    pass


def solout_fun(property_checker, violating_state, plot_data):

    def solout(t, Y):
        plot_data[0] = np.concatenate((plot_data[0], np.array([t])))
        plot_data[1] = np.concatenate((plot_data[1], np.array([Y])))
        return 0

    return solout
'''

tst_str = '''
# sampling time
delta_t = <0.0>

# pvt simulator state required for initializing the simulator
plant_pvt_init_data = None

#############################
# P1: Property Description
#############################

# Time Horizon
T = <0.0>

# Rectangular bounds on initial plant states X0[0, :] <= X <= X0[1, :]
initial_set = <[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]>

# Unsafe Boxed Region
error_set = <[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]>

# rectangular bounds on exogenous inputs to the contorller. Such as, controller
# disturbance.
ci = <[[0.0], [0.0]]>
############################

# Results Scratchpad:
# vio = _/100k took _ mins [plotting, logging?]
# SS = falsified in _ [plotting, logging?]
# grid_eps = <[0.0, 0.0]>
# num_samples = <2>
# SS + symex: falsified in _ [plotting, logging?]
########################
# Abstraction Params
########################
# initial abstraction grid size
grid_eps = <[0.0, 0.0, 0.0]>

# number of samples at every scatter step
num_samples = <0>

# maximum iteration before SS iter outs.
MAX_ITER = <0>

# minDist=0.05
########################

# initial controller states which are C ints
initial_controller_integer_state = <[0.0]>

# initial controller states which are C doubles
initial_controller_float_state = <[0.0]>

# number of control inputs to the plant
num_control_inputs = <0>

################################
# Unimplemented
################################
# Initial plant discrete state: List all states
initial_discrete_state = <[0]>
# Rectangularly bounded exogenous inputs to the plant (plant noise).
pi = [[], []]
# Initial pvt simulator state, associated with with an execution trace.
initial_pvt_states = []
################################

################
# Simulators
################
## Plant ##
# is the plant simulator implemented in Python(python) or Matlab(matlab)?
plant_description = <['python', 'matlab']>
# relative/absolute path for the simulator file containing sim()
plant_path = <['*.py', '*.m']>

## Controller ##
# relative/absolute path for the controller .so
controller_path = <'*.so'>
# relative path for the directory containing smt2 files for each path
controller_path_dir_path = './paths'
###############

################
# DO NOT MODIFY
################
CONVERSION_FACTOR = 1.0
refinement_factor = 2.0
'''

compile_script_str = '''
#!/usr/bin/env bash
set -o verbose

soname=<>.so
SOURCE=<>.c

# gcc -c -Wall ./$SOURCE
# Create SO
gcc -shared -Wl,-soname,$soname -o ./$soname -fPIC ./$SOURCE
#llvm-gcc -emit-llvm -c -g <>.c
'''

controller_h_str = '''
typedef struct{
    int* int_state_arr;
    double* float_state_arr;
    double* output_arr;
}RETURN_VAL;

typedef struct{
    double* input_arr;
    int* int_state_arr;
    double* float_state_arr;
    double* x_arr;
}INPUT_VAL;

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
void controller_init();
'''

controller_c_str = '''
#include "controller.h"

void controller_init(){
}

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
{
  _ = input->x_arr[];
  _ = input->float_state_arr[];
  _ = input->int_state_arr[];
  _ = input->input_arr[];

  ret_val->output_arr[] = _;
  ret_val->float_state_arr[] = _;
  ret_val->int_state_arr[] = _;

  return (void*)0;
}
'''

PC_DIR_PATH = './paths/pathcrawler'
KLEE_DIR_PATH = './paths/klee'
TST_FILE = '{}.tst'
PLANT_FILE = '{}_plant.py'
COMPILATION_SCRIPT = 'compile.sh'
CONTROLLER_H = 'controller.h'
CONTROLLER_C = '{}_controller.c'


def main():
    dir_path = f.sanitize_path(sys.argv[1])
    if f.file_exists(dir_path):
        print 'Failed: requested directory exists: {}'.format(dir_path)
        return
    if dir_path == '':
        raise err.Fatal('dir path empty!')
    dir_name = f.get_file_name_from_path(dir_path)
    f.make_n_change_dir(dir_path)
    f.write_data(TST_FILE.format(dir_name), tst_str)
    f.write_data(PLANT_FILE.format(dir_name), plant_str)
    f.write_data(COMPILATION_SCRIPT, compile_script_str)
    f.write_data(CONTROLLER_H, controller_h_str)
    f.write_data(CONTROLLER_C.format(dir_name), controller_c_str)
    f.make_dir(PC_DIR_PATH)

    # make compilation script executable
    f.make_exec(COMPILATION_SCRIPT)

if __name__ == '__main__':
    main()
