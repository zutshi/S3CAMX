inf = float('inf')
# sampling time
delta_t = 1.0

# pvt simulator state required for initializing the simulator
plant_pvt_init_data = None

#############################
# P1: Property Description
#############################


# Rectangular bounds on initial plant states X0[0, :] <= X <= X0[1, :]
initial_set = [[0.0],[0.0]]
# Unsafe Boxed Region
error_set = [[20.0], [inf]]
#error_set = [[2], [3]]
# Time Horizon
T = 50

#T = 200
#error_set = [[50.0], [inf]]
#T = 500
#error_set = [[150.0], [inf]]

# rectangular bounds on exogenous inputs to the contorller. Such as, controller
# disturbance.
ci = [[-1.0], [1.0]]
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
grid_eps = [0.5]
pi_grid_eps = []

# number of samples at every scatter step
num_samples = 10

# maximum iteration before SS iter outs.
MAX_ITER = 10
min_smt_sample_dist = 0.5
# minDist=0.05
########################

# initial controller states which are C ints
initial_controller_integer_state = []

# initial controller states which are C doubles
initial_controller_float_state = []

# number of control inputs to the plant
num_control_inputs = 1

################################
# Unimplemented
################################
# Initial plant discrete state: List all states
initial_discrete_state = [0]
# Rectangularly bounded exogenous inputs to the plant (plant noise).
pi = [[],[]]
#pi = [[0.0, 0.0], [1.0, 1.0]]
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
plant_path = 'spi_plant.py'

## Controller ##
# relative/absolute path for the controller .so
controller_path = 'spi_controller.so'
# relative path for the directory containing smt2 files for each path
controller_path_dir_path = './paths'
###############

################
# DO NOT MODIFY
################
CONVERSION_FACTOR = 1.0
refinement_factor = 2.0
