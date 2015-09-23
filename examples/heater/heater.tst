# minDist=10

delta_t = 0.2

plant_pvt_init_data = None

##### NOTES
#initial_set = [[69.0], [71.0]] #actually its 69.9 to 70?
#initial_set = [[68.0], [69.0]]
# initial_set = [[67.0], [70.0]] #Results in 2 distinct periodic orbits


#################################
# P1
#################################
# SS solves it with grid eps = 0.1, and num_samples = 5 in 15s!
# num vio = 120/100k in 4m
# grid_eps = 5
# num_samples = 5
min_smt_sample_dist  = 1
initial_set = [[55.0], [75.0]]
#error_set = [[0.0], [52.0]]
error_set = [[76.0], [500]]
T = 2
# SS + SymEx takes 30s
#P1 = (initial_set, error_set, T)

## Used for SS + SymEx
grid_eps = [5.0]
num_samples = 5

## Used for SS
#grid_eps = [0.1]
#num_samples = 5


#################################
# P2
#################################
# SS solves it with grid eps = 0.1, num_samples = 5 in 12s!!
# num vio = 38/100k in 5min
# SS + SymEX
#refinement_factor = 2.0
#grid_eps = [0.1]
#num_samples = 5
#delta_t = 0.2
# midist = 1
#initial_set = [[55.0], [75.0]]
#error_set = [[76.0], [100.0]]
#T = 2

# concrete run
# grid_eps = 5
# num_samples = 2


#P2 = (initial_set, error_set, T)

#properties = {'P0':P0,
#              'P1':P1,
#              'P2':P2,
#              }


##################################
# P2 NOT DONE YET...but with grid eps = 1, and max_hd = 2, should work
#initial_set = [[55.0], [75.0]]
#initial_set = [[65.0], [70.0]]
#error_set = [[76.0], [200.0]]

initial_discrete_state = [0]

# chatter_detect, previous_command_to_heater, on_counter, off_counter
initial_controller_integer_state = [0, 0, 0, 0]
initial_controller_float_state = []

num_control_inputs = 1

#num_controller_integer_states = 4
#num_controller_float_states = 0
#num_plant_states = 1
#num_conrtoller_disturbances = 1
#num_plant_disturbances = 0
#num_plant_discrete_states = 1
#num_reference_signals = 1
#num_pvt_sim_states = 1

# Reference signal \in [0.0, 4.0]
# Disturbances ... add later
#ci = [[-0.5], [-0.0]]
ci = [[0.0], [-0.0]]
#.65
#.6
pi = [[],[]]

MAX_ITER = 10

################
# Simulators
################
# Plant
plant_description = 'python'
plant_path = 'heater.py'
# Controller
controller_path = './heater.so'
controller_path_dir_path = './paths'

################
# Abstraction
################

#refinement_factor = 2.0
#grid_eps = [0.1]
#num_samples = 5
###midist = 3
##############################
#refinement_factor = 2.0
#grid_eps = 5
#num_samples = 5
refinement_factor = 2.0

CONVERSION_FACTOR = 1.0
