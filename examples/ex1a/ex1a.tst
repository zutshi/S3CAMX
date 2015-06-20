MODE = 'falsify'
METHOD = 'concrete'

initial_set = [[0.0], [2.0]]   # property should be sat with 0.6 <= x0 <= 0.6

error_set = [[-10.0], [0.0]]    # x becomes negative. replace bigNum by infinity

initial_discrete_state = [0]

initial_controller_state = []

T = 2.0

controller = None

num_controller_states = 0
num_plant_states = 1
num_control_inputs = 0
num_conrtoller_disturbances = 0
num_plant_disturbances = 0
num_plant_discrete_states = 1
num_reference_signals = 0
num_pvt_sim_states = 0

ci = []
pi = []

MAX_ITER = 8
