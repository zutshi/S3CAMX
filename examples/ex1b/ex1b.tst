# CONVERSION_FACTOR = 1000

MODE = 'falsify'
#METHOD = 'concolic'
METHOD = 'symbolic'
#METHOD = 'concrete'

initial_set = [[0.0], [2.0]]   # property should be sat with 0.6 <= x0 <= 0.6

error_set = [[-10.0], [0.0]]    # x becomes negative

initial_discrete_state = []

initial_controller_state = [0]

T = 2.0


controller = './ex1b_controller'
CONVERSION_FACTOR = 1000.0

num_controller_states = 1
num_plant_states = 1
num_control_inputs = 1
num_conrtoller_disturbances = 1
num_plant_disturbances = 1
num_plant_discrete_states = 0
num_reference_signals = 0
num_pvt_sim_states = 0

ci = [[-0.0],[0.0]]
pi = [[0.0],[0.0]]

controller_path_dir_path = './paths'

MAX_ITER = 80
