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


# XXX: Have replaced infinity with 1000 because S-Taliro cribs like anything,
# and am not very confident passing it infinity!

# ********************
# P1: number of violations: 348
# time spent(s) = 1052.58428597
error_set = [[20.0], [1000.0]]
T = 50

# ********************
# P2: number of violations: 33
# time spent(s) = 3656.08513999
# error_set = [[50.0], [1000]]
# T = 200

# ********************
# P3: number of violations: 0
# time spent(s) =
# error_set = [[150.0], [1000.0]]
# T = 500

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

# number of samples at every scatter step
# SymEx
num_samples = 1
# SS
#num_samples = 10

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
