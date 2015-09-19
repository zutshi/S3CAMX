inf = float('inf')


plant_pvt_init_data = None

################################
# WARNING: if T is changed,
# make appropriate changes
# in AbstractFuelControl.m
# modify simTime in init()
T = 12
delta_t = 4
################################

# EN_SPEED = 1047197  TH_ANGLE = 88000  TH_FLOW = 26342 AF_MEAS = 0

########################### plant states
# cne
# Throttle delay
# p0
# Wall wetting
# V&V
# Amplitude % default in model = 10
# Period    % default in model = 10
########################### plant outputs
# engine_speed_wk
# throttle_angle_wk
# throttle_flow_wk
# airbyfuel_meas_wk
# verification_measurement_wk
############################ plant search space
# engine speed % default in model = 1000
# Time


## Jyo's request for Magazine
#initial_set = [[0., 0., 0.982000, 0.011200, 0., 60.0, 5., 104.7197, 8.8000, 2.6342, 0., 0., 4000.0, 0.80, 0.0,0.0, 0.0, 0.0, 0.982, 0.0, 0.0],\
#               [0., 0., 0.982000, 0.011200, 0., 60.0, 5., 104.7197, 8.8000, 2.6342, 0., 0., 4000.0, 0.80, 0.0,0.0, 0.0, 0.0, 0.982, 0.0, 0.0]]

initial_set = [[0.,   0.,0.982, 0.0112, 0.,01.0,  05., 104.7197, 8.8, 2.6342, 0.,   0.,   900.0,  0.99, 0.0,  0.0,  0.0,  0.0, 0.982,  0.0, 0.0],\
               [0,    0, 0.982, 0.0112, 0, 61.19, 10., 104.7197, 8.8, 2.6342, 0., 0., 4000.0, 1.01, 0., 0., 0., 0., 0.982, 0., 0.]]
               #[0., 0., 0.982000, 0.011200, 0., 61.19, 10., 104.7197, 8.8000, 2.6342, 0., 0., 4000.0, 1.20, 0.0,0.0, 0.0, 0.0, 0.982, 0.0, 0.0]]

error_set = [[-inf, -inf, -inf, -inf, -inf, -inf, -inf, -inf, -inf, -inf, -inf, 0.02, -inf, -inf, -inf, -inf, -inf, -inf, -inf, -inf, -inf],\
             [inf,   inf,  inf,  inf,  inf,  inf,  inf,  inf,  inf,  inf,  inf,  inf,  inf,  inf,  inf,  inf,  inf,  inf,  inf,  inf,  inf]]


#grid_eps = [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 10.0, 20.0, 2000.0, 10.0, 5.0, 0.0001, 0.0001, 500.0, 0.01, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001]

# af \in [0.8, 1.2]
#grid_eps = [0.001, 1, 1, 1, 1, 10.0, 20.0, 200.0, 10.0, 5.0, 1, 1, 500.0, 0.2, 1, 1, 1, 1, 1,1, 1]

# af \in [0.99, 1.01]
#grid_eps = [0.001, 1, 1, 1, 1, 10.0, 20.0, 200.0, 10.0, 5.0, 1, 1, 500.0, 0.01, 1, 1, 1, 1, 1,1, 1]
grid_eps = [0.00, 1, 1, 1, 1, 10.0, 20.0, 200.0, 10.0, 5.0, 1, 1, 500.0, 0.01, 1, 1, 1, 1, 1,1, 1]

min_smt_sample_dist = 0.05
num_samples = 3

initial_discrete_state = [0]

initial_controller_integer_state = []

initial_controller_float_state = []

#initial_controller_float_state = [0,        # normal_mode_detect_1
#                                  0,        # pi
#                                  0.982,    # air_estimate
#                                  0,        # sensor_fail_detect
#                                  0,        # power_mode_detect
#                                  0,        # normal_mode_detect_1_a
#                                  0,        # AF_Controller_B->Sum3
#                                  ]

num_control_inputs = 0


ci = [[0.0], [0.0]]
pi = [[],[]]
MAX_ITER = 4
################
# Simulators
################
# Plant
plant_description = 'matlab'
plant_path = 'AbstractFuelControl_BB.m'
# Controller
controller_path = None
controller_path_dir_path = None

CONVERSION_FACTOR = 1.0
refinement_factor = 2.0
