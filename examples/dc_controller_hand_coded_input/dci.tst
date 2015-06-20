
# minDist=10

MODE = 'falsify'
METHOD = 'symbolic'
#METHOD = 'concrete'
#symbolic_analyzer = 'klee'
symbolic_analyzer = 'pathcrawler'

#MODE = 'simulate'
num_sim_samples = 100000

delta_t = 0.02
plot = True

#error_set = [[0.9, 5.5], [1.2, 10.5]]
#error_set = [[1.0, 5.5], [1.4, 10.5]]
#easy
#error_set = [[0.9, 8.0], [1.4, 14.0]]

#
# P1
# vio = 
#error_set = [[1.50, 8.0], [2.0, 20.0]]
# grid settings: 

# P2
# vio = 4/1000
# error_set = [[1.5, 8.0], [2.0, 16.0]]
# grid settings: 

# P3: few mins, 1 iter
# vio = 7/1000
# error_set = [[1.45, 8.0], [2.0, 16.0]]
# grid settings: 

#tmp prop P4, T = 0.8 [time with plotting = 22m]
# grid_eps = 0.01, 0.01
#vio = 132/1000 [time without plotting = 2m]
#T = 1.0
#initial_set = [[-0.0, -0.0], [0.0, 0.0]]
#error_set = [[1.5, -100], [2.0, 100]]

#####tmp prop P4, T = 0.8 [time with plotting = 22m]
###### grid_eps = 0.01, 0.01
#######vio = /1000 [time without plotting = 2m]
#######T = 1.0
#######initial_set = [[-0.0, -0.0], [0.0, 0.0]]
#######error_set = [[1.5, -100], [2.0, 100]]
######## ci = [[-0.5], [-0.0]]
# took 10 mins to violate with plotting on
# but 96/100 vio :(

# P5
# falsified in ~2m with/without plotting
# vio = 0/100k took 45 mins without plotting
T = 1.0
initial_set = [[-0.0, -0.0], [0.0, 0.0]]
error_set = [[1.0, 10], [1.2, 11]]
# error_set = [[1.2, 10], [1.3, 11]] #nahi ho raha! BUT random testing results havent
#confirmed if falsification exist
ci = [[-0.5], [-0.0]]

################
# Abstraction
################
#grid_eps = 0.01, 0.05
grid_eps = [0.01, 0.01]
refinement_factor = 2.0
num_samples = 1



initial_discrete_state = [0]

initial_controller_state = [0.0]


num_controller_states = 1
num_plant_states = 2
num_control_inputs = 1
num_conrtoller_disturbances = 1
num_plant_disturbances = 0
num_plant_discrete_states = 1
num_reference_signals = 1
num_pvt_sim_states = 1

# Reference signal \in [0.0, 4.0]
# Disturbances ... add later
#ci = [[-0.5], [-0.0]]
#.65
#.6
pi = []

MAX_ITER = 10


MAX_ITER = 6
################
# Simulators
################
# Plant
plant_description = 'native'
plant_path = 'dc_motor.py'
# Controller
controller = './dc_controller_with_input'
controller_path_dir_path = './paths'
# Conversion
CONVERSION_FACTOR = 1000.0

