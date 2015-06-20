delta_t = 0.01

plant_pvt_init_data = None


T = 10.0
# EN_SPEED = 1047197  TH_ANGLE = 88000  TH_FLOW = 26342 AF_MEAS = 0

########################### plant states
# cne
# Throttle delay
# p0
# Wall wetting
# V&V
# Amplitude
# Period
########################### plant outputs
# engine_speed_wk
# throttle_angle_wk
# throttle_flow_wk
# airbyfuel_meas_wk
# verification_measurement_wk
############################ plant search space

initial_set = [[0., 0., 0.982000, 0.011200, 0., 61.3, 05., 104.7197, 8.8000, 2.6342, 0., 0., 900],\
               [0., 0., 0.982000, 0.011200, 0., 81.2, 10., 104.7197, 8.8000, 2.6342, 0., 0., 1100]]

#initial_set = [[0., 0., 0.982000, 0.011200, 0., 0.0, 10., 0., 0., 0., 0., 0.,],\
#               [0., 0., 0.982000, 0.011200, 0., 61.1, 30.0, 0., 0., 0., 0., 0.,]]
error_set = [[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.02, 0.0],\
             [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.0, 0.0]]

grid_eps = [0.01, 0.01, 0.01, 0.01, 0.01, 20, 10, 0.01, 0.01, 0.01, 0.01, 0.01, 500.0]
num_samples = 1

initial_discrete_state = [0]
initial_private_state = [0]

#  AF_Controller_DW->normal_mode_detect_1 = 0;//AF_Controller_P->UnitDelay2_InitialCondition;
#  AF_Controller_DW->pi = 0;//AF_Controller_P->UnitDelay1_InitialCondition_l;
#  AF_Controller_DW->air_estimate = 98200;//AF_Controller_P->UnitDelay1_InitialCondition;
#  AF_Controller_DW->commanded_fuel = 1726;//AF_Controller_P->commanded_fuel_InitialValue;
#  AF_Controller_DW->airbyfuel_ref = 147000;//AF_Controller_P->mode_fb1_InitialValue;
#  AF_Controller_DW->engine_speed = 0;//AF_Controller_P->DataStoreMemory_InitialValue;
#  AF_Controller_DW->throttle_flow = 0;//AF_Controller_P->DataStoreMemory1_InitialValue;
#  AF_Controller_DW->airbyfuel_meas = 0;//AF_Controller_P->DataStoreMemory2_InitialValue;
#  AF_Controller_DW->throttle_angle = 0;//AF_Controller_P->DataStoreMemory3_InitialValue;
#  AF_Controller_DW->sensor_fail_detect = 0;//AF_Controller_P->UnitDelay_InitialCondition;
#  AF_Controller_DW->power_mode_detect = 0;//AF_Controller_P->UnitDelay1_InitialCondition_f;
#  AF_Controller_DW->normal_mode_detect_1_a = 0;//AF_Controller_P->UnitDelay1_InitialCondition_c;
#  AF_Controller_DW->controller_mode = 1;//AF_Controller_P->mode_fb_InitialValue; 
#  AF_Controller_B->Sum3 = 0;


initial_controller_integer_state = [0,        # normal_mode_detect_1
                            0,        # pi
                            9.82,    # air_estimate
                            0.1726,     # commanded_fuel
                            14.7,   # airbyfuel_ref
                            0,        # engine_speed
                            0,        # throttle_flow
                            0,        # airbyfuel_meas
                            0,        # throttle_angle
                            0,        # sensor_fail_detect
                            0,        # power_mode_detect
                            0,        # normal_mode_detect_1_a
                            0.0001,   # controller_mode         #TODO: this is not good...!! have to scale down stuff that is never being scaled!!
                            0,        # AF_Controller_B->Sum3
                            ]


num_control_inputs = 3
initial_controller_float_state = []


ci = [[0.0], [0.0]]
pi = []
MAX_ITER = 4
################
# Simulators
################
# Plant
plant_description = 'matlab'
plant_path = 'AbstractFuelControl.m'
# Controller
controller_path = './controller.so'
controller_path_dir_path = './paths'

CONVERSION_FACTOR = 1.0
#CONVERSION_FACTOR = 10000.0
refinement_factor = 2.0
