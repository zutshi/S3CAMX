
# sampling time
delta_t = 0.1

# pvt simulator state required for initializing the simulator
plant_pvt_init_data = None

#############################
# P1: Property Description
#############################

# Time Horizon
T = 2.0

# sys_k = [x_k, d_k, pvt_k, ci_k, pi_k]
plant_composition = [[2,1,0,1,1],[2,1,0,1,1]]

# Rectangular bounds on initial plant states X0[0, :] <= X <= X0[1, :]
initial_set = [[0.0, 0.0, 2.0, 2.0], [1.0, 1.0, 3.0, 3.0]]

# Unsafe Boxed Region
error_set = [[2.0, 2.0, 4.0, 4.0], [3.0, 3.0, 5.0, 5.0]]

# rectangular bounds on exogenous inputs to the contorller. Such as, controller
# disturbance.
ci = [[1,2],[1,2]]
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
grid_eps = [.1, .2, .1, .2]
ci_grid_eps = [1, 2]
pi_grid_eps = [1, 2]

# number of samples at every scatter step
num_samples = 1

# maximum iteration before SS iter outs.
MAX_ITER = 5

min_smt_sample_dist = 0.5
########################

# initial controller states which are C ints
initial_controller_integer_state = []

# initial controller states which are C doubles
initial_controller_float_state = []

# number of control inputs to the plant
num_control_inputs = 0

################################
# Unimplemented
################################
# Initial plant discrete state: List all states
initial_discrete_state = [0,0]
# Rectangularly bounded exogenous inputs to the plant (plant noise).
pi = [[1,2], [1,2]]
# Initial pvt simulator state, associated with with an execution trace.
initial_pvt_states = []
################################

################
# Simulators
################
## Plant ##
# is the plant simulator implemented in Python(python) or Matlab(matlab)?
plant_description = 'python'
# relative/absolute path for the simulator file containing sim()
plant_path = 'param_sys_plant.py'
property_checker_path = 'check_prop.py'

## Controller ##
# relative/absolute path for the controller .so
controller_path = None
# relative path for the directory containing smt2 files for each path
controller_path_dir_path = None
###############
