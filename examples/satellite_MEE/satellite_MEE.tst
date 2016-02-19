inf = float('inf')
# sampling time
delta_t = 50.0

# pvt simulator state required for initializing the simulator
plant_pvt_init_data = None

#############################
# P1: Property Description
#############################

# Time Horizon
T = 8000.0

# Rectangular bounds on initial plant states X0[0, :] <= X <= X0[1, :]
#initial_set = [[2000, 2000, 6000,-7,-2,3], [3000, 3000,6500,-6,-1,4]]

# violatins have been found for this
#initial_set = [[2730.12176, 2107.72809, 6280.01960, -6.79622541, -1.75317772, 3.88977028], [2730.12176, 2107.72809, 6280.01960, -6.79622541, -1.75317772, 3.88977028]]
#
# smaller set
#initial_set = [[2700, 2100, 6200, -7.0, -2.0, 3.5],
#               [2800, 2200, 6300, -6.5, -1.7, 4.0]]

# Cosmos 2251
initial_set = [[2689.06, 2726.88, 6049.935, -6.53545, -1.16479, 3.40109],
               [2689.06, 2726.88, 6049.935, -6.53545, -1.16479, 3.40109]]
# Unsafe Boxed Region
#error_set = [[1250,1350, 6500,-inf,-inf,-inf], [1750, 1850,7000,inf,inf,inf]]
error_set = [[0,0,0,0,0,0]*2] # Always false!

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
grid_eps = [25,25,25,0.2, 0.2, 0.2]
#grid_eps = [0.1]*6

# number of samples at every scatter step
num_samples = 1

# maximum iteration before SS iter outs.
MAX_ITER = 6

# minDist=0.05
########################

# Rectangularly bounded exogenous inputs to the plant (plant noise).
pi = [[0], [0]]

################################
# Unimplemented
################################
# Initial plant discrete state: List all states
initial_discrete_state = [0]
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
plant_path = 'satellite_MEE.m'

################
# DO NOT MODIFY
################
## controller params: PLEASE IGNORE

min_smt_sample_dist = 1
# relative/absolute path for the controller .so
controller_path = None
# relative path for the directory containing smt2 files for each path
controller_path_dir_path = None
# initial controller states which are C ints
initial_controller_integer_state = []

# initial controller states which are C doubles
initial_controller_float_state = []

# number of control inputs to the plant
num_control_inputs = 0

# rectangular bounds on exogenous inputs to the contorller. Such as, controller
# disturbance.
ci = [[0.0], [0.0]]
CONVERSION_FACTOR = 1.0
refinement_factor = 2.0
