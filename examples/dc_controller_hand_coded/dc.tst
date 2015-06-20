
#MODE = 'simulate'
MODE = 'falsify'

METHOD = 'symbolic'

delta_t = 0.02

initial_set = [[0.0, 0.0], [0.0, 0.0]]

error_set = [[-1, -6.5], [-0.7, -5.6]]

initial_discrete_state = [0]

initial_controller_state = [0.0, 0.0, 0.0]

#T = 20.0
T = 2.0

num_controller_states = 3
num_plant_states = 2
num_control_inputs = 1
num_conrtoller_disturbances = 1
num_plant_disturbances = 0
num_plant_discrete_states = 1
num_reference_signals = 1
num_pvt_sim_states = 1

# Reference signal \in [0.0, 4.0]
# Disturbances ... add later
ci = [[0.0], [0.0]]
pi = []

MAX_ITER = 4

controller = './dc_controller_without_input'
#controller = './dc_controller_with_input'

controller_path_dir_path = './paths'

CONVERSION_FACTOR = 1000.0

MAX_ITER = 2

#        s=2,
#        u=1,
#        x=2,
#        r=1,
#        pi=1,
#        ci=1,
#        d=1,
#        p=1,
