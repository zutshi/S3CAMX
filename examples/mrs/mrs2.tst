import toy_instance

# sampling time
delta_t = 1.0

#benchmark_id = int(raw_input('Enter toy benchmark id: '))
benchmark_id = 2

# pvt simulator state required for initializing the simulator
plant_pvt_init_data = benchmark_id

#############################
# P1: Property Description
#############################

# Time Horizon
T = 2.0

initial_set, error_set, ci = toy_instance.select(benchmark_id)

############################
# Results Scratchpad:
# ##########################
# vio = _/100k took _ mins [plotting, logging?]
# SS = falsified in _ [plotting, logging?]
# grid_eps = <[0.0, 0.0]>
# num_samples = <2>
# SS + symex: falsified in _ [plotting, logging?]
########################
# Abstraction Params
########################
# initial abstraction grid size
grid_eps = [1.0, 1.0, 1.0, 1.0]

# number of samples at every scatter step
#num_samples = 5
num_samples = 1

# maximum iteration before SS iter outs.
MAX_ITER = 5

min_smt_sample_dist = 0.05
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
initial_discrete_state = []
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
plant_description = 'python' 
# relative/absolute path for the simulator file containing sim()
plant_path = 'toy_model_10u_plant.py' 

## Controller ##
# relative/absolute path for the controller .so
controller_path = 'toy_model_10u_controller.so'
# relative path for the directory containing smt2 files for each path
controller_path_dir_path = './paths'
###############

################
# DO NOT MODIFY
################
CONVERSION_FACTOR = 1.0
refinement_factor = 2.0
