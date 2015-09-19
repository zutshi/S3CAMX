import numpy as np

delta_t = 0.01

plant_pvt_init_data = None

################################
# WARNING: if T is changed,
# make appropriate changes
# in AbstractFuelControl.m
# modify simTime in init()
T = 12.0
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

# fix states for testing....
#initial_set = [[0., 0., 0.982000, 0.011200, 0., 68.423, 7.9048, 104.7197, 8.8000, 2.6342, 0., 0., 1021.8],\
#               [0., 0., 0.982000, 0.011200, 0., 68.423, 7.9048, 104.7197, 8.8000, 2.6342, 0., 0., 1021.8]]

# Actual initial set!
#initial_set = [[0., 0., 0.982000, 0.011200, 0., 61.3, 05., 104.7197, 8.8000, 2.6342, 0., 0., 900],\
#               [0., 0., 0.982000, 0.011200, 0., 81.2, 10., 104.7197, 8.8000, 2.6342, 0., 0., 1100]]

## Jyo's request for Magazine
#              [cne, Thr., p0,       ww,    V&V, amp, prd, en_sp,     th_fl,   af,  ver, \mu, en_sp, AF_tol]
initial_set = [[0., 0., 0.982000, 0.011200, 0., 01.0,  05., 104.7197, 8.8000, 2.6342, 0., 0., 900,   0.8],\
               [0., 0., 0.982000, 0.011200, 0., 61.19, 10., 104.7197, 8.8000, 2.6342, 0., 0., 4000,  1.2]]

#initial_set = [[0., 0., 0.982000, 0.011200, 0., 0.0, 10., 0., 0., 0., 0., 0.,],\
#               [0., 0., 0.982000, 0.011200, 0., 61.1, 30.0, 0., 0., 0., 0., 0.,]]
# must change .m file for prop vio detection!

error_set = [[-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, 0.02, -np.inf, -np.inf],\
             [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf]]

#grid_eps = [0.01, 0.01, 0.01, 0.01, 0.01, 20, 5, 0.01, 0.01, 0.01, 0.01, 0.01, 500.0]
#           cne, Thr., p0, ww,  V&V, amp,   prd,  en_sp, th_fl, af, ver, \mu, en_sp, AF_tol
grid_eps = [1.0, 1.0, 1.0, 1.0, 1.0, 100.0, 20.0, 200.0, 10.0, 5.0, 1.0, 1.0, 2000.0, 0.2]
num_samples = 1
min_smt_sample_dist = 0.05

initial_discrete_state = [0]
initial_private_state = [T]

initial_controller_integer_state = []

initial_controller_float_state = [0,        # normal_mode_detect_1
                                  0,        # pi
                                  0.982,    # air_estimate
                                  0,        # sensor_fail_detect
                                  0,        # power_mode_detect
                                  0,        # normal_mode_detect_1_a
                                  0,        # AF_Controller_B->Sum3
                                  ]

num_control_inputs = 3


ci = [[0.0], [0.0]]
pi = [[],[]]
MAX_ITER = 4
################
# Simulators
################
# Plant
plant_description = 'matlab'
plant_path = 'AbstractFuelControl.m'
# Controller
controller_path = './afc.so'
controller_path_dir_path = './paths'

CONVERSION_FACTOR = 1.0
#CONVERSION_FACTOR = 10000.0
refinement_factor = 2.0
