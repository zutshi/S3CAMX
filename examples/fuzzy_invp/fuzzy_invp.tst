delta_t = 0.01
plant_pvt_init_data = None

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
initial_set = [[-0.0, -0.0, 0.0], [1.00, 1.0, 0.0]]
error_set = [[-4, 1.5, -20], [4.0, 10, 20]]
MAX_ITER = 10
grid_eps = [1.0, 1.0, 2.0]
#grid_eps = 0.02, 0.02, 0.2
min_smt_sample_dist = 0.5
num_samples = 5
#num_samples = 1 # for testing

######################################

initial_discrete_state = [0]

initial_controller_integer_state = []
initial_controller_float_state = []

num_control_inputs = 1

# Reference signal \in [0.0, 4.0]
# Disturbances ... add later
#ci = [[0.], [0.]]
ci = [[0.0],[1.0]]
pi = [[],[]]

################
# Simulators
################
# Plant
plant_description = 'python'
plant_path = 'invp.py'
#Controller
controller_path = 'fuzzy_controller.so'
controller_path_dir_path = './paths'

CONVERSION_FACTOR = 1.0
refinement_factor = 2.0
