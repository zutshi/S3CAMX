MODE = 'falsify'
#METHOD = 'concrete'
METHOD = 'symbolic'

#MODE = 'simulate'
#num_sim_samples = 100000

delta_t = 0.01

# ideal X0
# initial_set = [[-0.1, -0.1, 0.0], [0.1, 0.1, 0.0]]
# hardest
#error_set = [[-1., -0.6, 5.40], [1., 0.6, 5.45]]

# smaller X0
#initial_set = [[-0., -0., 0.0], [0.1, 0.1, 0.0]]
#error_set = [????]

# property: P1 [can make X0 bigger by extending into -ve direction]
# vio = 8/100k [time without plotting = 10min]
# grid_eps = 1., 1., 2.0
# num_samples = 5
# falsification times with plotting: 35m [1st iter]
# falsification times with SS = 0.1 min!! [no plotting]
#midist=X, used random smt coupled with smt
T = 0.1
initial_set = [[-0., -0., 0.0], [1.00, 1.0, 0.0]]
error_set = [[-4, 1.5, -20], [4., 10, 20]]


initial_discrete_state = [0]

initial_controller_state = [0]

num_controller_states = 1
num_plant_states = 3
num_control_inputs = 1
num_conrtoller_disturbances = 1
num_plant_disturbances = 0
num_plant_discrete_states = 1
num_reference_signals = 1
num_pvt_sim_states = 1

# Reference signal \in [0.0, 4.0]
# Disturbances ... add later
ci = [[0.], [0.]]
#.65
#.6
pi = []

MAX_ITER = 4

controller = 'fuzzy_controller'

controller_path_dir_path = './paths'
CONVERSION_FACTOR = 100.0

MAX_ITER = 10
