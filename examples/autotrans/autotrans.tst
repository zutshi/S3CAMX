inf = float('inf')

# sampling time
delta_t = 1.0

# pvt simulator state required for initializing the simulator
plant_pvt_init_data = None

#############################
# P1: Property Description
#############################

# Time Horizon
T = 30.0

# Rectangular bounds on initial plant states X0[0, :] <= X <= X0[1, :]
# [plant outputs, plant states]
# vehicle speed[output], wheel speed, engine rpm
initial_set = [[0.0, 10.0, 1000.0], [0.0, 10.0, 1000.0]]

# Unsafe Boxed Region
error_set = [[-inf, -inf, 3000.0], [inf, inf, 4000.0]]

# rectangular bounds on exogenous inputs to the contorller. Such as, controller
# disturbance: Throttle, Brake Torque
ci = [[0.0, 0.0],[100.0, 300]]
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
grid_eps = [100.0, 5.0, 1000.0]
min_smt_sample_dist = 1.0;

# number of samples at every scatter step
num_samples = 1

# maximum iteration before SS iter outs.
MAX_ITER = 5

# minDist=0.05
########################

# initial controller states which are C ints
# temporalCounter_i1, is_active_c1_shift_controller, is_gear_state, is_active_gear_state,
# is_selection_state, is_active_selection_state
initial_controller_integer_state = [0]*6

# initial controller states which are C doubles
# disturbance[0], disturbance[1], Gear
initial_controller_float_state = [0.0]*3

# number of control inputs to the plant
num_control_inputs = 3

################################
# Unimplemented
################################
# Initial plant discrete state: List all states
initial_discrete_state = [0]
# Rectangularly bounded exogenous inputs to the plant (plant noise).
pi = [[],[]]
# Initial pvt simulator state, associated with with an execution trace.
initial_pvt_states = []
################################

################
# Simulators
################
## Plant ##
# is the plant simulator implemented in Python(python) or Matlab(matlab)?
plant_description = 'matlab'
# relative/absolute path for the simulator file containing sim()
plant_path = 'plant.m'

## Controller ##
# relative/absolute path for the controller .so
controller_path = 'autotrans_controller.so'
# relative path for the directory containing smt2 files for each path
controller_path_dir_path = './paths'
###############

################
# DO NOT MODIFY
################
#CONVERSION_FACTOR = 1.0
refinement_factor = 2.0
