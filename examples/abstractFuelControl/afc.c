#include "controller.h"
typedef double real32_T;
typedef unsigned char boolean_T;


typedef struct {
  real32_T Sum3;
} B_Z_AF_Controller_T;

typedef struct {
  struct {
    void *LoggedData;
  } afc_PWORK;

  struct {
    void *LoggedData;
  } fc_PWORK;

  struct {
    void *LoggedData;
  } Scope_PWORK;

  struct {
    void *LoggedData;
  } fb_sat_PWORK;

  struct {
    void *LoggedData;
  } mode_PWORK;

  real32_T normal_mode_detect_1;
  real32_T pi;
  real32_T air_estimate;
  boolean_T sensor_fail_detect;
  boolean_T power_mode_detect;
  boolean_T normal_mode_detect_1_e;
} DW_Z_AF_Controller_T;

struct P_Z_AF_Controller_T_ {
  real32_T Constant2_Value;
  real32_T fb_fuel_saturation_UpperSat;
  real32_T fb_fuel_saturation_LowerSat;
  real32_T Constant3_Value;
  real32_T Constant1_Value;
  real32_T Constant2_Value_e;
  real32_T Constant3_Value_e;
  real32_T Constant4_Value;
  real32_T Constant5_Value;
  real32_T UnitDelay1_InitialCondition;
  real32_T Gain_Gain;
  real32_T Constant1_Value_m;
  real32_T Gain_Gain_b;
  real32_T Gain1_Gain;
  real32_T UnitDelay1_InitialCondition_f;
  real32_T fuel_saturation_UpperSat;
  real32_T fuel_saturation_LowerSat;
  real32_T airbyfuel_reference_Value;
  real32_T airbyfuel_reference_power_Value;
  real32_T UnitDelay2_InitialCondition;
  real32_T sampling_sec_Value;
  real32_T normal_mode_start_sec_Value;
  real32_T Constant1_Value_b;
  real32_T Constant_Value;
  real32_T threshold_Value;
  real32_T DataStoreMemory_InitialValue;
  real32_T DataStoreMemory1_InitialValue;
  real32_T DataStoreMemory2_InitialValue;
  real32_T DataStoreMemory3_InitialValue;
  real32_T commanded_fuel_InitialValue;
  real32_T mode_fb1_InitialValue;
  boolean_T UnitDelay1_InitialCondition_l;
  boolean_T UnitDelay1_InitialCondition_j;
  boolean_T UnitDelay_InitialCondition;
  boolean_T mode_fb_InitialValue;
};
typedef struct P_Z_AF_Controller_T_ P_Z_AF_Controller_T;
P_Z_AF_Controller_T Z_AF_Controller_P = {
  1.0,
  100.0,
  0.0,
  1.0,
  0.01,
  -0.366,
  0.08979,
  -0.0337,
  0.0001,
  0.982,
  0.41328,
  0.01,
  0.04,
  0.14,
  0.0,
  1.66,
  0.13,
  14.7,
  12.5,
  0.0,
  0.01,
  10.0,
  20.0,
  50.0,
  -1.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.1726,
  14.7,
  0,
  0,
  0,
  1
};


void Z_AF_Controller_step(B_Z_AF_Controller_T *Z_AF_Controller_B,
  DW_Z_AF_Controller_T *Z_AF_Controller_DW,
  real32_T Z_AF_Controller_U_engine_speed_radps, real32_T
  Z_AF_Controller_U_throttle_angle_deg, real32_T
  Z_AF_Controller_U_throttle_flow_gps, real32_T Z_AF_Controller_U_airbyfuel_meas,
  real32_T *Z_AF_Controller_Y_commanded_fuel_gps, boolean_T
  *Z_AF_Controller_Y_controller_mode, real32_T *Z_AF_Controller_Y_airbyfuel_ref)
{
  real32_T rtb_DataStoreRead2;
  real32_T rtb_DataStoreRead;
  real32_T rtb_DataStoreRead4_c;
  real32_T rtb_DataStoreRead3;
  real32_T rtb_DataStoreRead5;
  real32_T rtb_DataStoreRead6;
  real32_T rtb_Switch_n0;
  boolean_T rtb_DataStoreRead1_a;
  boolean_T rtb_LogicalOperator_d;
  boolean_T rtb_DataStoreRead3_f;
  boolean_T rtb_LogicalOperator;
  boolean_T rtb_RelationalOperator1;
  real32_T rtb_Sum_d;
  real32_T rtb_Sum3;
  real32_T rtb_Sum1_d;
  real32_T rtb_Sum2;
  rtb_LogicalOperator = ((Z_AF_Controller_U_airbyfuel_meas <=
    Z_AF_Controller_P.threshold_Value) ||
    Z_AF_Controller_DW->sensor_fail_detect);
  Z_AF_Controller_DW->sensor_fail_detect = rtb_LogicalOperator;
  rtb_Sum_d = Z_AF_Controller_DW->normal_mode_detect_1 +
    Z_AF_Controller_P.sampling_sec_Value;
  rtb_LogicalOperator_d = ((rtb_Sum_d >=
    Z_AF_Controller_P.normal_mode_start_sec_Value) ||
    Z_AF_Controller_DW->normal_mode_detect_1_e);
  Z_AF_Controller_DW->normal_mode_detect_1 = rtb_Sum_d;
  Z_AF_Controller_DW->normal_mode_detect_1_e = rtb_LogicalOperator_d;
  if (Z_AF_Controller_DW->power_mode_detect) {
    rtb_Sum1_d = Z_AF_Controller_P.Constant_Value;
  } else {
    rtb_Sum1_d = Z_AF_Controller_P.Constant_Value +
      Z_AF_Controller_P.Constant1_Value_b;
  }

  rtb_RelationalOperator1 = (Z_AF_Controller_U_throttle_angle_deg >= rtb_Sum1_d);
  Z_AF_Controller_DW->power_mode_detect = rtb_RelationalOperator1;
  rtb_LogicalOperator = (rtb_LogicalOperator || (!rtb_LogicalOperator_d) ||
    rtb_RelationalOperator1);
  if (rtb_LogicalOperator_d && rtb_RelationalOperator1) {
    rtb_Sum_d = Z_AF_Controller_P.airbyfuel_reference_power_Value;
  } else {
    rtb_Sum_d = Z_AF_Controller_P.airbyfuel_reference_Value;
  }

  rtb_Sum3 = ((Z_AF_Controller_DW->air_estimate *
               Z_AF_Controller_U_engine_speed_radps *
               Z_AF_Controller_P.Constant3_Value_e +
               Z_AF_Controller_P.Constant2_Value_e) +
              Z_AF_Controller_DW->air_estimate *
              Z_AF_Controller_DW->air_estimate *
              Z_AF_Controller_U_engine_speed_radps *
              Z_AF_Controller_P.Constant4_Value) +
    Z_AF_Controller_U_engine_speed_radps * Z_AF_Controller_U_engine_speed_radps *
    Z_AF_Controller_DW->air_estimate * Z_AF_Controller_P.Constant5_Value;
  Z_AF_Controller_DW->air_estimate += (Z_AF_Controller_U_throttle_flow_gps -
    rtb_Sum3) * Z_AF_Controller_P.Gain_Gain *
    Z_AF_Controller_P.Constant1_Value;
  rtb_DataStoreRead3_f = rtb_LogicalOperator;
  if (!rtb_DataStoreRead3_f) {
    rtb_Sum1_d = Z_AF_Controller_U_airbyfuel_meas - rtb_Sum_d;
    rtb_Sum2 = Z_AF_Controller_P.Gain1_Gain * rtb_Sum1_d *
      Z_AF_Controller_P.Constant1_Value_m + Z_AF_Controller_DW->pi;
    Z_AF_Controller_B->Sum3 = Z_AF_Controller_P.Gain_Gain_b * rtb_Sum1_d +
      rtb_Sum2;
    Z_AF_Controller_DW->pi = rtb_Sum2;
  }

  if (rtb_DataStoreRead3_f) {
    rtb_Switch_n0 = Z_AF_Controller_P.Constant3_Value;
  } else {
    rtb_Sum1_d = Z_AF_Controller_P.Constant2_Value + Z_AF_Controller_B->Sum3;
    if (rtb_Sum1_d > Z_AF_Controller_P.fb_fuel_saturation_UpperSat) {
      rtb_Switch_n0 = Z_AF_Controller_P.fb_fuel_saturation_UpperSat;
    } else if (rtb_Sum1_d < Z_AF_Controller_P.fb_fuel_saturation_LowerSat) {
      rtb_Switch_n0 = Z_AF_Controller_P.fb_fuel_saturation_LowerSat;
    } else {
      rtb_Switch_n0 = rtb_Sum1_d;
    }
  }

  rtb_Sum1_d = rtb_Sum3 / rtb_Sum_d * rtb_Switch_n0;
  if (rtb_Sum1_d > Z_AF_Controller_P.fuel_saturation_UpperSat) {
    rtb_DataStoreRead = Z_AF_Controller_P.fuel_saturation_UpperSat;
  } else if (rtb_Sum1_d < Z_AF_Controller_P.fuel_saturation_LowerSat) {
    rtb_DataStoreRead = Z_AF_Controller_P.fuel_saturation_LowerSat;
  } else {
    rtb_DataStoreRead = rtb_Sum1_d;
  }

  rtb_DataStoreRead4_c = Z_AF_Controller_U_airbyfuel_meas;
  rtb_DataStoreRead3 = Z_AF_Controller_U_throttle_flow_gps;
  rtb_DataStoreRead5 = Z_AF_Controller_U_throttle_angle_deg;
  rtb_DataStoreRead6 = Z_AF_Controller_U_engine_speed_radps;
  rtb_DataStoreRead2 = rtb_Sum_d;
  rtb_DataStoreRead1_a = rtb_LogicalOperator;
  *Z_AF_Controller_Y_commanded_fuel_gps = rtb_DataStoreRead;
  *Z_AF_Controller_Y_controller_mode = rtb_DataStoreRead1_a;
  *Z_AF_Controller_Y_airbyfuel_ref = rtb_DataStoreRead2;
}

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
{       
  // bus
  B_Z_AF_Controller_T Z_AF_Controller_B;

  // DSM
  DW_Z_AF_Controller_T Z_AF_Controller_DW;

  // outputs
  real32_T commanded_fuel_gps;
  boolean_T controller_mode;
  real32_T airbyfuel_ref;

  // plant states
  double engine_speed = input->x_arr[7];
  double throttle_angle = input->x_arr[8];
  double throttle_flow = input->x_arr[9];
  double airbyfuel_meas = input->x_arr[10];

  Z_AF_Controller_DW.normal_mode_detect_1 = input->float_state_arr[0];
  Z_AF_Controller_DW.pi = input->float_state_arr[1];
  Z_AF_Controller_DW.air_estimate = input->float_state_arr[2];
  Z_AF_Controller_DW.sensor_fail_detect = input->float_state_arr[3];
  Z_AF_Controller_DW.power_mode_detect = input->float_state_arr[4];
  Z_AF_Controller_DW.normal_mode_detect_1_e = input->float_state_arr[5];
  Z_AF_Controller_B.Sum3 = input->float_state_arr[6];

  // actual controller call
  Z_AF_Controller_step(&Z_AF_Controller_B, &Z_AF_Controller_DW, 
      engine_speed, throttle_angle, throttle_flow, airbyfuel_meas,
      &commanded_fuel_gps, &controller_mode, &airbyfuel_ref);

  ret_val->float_state_arr[0] = Z_AF_Controller_DW.normal_mode_detect_1;
  ret_val->float_state_arr[1] = Z_AF_Controller_DW.pi;
  ret_val->float_state_arr[2] = Z_AF_Controller_DW.air_estimate;
  ret_val->float_state_arr[3] = Z_AF_Controller_DW.sensor_fail_detect;
  ret_val->float_state_arr[4] = Z_AF_Controller_DW.power_mode_detect;
  ret_val->float_state_arr[5] = Z_AF_Controller_DW.normal_mode_detect_1_e;
  ret_val->float_state_arr[6] = Z_AF_Controller_B.Sum3;


  ret_val->output_arr[0] = commanded_fuel_gps;
  ret_val->output_arr[1] = controller_mode;
  ret_val->output_arr[2] = airbyfuel_ref;

#ifdef DEBUG_PRINT
  printf("CMD_FUEL = %f\n", commanded_fuel_gps);
#endif
}

void controller_init(){
}
