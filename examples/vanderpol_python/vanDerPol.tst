MODE = 'falsify'
METHOD = 'concrete'

initial_set = [[-0.4, -0.4], [0.4, 0.4]]

error_set = [[-1, -6.5], [-0.7, -5.6]]

initial_discrete_state = [0]

initial_controller_state = []

T = 1.0


controller = None

num_controller_states = 0
num_plant_states = 2
num_control_inputs = 0
num_conrtoller_disturbances = 0
num_plant_disturbances = 0
num_plant_discrete_states = 1
num_reference_signals = 0
num_pvt_sim_states = 0

ci = []
pi = []

MAX_ITER = 4
