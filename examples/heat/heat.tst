import heat as H

inf = float('inf')

benchmark_id = 1

plant_pvt_init_data = benchmark_id

delta_t = 0.5


X0, Xf, H0, NUM_ROOMS  = H.get_benchmark_inits(benchmark_id)
H.create_benchmark_specefic_controller_header(benchmark_id)
NUM_ROOMS = 3

# P1
#T = 50.0
T = 10.0

#initial_set = [[19.75894131, 19.07248385, 19.60889913], [19.75894131, 19.07248385, 19.60889913]]
initial_set = [[19.0, 19.0, 19.0], [20.0, 20.0, 20.0]]
#initial_set = X0

ci = [[0.0], [0.0]]

# easy prop!

# vio = _/100k took _ mins [plotting, logging?]
# SS = falsified in _ [plotting, logging?]
# grid_eps = <[0.0, 0.0]>
# num_samples = <2>
# SS + symex: falsified in _ [plotting, logging?]
#
#error_set = [[-inf, -inf, -inf], [17.5, inf, inf]]
#grid_eps = [1.0, 1.0, 1.0]
#min_smt_sample_dist = 0.5
#num_samples = 1


# hard prop

# vio = _/100k took _ mins [plotting, logging?]
# SS = falsified in _ [plotting, logging?]
# grid_eps = <[0.0, 0.0]>
# num_samples = <2>
# SS + symex: falsified in _ [plotting, logging?]
#
error_set = [[-inf, -inf, -inf], [17.23, inf, inf]]
grid_eps = [1.0, 1.0, 1.0]
min_smt_sample_dist = 0.5
#num_samples = 3
# 1 works!! ?? need to run regression
#num_samples = 3 # symex
num_samples = 5 # concrete


#TODO : add OR operator for error set!
#error_set = [[-inf, -inf, -inf], [inf, 17.5, inf]]
#error_set = [[-inf, -inf, -inf], [inf, inf , 17.5]]
#error_set = [[-inf, -inf, -inf], Xf]


initial_discrete_state = [0]

initial_controller_integer_state = [1, 0, 0]
#initial_controller_integer_state = H0
initial_controller_float_state = []


num_control_inputs = NUM_ROOMS

pi = [[],[]]

MAX_ITER = 10

################
# Simulators
################
# Plant
plant_description = 'python'
plant_path = 'heat_plant.py'
# Controller
controller_path = 'heat_controller.so'
controller_path_dir_path = './paths'

CONVERSION_FACTOR = 1.0
refinement_factor = 2.0
