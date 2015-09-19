
delta_t = 0.02


plant_pvt_init_data = None

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
T = 1.0
initial_set = [[-0.0, -0.0], [0.0, 0.0]]
ci = [[-0.5], [-0.0]]
error_set = [[1.0, 10.0], [1.2, 11.0]]
# vio = 0/100k took 45 mins without plotting
# symex: falsified in ~2m with/without plotting
#   took only one iter
#   needs 2 samples! takes around 92s with and 51s w/o plotting and logging
grid_eps = [0.1, 0.1]
min_smt_sample_dist = 0.05
#num_samples = 2 #symex
num_samples = 2 #concrete
# ss: pending...

# error_set = [[1.2, 10], [1.3, 11]] #nahi ho raha! BUT random testing results havent
#confirmed if falsification exist


initial_discrete_state = [0]

initial_controller_integer_state = []
initial_controller_float_state = [0.0]

num_control_inputs = 1

# Reference signal \in [0.0, 4.0]
# Disturbances ... add later
#ci = [[-0.5], [-0.0]]
#.65
#.6
pi = [[],[]]

MAX_ITER = 6
################
# Simulators
################
# Plant
plant_description = 'python'
plant_path = 'dc_motor.py'
# Controller
controller_path = './dc_motor_controller.so'
controller_path_dir_path = './paths'
# Conversion
CONVERSION_FACTOR = 1.0

refinement_factor = 2.0
