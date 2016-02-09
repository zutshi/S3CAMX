inf = float('inf')

# sampling time
delta_t = 10.0

# pvt simulator state required for initializing the simulator
plant_pvt_init_data = None

#############################
# P1: Property Description
#############################

# Time Horizon
T = 720.0

# Rectangular bounds on initial plant states X0[0, :] <= X <= X0[1, :]
# [gValues gsValues iValues]
initial_set = [[80.0, 90.0, 0.0], [160.0, 150.0, 1.0]]

# Unsafe Boxed Region
error_set = [[0, -inf, -inf], [70, inf, inf]]

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
grid_eps = [50.0, 50.0, 50.0]


# number of samples at every scatter step
num_samples = 2

# maximum iteration before SS iter outs.
MAX_ITER = 2

# minDist=0.05
########################

# Rectangularly bounded exogenous inputs to the plant (plant noise).
pi = [[-20.0], [20.0]]
pi_grid_eps = [5.0]


################################
# Unimplemented
################################
# Initial plant discrete state: List all states
# [TotalTime, TimeElapsed, ControllerStartTime, DallaMan_curState(:,1:10), isPIDInitialized, PID_ctrlState[10x1 stct]]
initial_discrete_state = [T, 0.0, 40.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
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
plant_path = 'artificial_pancreas.m'

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
ci = [[], []]
<<<<<<< HEAD
=======
ci_grid_eps = []
>>>>>>> 45f97683ef34877111e50a2386fc37a4aab85418
