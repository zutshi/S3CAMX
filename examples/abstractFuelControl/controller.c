//#define KLEE_ASSUMES
//#define DEBUG

//#ifdef KLEE_ASSUMES
//  #include <klee/klee.h>
//#endif

#ifdef DEBUG
  #include <stdio.h>
#endif

#include "controller.h"


/*=======================================================================*
 * Fixed width word size data types:                                     *
 *   int8_T, int16_T, int32_T     - signed 8, 16, or 32 bit integers     *
 *   uint8_T, uint16_T, uint32_T  - unsigned 8, 16, or 32 bit integers   *
 *=======================================================================*/
typedef int int32_T;

/*===========================================================================*
 * Generic type definitions: boolean_T, int_T, uint_T, ulong_T, char_T,      *
 *                           and byte_T.                                     *
 *===========================================================================*/
typedef unsigned char boolean_T;

/*=======================================================================*
 * Min and Max:                                                          *
 *   int8_T, int16_T, int32_T     - signed 8, 16, or 32 bit integers     *
 *   uint8_T, uint16_T, uint32_T  - unsigned 8, 16, or 32 bit integers   *
 *=======================================================================*/
#define MAX_int8_T                     ((int8_T)(127))
#define MIN_int8_T                     ((int8_T)(-128))
#define MAX_uint8_T                    ((uint8_T)(255U))
#define MIN_uint8_T                    ((uint8_T)(0U))
#define MAX_int16_T                    ((int16_T)(32767))
#define MIN_int16_T                    ((int16_T)(-32768))
#define MAX_uint16_T                   ((uint16_T)(65535U))
#define MIN_uint16_T                   ((uint16_T)(0U))
#define MAX_int32_T                    ((int32_T)(2147483647))
#define MIN_int32_T                    ((int32_T)(-2147483647-1))
#define MAX_uint32_T                   ((uint32_T)(0xFFFFFFFFU))
#define MIN_uint32_T                   ((uint32_T)(0U))

/* Block signals (auto storage) */
typedef struct {
  int32_T Divide2;                     /* '<S24>/Divide2' */
} B_AF_Controller_T;

typedef struct {

  int32_T normal_mode_detect_1;        /* '<S26>/Unit Delay2' */
  int32_T pi;                          /* '<S9>/UnitDelay1' */
  int32_T air_estimate;                /* '<S5>/UnitDelay1' */
  int32_T commanded_fuel;              /* '<S1>/commanded_fuel' */
  int32_T airbyfuel_ref;               /* '<S1>/mode_fb1' */
  int32_T engine_speed;                /* '<S2>/DataStoreMemory' */
  int32_T throttle_flow;               /* '<S2>/DataStoreMemory1' */
  int32_T airbyfuel_meas;              /* '<S2>/DataStoreMemory2' */
  int32_T throttle_angle;              /* '<S2>/DataStoreMemory3' */
  boolean_T sensor_fail_detect;        /* '<S28>/Unit Delay' */
  boolean_T power_mode_detect;         /* '<S27>/Unit Delay1' */
  boolean_T normal_mode_detect_1_a;    /* '<S26>/Unit Delay1' */
  boolean_T controller_mode;           /* '<S1>/mode_fb' */
} DW_AF_Controller_T;


/* Parameters (auto storage) */
struct P_AF_Controller_T_ {
  int32_T Constant2_Value;             /* Computed Parameter: Constant2_Value
                                        * Referenced by: '<S6>/Constant2'
                                        */
  int32_T fb_fuel_saturation_UpperSat; /* Computed Parameter: fb_fuel_saturation_UpperSat
                                        * Referenced by: '<S6>/fb_fuel_saturation'
                                        */
  int32_T fb_fuel_saturation_LowerSat; /* Computed Parameter: fb_fuel_saturation_LowerSat
                                        * Referenced by: '<S6>/fb_fuel_saturation'
                                        */
  int32_T Constant3_Value;             /* Computed Parameter: Constant3_Value
                                        * Referenced by: '<S6>/Constant3'
                                        */
  int32_T Constant2_Value_d;           /* Computed Parameter: Constant2_Value_d
                                        * Referenced by: '<S8>/Constant2'
                                        */
  int32_T Constant8_Value;             /* Computed Parameter: Constant8_Value
                                        * Referenced by: '<S15>/Constant8'
                                        */
  int32_T UnitDelay1_InitialCondition; /* Computed Parameter: UnitDelay1_InitialCondition
                                        * Referenced by: '<S8>/UnitDelay1'
                                        */
  int32_T Constant8_Value_e;           /* Computed Parameter: Constant8_Value_e
                                        * Referenced by: '<S25>/Constant8'
                                        */
  int32_T Constant3_Value_c;           /* Computed Parameter: Constant3_Value_c
                                        * Referenced by: '<S8>/Constant3'
                                        */
  int32_T Constant8_Value_b;           /* Computed Parameter: Constant8_Value_b
                                        * Referenced by: '<S14>/Constant8'
                                        */
  int32_T Constant8_Value_o;           /* Computed Parameter: Constant8_Value_o
                                        * Referenced by: '<S16>/Constant8'
                                        */
  int32_T Constant8_Value_k;           /* Computed Parameter: Constant8_Value_k
                                        * Referenced by: '<S21>/Constant8'
                                        */
  int32_T Constant8_Value_ov;          /* Computed Parameter: Constant8_Value_ov
                                        * Referenced by: '<S23>/Constant8'
                                        */
  int32_T Constant8_Value_ev;          /* Computed Parameter: Constant8_Value_ev
                                        * Referenced by: '<S20>/Constant8'
                                        */
  int32_T Constant4_Value;             /* Computed Parameter: Constant4_Value
                                        * Referenced by: '<S8>/Constant4'
                                        */
  int32_T Constant8_Value_j;           /* Computed Parameter: Constant8_Value_j
                                        * Referenced by: '<S22>/Constant8'
                                        */
  int32_T Constant8_Value_o0;          /* Computed Parameter: Constant8_Value_o0
                                        * Referenced by: '<S17>/Constant8'
                                        */
  int32_T Constant8_Value_d;           /* Computed Parameter: Constant8_Value_d
                                        * Referenced by: '<S19>/Constant8'
                                        */
  int32_T Constant6_Value;             /* Computed Parameter: Constant6_Value
                                        * Referenced by: '<S8>/Constant6'
                                        */
  int32_T Constant5_Value;             /* Computed Parameter: Constant5_Value
                                        * Referenced by: '<S8>/Constant5'
                                        */
  int32_T Constant8_Value_h;           /* Computed Parameter: Constant8_Value_h
                                        * Referenced by: '<S26>/Constant8'
                                        */
  int32_T Constant8_Value_es;          /* Computed Parameter: Constant8_Value_es
                                        * Referenced by: '<S18>/Constant8'
                                        */
  int32_T Gain_Gain;                   /* Computed Parameter: Gain_Gain
                                        * Referenced by: '<S8>/Gain'
                                        */
  int32_T Constant1_Value;             /* Computed Parameter: Constant1_Value
                                        * Referenced by: '<S8>/Constant1'
                                        */
  int32_T Constant8_Value_km;          /* Computed Parameter: Constant8_Value_km
                                        * Referenced by: '<S24>/Constant8'
                                        */
  int32_T Gain3_Gain;                  /* Computed Parameter: Gain3_Gain
                                        * Referenced by: '<S12>/Gain3'
                                        */
  int32_T Gain2_Gain;                  /* Computed Parameter: Gain2_Gain
                                        * Referenced by: '<S12>/Gain2'
                                        */
  int32_T Gain1_Gain;                  /* Computed Parameter: Gain1_Gain
                                        * Referenced by: '<S12>/Gain1'
                                        */
  int32_T Constant1_Value_h;           /* Computed Parameter: Constant1_Value_h
                                        * Referenced by: '<S12>/Constant1'
                                        */
  int32_T UnitDelay1_InitialCondition_l;/* Computed Parameter: UnitDelay1_InitialCondition_l
                                         * Referenced by: '<S12>/UnitDelay1'
                                         */
  int32_T Gain_Gain_c;                 /* Computed Parameter: Gain_Gain_c
                                        * Referenced by: '<S12>/Gain'
                                        */
  int32_T Constant8_Value_l;           /* Computed Parameter: Constant8_Value_l
                                        * Referenced by: '<S28>/Constant8'
                                        */
  int32_T Constant8_Value_c;           /* Computed Parameter: Constant8_Value_c
                                        * Referenced by: '<S27>/Constant8'
                                        */
  int32_T Gain1_Gain_g;                /* Computed Parameter: Gain1_Gain_g
                                        * Referenced by: '<S13>/Gain1'
                                        */
  int32_T Gain1_Gain_j;                /* Computed Parameter: Gain1_Gain_j
                                        * Referenced by: '<S6>/Gain1'
                                        */
  int32_T Constant8_Value_i;           /* Computed Parameter: Constant8_Value_i
                                        * Referenced by: '<S10>/Constant8'
                                        */
  int32_T Constant8_Value_f;           /* Computed Parameter: Constant8_Value_f
                                        * Referenced by: '<S11>/Constant8'
                                        */
  int32_T fuel_saturation_UpperSat;    /* Computed Parameter: fuel_saturation_UpperSat
                                        * Referenced by: '<S6>/fuel_saturation'
                                        */
  int32_T fuel_saturation_LowerSat;    /* Computed Parameter: fuel_saturation_LowerSat
                                        * Referenced by: '<S6>/fuel_saturation'
                                        */
  int32_T Constant8_Value_m;           /* Computed Parameter: Constant8_Value_m
                                        * Referenced by: '<S9>/Constant8'
                                        */
  int32_T airbyfuel_reference_Value;   /* Computed Parameter: airbyfuel_reference_Value
                                        * Referenced by: '<S7>/airbyfuel_reference'
                                        */
  int32_T airbyfuel_reference_power_Value;/* Computed Parameter: airbyfuel_reference_power_Value
                                           * Referenced by: '<S7>/airbyfuel_reference_power'
                                           */
  int32_T UnitDelay2_InitialCondition; /* Computed Parameter: UnitDelay2_InitialCondition
                                        * Referenced by: '<S29>/Unit Delay2'
                                        */
  int32_T sampling_sec_Value;          /* Computed Parameter: sampling_sec_Value
                                        * Referenced by: '<S29>/sampling_sec'
                                        */
  int32_T normal_mode_start_sec_Value; /* Computed Parameter: normal_mode_start_sec_Value
                                        * Referenced by: '<S29>/normal_mode_start_sec'
                                        */
  int32_T Constant1_Value_f;           /* Computed Parameter: Constant1_Value_f
                                        * Referenced by: '<S30>/Constant1'
                                        */
  int32_T Constant_Value;              /* Computed Parameter: Constant_Value
                                        * Referenced by: '<S30>/Constant'
                                        */
  int32_T threshold_Value;             /* Computed Parameter: threshold_Value
                                        * Referenced by: '<S31>/threshold'
                                        */
  int32_T Gain2_Gain_i;                /* Computed Parameter: Gain2_Gain_i
                                        * Referenced by: '<S7>/Gain2'
                                        */
  int32_T DataStoreMemory_InitialValue;/* Computed Parameter: DataStoreMemory_InitialValue
                                        * Referenced by: '<S5>/DataStoreMemory'
                                        */
  int32_T DataStoreMemory1_InitialValue;/* Computed Parameter: DataStoreMemory1_InitialValue
                                         * Referenced by: '<S5>/DataStoreMemory1'
                                         */
  int32_T DataStoreMemory2_InitialValue;/* Computed Parameter: DataStoreMemory2_InitialValue
                                         * Referenced by: '<S5>/DataStoreMemory2'
                                         */
  int32_T DataStoreMemory3_InitialValue;/* Computed Parameter: DataStoreMemory3_InitialValue
                                         * Referenced by: '<S5>/DataStoreMemory3'
                                         */
  int32_T Constant8_Value_bz;          /* Computed Parameter: Constant8_Value_bz
                                        * Referenced by: '<S4>/Constant8'
                                        */
  int32_T Constant8_Value_oo;          /* Computed Parameter: Constant8_Value_oo
                                        * Referenced by: '<S2>/Constant8'
                                        */
  int32_T Constant8_Value_f0;          /* Computed Parameter: Constant8_Value_f0
                                        * Referenced by: '<S3>/Constant8'
                                        */
  int32_T commanded_fuel_InitialValue; /* Computed Parameter: commanded_fuel_InitialValue
                                        * Referenced by: '<S1>/commanded_fuel'
                                        */
  int32_T mode_fb1_InitialValue;       /* Computed Parameter: mode_fb1_InitialValue
                                        * Referenced by: '<S1>/mode_fb1'
                                        */
  boolean_T UnitDelay1_InitialCondition_c;/* Computed Parameter: UnitDelay1_InitialCondition_c
                                           * Referenced by: '<S29>/Unit Delay1'
                                           */
  boolean_T UnitDelay1_InitialCondition_f;/* Computed Parameter: UnitDelay1_InitialCondition_f
                                           * Referenced by: '<S30>/Unit Delay1'
                                           */
  boolean_T UnitDelay_InitialCondition;/* Computed Parameter: UnitDelay_InitialCondition
                                        * Referenced by: '<S31>/Unit Delay'
                                        */
  boolean_T mode_fb_InitialValue;      /* Computed Parameter: mode_fb_InitialValue
                                        * Referenced by: '<S1>/mode_fb'
                                        */
};

typedef struct P_AF_Controller_T_ P_AF_Controller_T;

static P_AF_Controller_T AF_Controller_P = {
  10000,                               /* Computed Parameter: Constant2_Value
                                        * Referenced by: '<S6>/Constant2'
                                        */
  2147483647,                          /* Computed Parameter: fb_fuel_saturation_UpperSat
                                        * Referenced by: '<S6>/fb_fuel_saturation'
                                        */
  0,                                   /* Computed Parameter: fb_fuel_saturation_LowerSat
                                        * Referenced by: '<S6>/fb_fuel_saturation'
                                        */
  10000,                               /* Computed Parameter: Constant3_Value
                                        * Referenced by: '<S6>/Constant3'
                                        */
  -366000,                             /* Computed Parameter: Constant2_Value_d
                                        * Referenced by: '<S8>/Constant2'
                                        */
  100000,                              /* Computed Parameter: Constant8_Value
                                        * Referenced by: '<S15>/Constant8'
                                        */
  98200,                               /* Computed Parameter: UnitDelay1_InitialCondition
                                        * Referenced by: '<S8>/UnitDelay1'
                                        */
  100,                                 /* Computed Parameter: Constant8_Value_e
                                        * Referenced by: '<S25>/Constant8'
                                        */
  90,                                  /* Computed Parameter: Constant3_Value_c
                                        * Referenced by: '<S8>/Constant3'
                                        */
  10,                                  /* Computed Parameter: Constant8_Value_b
                                        * Referenced by: '<S14>/Constant8'
                                        */
  100000,                              /* Computed Parameter: Constant8_Value_o
                                        * Referenced by: '<S16>/Constant8'
                                        */
  10,                                  /* Computed Parameter: Constant8_Value_k
                                        * Referenced by: '<S21>/Constant8'
                                        */
  10,                                  /* Computed Parameter: Constant8_Value_ov
                                        * Referenced by: '<S23>/Constant8'
                                        */
  10,                                  /* Computed Parameter: Constant8_Value_ev
                                        * Referenced by: '<S20>/Constant8'
                                        */
  -34,                                 /* Computed Parameter: Constant4_Value
                                        * Referenced by: '<S8>/Constant4'
                                        */
  10000,                               /* Computed Parameter: Constant8_Value_j
                                        * Referenced by: '<S22>/Constant8'
                                        */
  100,                                 /* Computed Parameter: Constant8_Value_o0
                                        * Referenced by: '<S17>/Constant8'
                                        */
  100,                                 /* Computed Parameter: Constant8_Value_d
                                        * Referenced by: '<S19>/Constant8'
                                        */
  1,                                   /* Computed Parameter: Constant6_Value
                                        * Referenced by: '<S8>/Constant6'
                                        */
  1,                                   /* Computed Parameter: Constant5_Value
                                        * Referenced by: '<S8>/Constant5'
                                        */
  10,                                  /* Computed Parameter: Constant8_Value_h
                                        * Referenced by: '<S26>/Constant8'
                                        */
  100000,                              /* Computed Parameter: Constant8_Value_es
                                        * Referenced by: '<S18>/Constant8'
                                        */
  4133,                                /* Computed Parameter: Gain_Gain
                                        * Referenced by: '<S8>/Gain'
                                        */
  1,                                   /* Computed Parameter: Constant1_Value
                                        * Referenced by: '<S8>/Constant1'
                                        */
  100,                                 /* Computed Parameter: Constant8_Value_km
                                        * Referenced by: '<S24>/Constant8'
                                        */
  1,                                   /* Computed Parameter: Gain3_Gain
                                        * Referenced by: '<S12>/Gain3'
                                        */
  1,                                   /* Computed Parameter: Gain2_Gain
                                        * Referenced by: '<S12>/Gain2'
                                        */
  14,                                  /* Computed Parameter: Gain1_Gain
                                        * Referenced by: '<S12>/Gain1'
                                        */
  1,                                   /* Computed Parameter: Constant1_Value_h
                                        * Referenced by: '<S12>/Constant1'
                                        */
  0,                                   /* Computed Parameter: UnitDelay1_InitialCondition_l
                                        * Referenced by: '<S12>/UnitDelay1'
                                        */
  4,                                   /* Computed Parameter: Gain_Gain_c
                                        * Referenced by: '<S12>/Gain'
                                        */
  1000,                                /* Computed Parameter: Constant8_Value_l
                                        * Referenced by: '<S28>/Constant8'
                                        */
  1000,                                /* Computed Parameter: Constant8_Value_c
                                        * Referenced by: '<S27>/Constant8'
                                        */
  100,                                 /* Computed Parameter: Gain1_Gain_g
                                        * Referenced by: '<S13>/Gain1'
                                        */
  100,                                 /* Computed Parameter: Gain1_Gain_j
                                        * Referenced by: '<S6>/Gain1'
                                        */
  1000,                                /* Computed Parameter: Constant8_Value_i
                                        * Referenced by: '<S10>/Constant8'
                                        */
  100,                                 /* Computed Parameter: Constant8_Value_f
                                        * Referenced by: '<S11>/Constant8'
                                        */
  1660000,                             /* Computed Parameter: fuel_saturation_UpperSat
                                        * Referenced by: '<S6>/fuel_saturation'
                                        */
  130000,                              /* Computed Parameter: fuel_saturation_LowerSat
                                        * Referenced by: '<S6>/fuel_saturation'
                                        */
  100,                                 /* Computed Parameter: Constant8_Value_m
                                        * Referenced by: '<S9>/Constant8'
                                        */
  147,                                 /* Computed Parameter: airbyfuel_reference_Value
                                        * Referenced by: '<S7>/airbyfuel_reference'
                                        */
  125,                                 /* Computed Parameter: airbyfuel_reference_power_Value
                                        * Referenced by: '<S7>/airbyfuel_reference_power'
                                        */
  0,                                   /* Computed Parameter: UnitDelay2_InitialCondition
                                        * Referenced by: '<S29>/Unit Delay2'
                                        */
  1,                                   /* Computed Parameter: sampling_sec_Value
                                        * Referenced by: '<S29>/sampling_sec'
                                        */
  1000,                                /* Computed Parameter: normal_mode_start_sec_Value
                                        * Referenced by: '<S29>/normal_mode_start_sec'
                                        */
  200,                                 /* Computed Parameter: Constant1_Value_f
                                        * Referenced by: '<S30>/Constant1'
                                        */
  500,                                 /* Computed Parameter: Constant_Value
                                        * Referenced by: '<S30>/Constant'
                                        */
  -10000,                              /* Computed Parameter: threshold_Value
                                        * Referenced by: '<S31>/threshold'
                                        */
  1000,                                /* Computed Parameter: Gain2_Gain_i
                                        * Referenced by: '<S7>/Gain2'
                                        */
  0,                                   /* Computed Parameter: DataStoreMemory_InitialValue
                                        * Referenced by: '<S5>/DataStoreMemory'
                                        */
  0,                                   /* Computed Parameter: DataStoreMemory1_InitialValue
                                        * Referenced by: '<S5>/DataStoreMemory1'
                                        */
  0,                                   /* Computed Parameter: DataStoreMemory2_InitialValue
                                        * Referenced by: '<S5>/DataStoreMemory2'
                                        */
  0,                                   /* Computed Parameter: DataStoreMemory3_InitialValue
                                        * Referenced by: '<S5>/DataStoreMemory3'
                                        */
  1000,                                /* Computed Parameter: Constant8_Value_bz
                                        * Referenced by: '<S4>/Constant8'
                                        */
  1000,                                /* Computed Parameter: Constant8_Value_oo
                                        * Referenced by: '<S2>/Constant8'
                                        */
  1000,                                /* Computed Parameter: Constant8_Value_f0
                                        * Referenced by: '<S3>/Constant8'
                                        */
  1726,                                /* Computed Parameter: commanded_fuel_InitialValue
                                        * Referenced by: '<S1>/commanded_fuel'
                                        */
  147000,                              /* Computed Parameter: mode_fb1_InitialValue
                                        * Referenced by: '<S1>/mode_fb1'
                                        */
  0,                                   /* Computed Parameter: UnitDelay1_InitialCondition_c
                                        * Referenced by: '<S29>/Unit Delay1'
                                        */
  0,                                   /* Computed Parameter: UnitDelay1_InitialCondition_f
                                        * Referenced by: '<S30>/Unit Delay1'
                                        */
  0,                                   /* Computed Parameter: UnitDelay_InitialCondition
                                        * Referenced by: '<S31>/Unit Delay'
                                        */
  1                                    /* Computed Parameter: mode_fb_InitialValue
                                        * Referenced by: '<S1>/mode_fb'
                                        */
};                                     /* Modifiable parameters */



/* Disable shift div, use traditional instead
int32_T div_s32_floor(int32_T numerator, int32_T denominator)
{
  int32_T quotient;
  uint32_T absNumerator;
  uint32_T absDenominator;
  uint32_T tempAbsQuotient;
  uint32_T quotientNeedsNegation;
  if (denominator == 0) {
    quotient = numerator >= 0 ? MAX_int32_T : MIN_int32_T;

    // Divide by zero handler
  } else {
    absNumerator = (uint32_T)(numerator >= 0 ? numerator : -numerator);
    absDenominator = (uint32_T)(denominator >= 0 ? denominator : -denominator);
    quotientNeedsNegation = (uint32_T)((numerator < 0) != (denominator < 0));
    tempAbsQuotient = absNumerator / absDenominator;
    if (quotientNeedsNegation) {
      absNumerator %= absDenominator;
      if (absNumerator > (uint32_T)0) {
        tempAbsQuotient++;
      }
    }

    quotient = quotientNeedsNegation ? -(int32_T)tempAbsQuotient : (int32_T)
      tempAbsQuotient;
  }

  return quotient;
}
*/
int32_T div_s32_floor(int32_T numerator, int32_T denominator)
{
  return numerator/denominator;
}
/*
void mul_wide_s32(int32_T in0, int32_T in1, uint32_T *ptrOutBitsHi, uint32_T
                  *ptrOutBitsLo)
{
  uint32_T absIn;
  uint32_T absIn_0;
  uint32_T in0Lo;
  uint32_T in0Hi;
  uint32_T in1Hi;
  uint32_T productHiLo;
  uint32_T productLoHi;
  absIn = (uint32_T)(in0 < 0 ? -in0 : in0);
  absIn_0 = (uint32_T)(in1 < 0 ? -in1 : in1);
  in0Hi = absIn >> 16U;
  in0Lo = absIn & 65535U;
  in1Hi = absIn_0 >> 16U;
  absIn = absIn_0 & 65535U;
  productHiLo = in0Hi * absIn;
  productLoHi = in0Lo * in1Hi;
  absIn *= in0Lo;
  absIn_0 = 0U;
  in0Lo = (productLoHi << 16U) + absIn;
  if (in0Lo < absIn) {
    absIn_0 = 1U;
  }

  absIn = in0Lo;
  in0Lo += productHiLo << 16U;
  if (in0Lo < absIn) {
    absIn_0++;
  }

  absIn = (((productLoHi >> 16U) + (productHiLo >> 16U)) + in0Hi * in1Hi) +
    absIn_0;
  if (!((in0 == 0) || ((in1 == 0) || ((in0 > 0) == (in1 > 0))))) {
    absIn = ~absIn;
    in0Lo = ~in0Lo;
    in0Lo++;
    if (in0Lo == 0U) {
      absIn++;
    }
  }

  *ptrOutBitsHi = absIn;
  *ptrOutBitsLo = in0Lo;
}
*/
/*  disable shift mult, and use traditional instead
int32_T mul_s32_s32_s32_sat(int32_T a, int32_T b)
{
  int32_T result;
  uint32_T u32_chi;
  uint32_T u32_clo;
  mul_wide_s32(a, b, &u32_chi, &u32_clo);
  if (((int32_T)u32_chi > 0) || ((u32_chi == 0U) && (u32_clo >= 2147483648U))) {
    result = MAX_int32_T;
  } else if (((int32_T)u32_chi < -1) || (((int32_T)u32_chi == -1) && (u32_clo <
               2147483648U))) {
    result = MIN_int32_T;
  } else {
    result = (int32_T)u32_clo;
  }

  return result;
}
*/
int32_T mul_s32_s32_s32_sat(int32_T a, int32_T b)
{
  return a*b;
}
/* Model step function */
void AF_Controller_step(
    B_AF_Controller_T *AF_Controller_B,
    DW_AF_Controller_T *AF_Controller_DW,
    int32_T AF_Controller_U_engine_speed_radps,
    int32_T AF_Controller_U_throttle_angle_deg,
    int32_T AF_Controller_U_throttle_flow_gps,
    int32_T AF_Controller_U_airbyfuel_meas,
    int32_T *AF_Controller_Y_commanded_fuel_gps,
    boolean_T *AF_Controller_Y_controller_mode,
    int32_T *AF_Controller_Y_airbyfuel_ref)
{
  /* local block i/o variables */
  int32_T rtb_Divide2;
  int32_T rtb_Divide2_h;
  int32_T rtb_Divide2_hv;
  int32_T rtb_DataStoreRead2;
  int32_T rtb_DataStoreRead;
  int32_T rtb_DataStoreRead_j;
  int32_T rtb_Divide2_e;
  int32_T rtb_DataStoreRead2_c;
  int32_T rtb_Product;
  int32_T rtb_Sum2;
  int32_T rtb_Sum3;
  int32_T rtb_DataStoreRead4_fi;
  int32_T rtb_DataStoreRead3;
  int32_T rtb_DataStoreRead5;
  int32_T rtb_DataStoreRead6;
  int32_T rtb_Switch_l;
  int32_T rtb_Prod1;
  int32_T rtb_Gain1_b;
  int32_T rtb_Prod1_n;
  int32_T rtb_Gain1_o;
  int32_T rtb_Sum3_b;
  int32_T rtb_Prod1_f;
  boolean_T rtb_DataStoreRead1_k;
  boolean_T rtb_LogicalOperator_a;
  boolean_T rtb_DataStoreRead3_k;
  boolean_T rtb_LogicalOperator;
  boolean_T rtb_RelationalOperator1;
  int32_T rtb_Sum_j;
  int32_T rtb_Divide2_j;
  int32_T rtb_Divide2_i;

  /* Outputs for Atomic SubSystem: '<Root>/AF_Controller' */
  /* Product: '<S4>/Divide2' incorporates:
   *  Constant: '<S4>/Constant8'
   *  Inport: '<Root>/engine_speed_radps'
   */
  rtb_Divide2 = div_s32_floor(AF_Controller_U_engine_speed_radps,
    AF_Controller_P.Constant8_Value_bz);

  /* Product: '<S2>/Divide2' incorporates:
   *  Constant: '<S2>/Constant8'
   *  Inport: '<Root>/throttle_angle_deg'
   */
  rtb_Divide2_h = div_s32_floor(AF_Controller_U_throttle_angle_deg,
    AF_Controller_P.Constant8_Value_oo);

  /* Product: '<S3>/Divide2' incorporates:
   *  Constant: '<S3>/Constant8'
   *  Inport: '<Root>/throttle_flow_gps'
   */
  rtb_Divide2_hv = div_s32_floor(AF_Controller_U_throttle_flow_gps,
    AF_Controller_P.Constant8_Value_f0);

  /* Outputs for Atomic SubSystem: '<S1>/fuel_controller' */
  /* DataStoreWrite: '<S5>/DataStoreWrite' */
  AF_Controller_DW->engine_speed = rtb_Divide2;

  /* DataStoreWrite: '<S5>/DataStoreWrite3' */
  AF_Controller_DW->throttle_angle = rtb_Divide2_h;

  /* DataStoreWrite: '<S5>/DataStoreWrite1' */
  AF_Controller_DW->throttle_flow = rtb_Divide2_hv;

  /* DataStoreWrite: '<S5>/DataStoreWrite2' incorporates:
   *  Inport: '<Root>/airbyfuel_meas'
   */
  AF_Controller_DW->airbyfuel_meas = AF_Controller_U_airbyfuel_meas;

  /* Outputs for Atomic SubSystem: '<S5>/fuel_controller_mode_10ms' */
  /* Outputs for Atomic SubSystem: '<S7>/sensor_failure_detection' */
  /* Logic: '<S31>/Logical Operator' incorporates:
   *  Constant: '<S31>/threshold'
   *  DataStoreRead: '<S7>/DataStoreRead2'
   *  RelationalOperator: '<S31>/Relational Operator'
   *  UnitDelay: '<S31>/Unit Delay'
   */
  rtb_LogicalOperator = ((AF_Controller_DW->airbyfuel_meas <=
    AF_Controller_P.threshold_Value) || AF_Controller_DW->sensor_fail_detect);

  /* Update for UnitDelay: '<S31>/Unit Delay' */
  AF_Controller_DW->sensor_fail_detect = rtb_LogicalOperator;

  /* End of Outputs for SubSystem: '<S7>/sensor_failure_detection' */

  /* Outputs for Atomic SubSystem: '<S7>/normal_mode_detection' */
  /* Sum: '<S29>/Sum' incorporates:
   *  Constant: '<S29>/sampling_sec'
   *  UnitDelay: '<S29>/Unit Delay2'
   */
  rtb_Sum_j = AF_Controller_DW->normal_mode_detect_1 +
    AF_Controller_P.sampling_sec_Value;

  /* Logic: '<S29>/Logical Operator' incorporates:
   *  Constant: '<S29>/normal_mode_start_sec'
   *  RelationalOperator: '<S29>/Relational Operator'
   *  UnitDelay: '<S29>/Unit Delay1'
   */
  rtb_LogicalOperator_a = ((rtb_Sum_j >=
    AF_Controller_P.normal_mode_start_sec_Value) ||
    AF_Controller_DW->normal_mode_detect_1_a);

  /* Update for UnitDelay: '<S29>/Unit Delay2' */
  AF_Controller_DW->normal_mode_detect_1 = rtb_Sum_j;

  /* Update for UnitDelay: '<S29>/Unit Delay1' */
  AF_Controller_DW->normal_mode_detect_1_a = rtb_LogicalOperator_a;

  /* End of Outputs for SubSystem: '<S7>/normal_mode_detection' */

  /* Outputs for Atomic SubSystem: '<S7>/power_mode_detection' */
  /* Switch: '<S30>/Switch' incorporates:
   *  Constant: '<S30>/Constant'
   *  Constant: '<S30>/Constant1'
   *  Sum: '<S30>/Sum'
   *  UnitDelay: '<S30>/Unit Delay1'
   */
  if (AF_Controller_DW->power_mode_detect) {
    rtb_Sum_j = AF_Controller_P.Constant_Value;
  } else {
    rtb_Sum_j = AF_Controller_P.Constant_Value +
      AF_Controller_P.Constant1_Value_f;
  }

  /* End of Switch: '<S30>/Switch' */

  /* RelationalOperator: '<S30>/Relational Operator1' incorporates:
   *  DataStoreRead: '<S7>/DataStoreRead4'
   */
  rtb_RelationalOperator1 = (AF_Controller_DW->throttle_angle >= rtb_Sum_j);

  /* Update for UnitDelay: '<S30>/Unit Delay1' */
  AF_Controller_DW->power_mode_detect = rtb_RelationalOperator1;

  /* End of Outputs for SubSystem: '<S7>/power_mode_detection' */

  /* DataStoreWrite: '<S7>/DataStoreWrite' incorporates:
   *  Logic: '<S7>/Logical Operator1'
   *  Logic: '<S7>/Logical Operator2'
   */
  AF_Controller_DW->controller_mode = (rtb_LogicalOperator ||
    (!rtb_LogicalOperator_a) || rtb_RelationalOperator1);

  /* Switch: '<S7>/Switch' incorporates:
   *  Constant: '<S7>/airbyfuel_reference'
   *  Constant: '<S7>/airbyfuel_reference_power'
   *  Logic: '<S7>/Logical Operator3'
   */
  if (rtb_LogicalOperator_a && rtb_RelationalOperator1) {
    rtb_Sum_j = AF_Controller_P.airbyfuel_reference_power_Value;
  } else {
    rtb_Sum_j = AF_Controller_P.airbyfuel_reference_Value;
  }

  /* End of Switch: '<S7>/Switch' */

  /* DataStoreWrite: '<S7>/DataStoreWrite1' incorporates:
   *  Gain: '<S7>/Gain2'
   */
  AF_Controller_DW->airbyfuel_ref = mul_s32_s32_s32_sat
    (AF_Controller_P.Gain2_Gain_i, rtb_Sum_j);

  /* End of Outputs for SubSystem: '<S5>/fuel_controller_mode_10ms' */

  /* Outputs for Atomic SubSystem: '<S5>/fuel_controller_10ms' */
  /* DataStoreRead: '<S6>/DataStoreRead' */
  rtb_DataStoreRead_j = AF_Controller_DW->throttle_flow;

  /* Outputs for Atomic SubSystem: '<S6>/air_estimation' */
  /* UnitDelay: '<S8>/UnitDelay1' */
  rtb_Sum_j = AF_Controller_DW->air_estimate;

  /* Product: '<S25>/Divide2' incorporates:
   *  Constant: '<S25>/Constant8'
   *  UnitDelay: '<S8>/UnitDelay1'
   */
  rtb_Divide2_j = div_s32_floor(AF_Controller_DW->air_estimate,
    AF_Controller_P.Constant8_Value_e);

  /* Product: '<S20>/Divide2' incorporates:
   *  Constant: '<S20>/Constant8'
   *  DataStoreRead: '<S6>/DataStoreRead1'
   */
  rtb_Prod1_f = div_s32_floor(AF_Controller_DW->engine_speed,
    AF_Controller_P.Constant8_Value_ev);

  /* Product: '<S22>/Divide2' incorporates:
   *  Constant: '<S21>/Constant8'
   *  Constant: '<S22>/Constant8'
   *  Constant: '<S23>/Constant8'
   *  Constant: '<S8>/Constant4'
   *  Product: '<S21>/Divide2'
   *  Product: '<S23>/Divide2'
   *  Product: '<S8>/Prod3'
   */
  rtb_Prod1_f = div_s32_floor(div_s32_floor(rtb_Divide2_j,
    AF_Controller_P.Constant8_Value_k) * div_s32_floor(rtb_Divide2_j,
    AF_Controller_P.Constant8_Value_ov) * rtb_Prod1_f *
    AF_Controller_P.Constant4_Value, AF_Controller_P.Constant8_Value_j);

  /* Product: '<S17>/Divide2' incorporates:
   *  Constant: '<S17>/Constant8'
   */
  rtb_Divide2_i = div_s32_floor(rtb_Prod1_f, AF_Controller_P.Constant8_Value_o0);

  /* Product: '<S8>/Prod5' incorporates:
   *  DataStoreRead: '<S6>/DataStoreRead1'
   */
  rtb_Prod1_f = AF_Controller_DW->engine_speed * AF_Controller_DW->engine_speed;

  /* Product: '<S8>/Prod4' incorporates:
   *  Constant: '<S19>/Constant8'
   *  Constant: '<S8>/Constant5'
   *  Constant: '<S8>/Constant6'
   *  Product: '<S19>/Divide2'
   */
  rtb_Prod1_f = div_s32_floor(rtb_Prod1_f, AF_Controller_P.Constant8_Value_d) *
    AF_Controller_P.Constant6_Value * rtb_Divide2_j *
    AF_Controller_P.Constant5_Value;

  /* Product: '<S18>/Divide2' incorporates:
   *  Constant: '<S18>/Constant8'
   *  Constant: '<S26>/Constant8'
   *  Product: '<S26>/Divide2'
   */
  rtb_Prod1_f = div_s32_floor(div_s32_floor(rtb_Prod1_f,
    AF_Controller_P.Constant8_Value_h), AF_Controller_P.Constant8_Value_es);

  /* Sum: '<S8>/Sum3' incorporates:
   *  Constant: '<S14>/Constant8'
   *  Constant: '<S15>/Constant8'
   *  Constant: '<S16>/Constant8'
   *  Constant: '<S8>/Constant2'
   *  Constant: '<S8>/Constant3'
   *  DataStoreRead: '<S6>/DataStoreRead1'
   *  Product: '<S14>/Divide2'
   *  Product: '<S15>/Divide2'
   *  Product: '<S16>/Divide2'
   *  Product: '<S8>/Prod2'
   */
  rtb_Sum3 = ((div_s32_floor(div_s32_floor(rtb_Divide2_j *
    AF_Controller_DW->engine_speed * AF_Controller_P.Constant3_Value_c,
    AF_Controller_P.Constant8_Value_b), AF_Controller_P.Constant8_Value_o) +
               div_s32_floor(AF_Controller_P.Constant2_Value_d,
    AF_Controller_P.Constant8_Value)) + rtb_Divide2_i) + rtb_Prod1_f;

  /* Product: '<S8>/Prod1' incorporates:
   *  Constant: '<S8>/Constant1'
   *  Gain: '<S8>/Gain'
   *  Sum: '<S8>/Sum1'
   */
  rtb_Prod1_f = mul_s32_s32_s32_sat(AF_Controller_P.Gain_Gain,
    rtb_DataStoreRead_j - rtb_Sum3) * AF_Controller_P.Constant1_Value;

  /* Update for UnitDelay: '<S8>/UnitDelay1' incorporates:
   *  Constant: '<S24>/Constant8'
   *  Product: '<S24>/Divide2'
   *  Sum: '<S8>/Sum2'
   */
  AF_Controller_DW->air_estimate = div_s32_floor(rtb_Prod1_f,
    AF_Controller_P.Constant8_Value_km) + rtb_Sum_j;

  /* End of Outputs for SubSystem: '<S6>/air_estimation' */

  /* DataStoreRead: '<S6>/DataStoreRead4' */
  rtb_Sum_j = AF_Controller_DW->airbyfuel_ref;

  /* Product: '<S10>/Divide2' incorporates:
   *  Constant: '<S10>/Constant8'
   *  DataStoreRead: '<S6>/DataStoreRead4'
   */
  rtb_Divide2_e = div_s32_floor(AF_Controller_DW->airbyfuel_ref,
    AF_Controller_P.Constant8_Value_i);

  /* Outputs for Atomic SubSystem: '<S6>/feedforward_controller' */
  /* Gain: '<S13>/Gain1' incorporates:
   *  Gain: '<S6>/Gain1'
   */
  rtb_Gain1_b = mul_s32_s32_s32_sat(AF_Controller_P.Gain1_Gain_g,
    mul_s32_s32_s32_sat(AF_Controller_P.Gain1_Gain_j, rtb_Sum3));

  /* Product: '<S13>/Product' */
  rtb_Product = div_s32_floor(rtb_Gain1_b, rtb_Divide2_e);

  /* DataStoreRead: '<S6>/DataStoreRead3' */
  rtb_DataStoreRead3_k = AF_Controller_DW->controller_mode;

  /* DataStoreRead: '<S6>/DataStoreRead2' */
  rtb_DataStoreRead2_c = AF_Controller_DW->airbyfuel_meas;

  /* Outputs for Enabled SubSystem: '<S6>/feedback_PI_controller' incorporates:
   *  EnablePort: '<S12>/Enable'
   */
  /* Logic: '<S6>/Logical Operator2' */
  if (!rtb_DataStoreRead3_k) {
    /* Gain: '<S12>/Gain3' */
    rtb_Prod1_n = mul_s32_s32_s32_sat(AF_Controller_P.Gain3_Gain,
      rtb_DataStoreRead2_c);

    /* Gain: '<S12>/Gain2' */
    rtb_Gain1_o = mul_s32_s32_s32_sat(AF_Controller_P.Gain2_Gain, rtb_Sum_j);

    /* Sum: '<S12>/Sum1' */
    rtb_Sum3_b = rtb_Prod1_n - rtb_Gain1_o;

    /* Gain: '<S12>/Gain1' */
    rtb_Gain1_o = mul_s32_s32_s32_sat(AF_Controller_P.Gain1_Gain, rtb_Sum3_b);

    /* Product: '<S12>/Prod1' incorporates:
     *  Constant: '<S12>/Constant1'
     */
    rtb_Prod1_n = rtb_Gain1_o * AF_Controller_P.Constant1_Value_h;

    /* Sum: '<S12>/Sum2' incorporates:
     *  UnitDelay: '<S12>/UnitDelay1'
     */
    rtb_Sum2 = rtb_Prod1_n + AF_Controller_DW->pi;

    /* Gain: '<S12>/Gain' */
    rtb_Sum_j = mul_s32_s32_s32_sat(AF_Controller_P.Gain_Gain_c, rtb_Sum3_b);

    /* Product: '<S28>/Divide2' incorporates:
     *  Constant: '<S28>/Constant8'
     */
    rtb_Sum3_b = div_s32_floor(rtb_Sum2, AF_Controller_P.Constant8_Value_l);

    /* Sum: '<S12>/Sum3' */
    rtb_Sum3_b += rtb_Sum_j;

    /* Product: '<S27>/Divide2' incorporates:
     *  Constant: '<S27>/Constant8'
     */
    AF_Controller_B->Divide2 = div_s32_floor(rtb_Sum3_b,
      AF_Controller_P.Constant8_Value_c);

    /* Update for UnitDelay: '<S12>/UnitDelay1' */
    AF_Controller_DW->pi = rtb_Sum2;
  }

  /* End of Logic: '<S6>/Logical Operator2' */
  /* End of Outputs for SubSystem: '<S6>/feedback_PI_controller' */

  /* Switch: '<S6>/Switch' incorporates:
   *  Constant: '<S6>/Constant3'
   */
  if (rtb_DataStoreRead3_k) {
    rtb_Switch_l = AF_Controller_P.Constant3_Value;
  } else {
    /* Sum: '<S6>/Sum1' incorporates:
     *  Constant: '<S6>/Constant2'
     */
    rtb_Sum_j = AF_Controller_P.Constant2_Value + AF_Controller_B->Divide2;

    /* Saturate: '<S6>/fb_fuel_saturation' */
    if (rtb_Sum_j >= AF_Controller_P.fb_fuel_saturation_UpperSat) {
      rtb_Switch_l = AF_Controller_P.fb_fuel_saturation_UpperSat;
    } else if (rtb_Sum_j <= AF_Controller_P.fb_fuel_saturation_LowerSat) {
      rtb_Switch_l = AF_Controller_P.fb_fuel_saturation_LowerSat;
    } else {
      rtb_Switch_l = rtb_Sum_j;
    }

    /* End of Saturate: '<S6>/fb_fuel_saturation' */
  }

  /* End of Switch: '<S6>/Switch' */

  /* Product: '<S6>/Prod1' incorporates:
   *  Constant: '<S11>/Constant8'
   *  Product: '<S11>/Divide2'
   */
  rtb_Prod1 = rtb_Product * div_s32_floor(rtb_Switch_l,
    AF_Controller_P.Constant8_Value_f);

  /* Saturate: '<S6>/fuel_saturation' */
  if (rtb_Prod1 >= AF_Controller_P.fuel_saturation_UpperSat) {
    rtb_Sum_j = AF_Controller_P.fuel_saturation_UpperSat;
  } else if (rtb_Prod1 <= AF_Controller_P.fuel_saturation_LowerSat) {
    rtb_Sum_j = AF_Controller_P.fuel_saturation_LowerSat;
  } else {
    rtb_Sum_j = rtb_Prod1;
  }

  /* DataStoreWrite: '<S6>/DataStoreWrite' incorporates:
   *  Constant: '<S9>/Constant8'
   *  Product: '<S9>/Divide2'
   *  Saturate: '<S6>/fuel_saturation'
   */
  AF_Controller_DW->commanded_fuel = div_s32_floor(rtb_Sum_j,
    AF_Controller_P.Constant8_Value_m);

  /* DataStoreRead: '<S5>/DataStoreRead4' */
  rtb_DataStoreRead4_fi = AF_Controller_DW->airbyfuel_meas;

  /* DataStoreRead: '<S5>/DataStoreRead3' */
  rtb_DataStoreRead3 = AF_Controller_DW->throttle_flow;

  /* DataStoreRead: '<S5>/DataStoreRead5' */
  rtb_DataStoreRead5 = AF_Controller_DW->throttle_angle;

  /* DataStoreRead: '<S5>/DataStoreRead6' */
  rtb_DataStoreRead6 = AF_Controller_DW->engine_speed;

  /* DataStoreRead: '<S1>/DataStoreRead2' */
  rtb_DataStoreRead2 = AF_Controller_DW->airbyfuel_ref;

  /* DataStoreRead: '<S1>/DataStoreRead' */
  rtb_DataStoreRead = AF_Controller_DW->commanded_fuel;

  /* DataStoreRead: '<S1>/DataStoreRead1' */
  rtb_DataStoreRead1_k = AF_Controller_DW->controller_mode;

  /* Outport: '<Root>/commanded_fuel_gps' */
  *AF_Controller_Y_commanded_fuel_gps = rtb_DataStoreRead;

  /* Outport: '<Root>/controller_mode' */
  *AF_Controller_Y_controller_mode = rtb_DataStoreRead1_k;

  /* Outport: '<Root>/airbyfuel_ref' */
  *AF_Controller_Y_airbyfuel_ref = rtb_DataStoreRead2;
}



void* controller(INPUT_VAL* input_val, RETURN_VAL* ret_val)
 {

  B_AF_Controller_T AF_Controller_B;
  DW_AF_Controller_T AF_Controller_DW;

  int32_T commanded_fuel_gps;
  boolean_T controller_mode;
  int32_T airbyfuel_ref;

#ifdef KLEE_ASSUMES
  /*
  klee_assume((input_val->x_arr[0] >= 0)&(input_val->x_arr[0] <= 0));
  klee_assume((input_val->x_arr[1] >= 0)&(input_val->x_arr[1] <= 0));
  klee_assume((input_val->x_arr[2] >= 0)&(input_val->x_arr[2] <= 0));
  klee_assume((input_val->x_arr[3] >= 0)&(input_val->x_arr[3] <= 0));
  klee_assume((input_val->x_arr[4] >= 0)&(input_val->x_arr[4] <= 0));
  klee_assume((input_val->x_arr[5] >= 0)&(input_val->x_arr[5] <= 0));
  klee_assume((input_val->x_arr[6] >= 0)&(input_val->x_arr[6] <= 0));
*/
  klee_assume((input_val->x_arr[7] >= 1040000)&(input_val->x_arr[7] <= 1050000));
  klee_assume((input_val->x_arr[8] >= 0)&(input_val->x_arr[8] <= 200000));
  klee_assume((input_val->x_arr[9] >= 20000)&(input_val->x_arr[9] <=700000));
  klee_assume((input_val->x_arr[10] >= 0)&(input_val->x_arr[10] <= 200000));

  //klee_assume((input_val->x_arr[11] >= 0)&(input_val->x_arr[11] <= 0));

#endif

  long engine_speed = input_val->x_arr[7]; // this is actually omega
  long throttle_angle = input_val->x_arr[8];
  long throttle_flow = input_val->x_arr[9];
  long airbyfuel_meas = input_val->x_arr[10];
  
#ifdef DEBUG
  /*
  printf("EN_SPEED = %d\t", input_val->x_arr[7]);
  printf("TH_ANGLE = %d\t", input_val->x_arr[8]);
  printf("TH_FLOW = %d\t", input_val->x_arr[9]);
  printf("AF_MEAS = %d\n", input_val->x_arr[10]);
  */
#endif

#ifdef KLEE_ASSUMES
  klee_assume((input_val->int_state_arr[0] >= 0));
 /* 
  klee_assume((input_val->int_state_arr[1] >= )&(input_val->int_state_arr[1] <= ));
  klee_assume((input_val->int_state_arr[2] >= )&(input_val->int_state_arr[2] <= ));
  klee_assume((input_val->int_state_arr[3] >= )&(input_val->int_state_arr[3] <= ));
  klee_assume((input_val->int_state_arr[4] >= )&(input_val->int_state_arr[4] <= ));
  klee_assume((input_val->int_state_arr[5] >= )&(input_val->int_state_arr[5] <= ));
  klee_assume((input_val->int_state_arr[6] >= )&(input_val->int_state_arr[6] <= ));
  klee_assume((input_val->int_state_arr[7] >= )&(input_val->int_state_arr[7] <= ));
  klee_assume((input_val->int_state_arr[8] >= )&(input_val->int_state_arr[8] <= ));
  klee_assume((input_val->int_state_arr[9] >= )&(input_val->int_state_arr[9] <= ));
  */
  klee_assume((input_val->int_state_arr[10] >= 0)&(input_val->int_state_arr[10] <= 0));
  //klee_assume((input_val->int_state_arr[11] >= )&(input_val->int_state_arr[11] <= ));
  
  klee_assume((input_val->int_state_arr[12] >= 0)&(input_val->int_state_arr[12] <= 1));
  //klee_assume((input_val->int_state_arr[] >= )&(input_val->int_state_arr[] <= ));
#endif
  AF_Controller_DW.normal_mode_detect_1 = input_val->int_state_arr[0];       /* '<S8>/Unit Delay2' */
  AF_Controller_DW.pi = input_val->int_state_arr[1];                         /* '<S6>/UnitDelay1' */
  AF_Controller_DW.air_estimate = input_val->int_state_arr[2];               /* '<S5>/UnitDelay1' */
  AF_Controller_DW.commanded_fuel = input_val->int_state_arr[3];             /* '<S1>/commanded_fuel' */
  AF_Controller_DW.airbyfuel_ref = input_val->int_state_arr[4];              /* '<S1>/mode_fb1' */
  AF_Controller_DW.engine_speed = input_val->int_state_arr[5];               /* '<S2>/DataStoreMemory' */
  AF_Controller_DW.throttle_flow = input_val->int_state_arr[6];              /* '<S2>/DataStoreMemory1' */
  AF_Controller_DW.airbyfuel_meas = input_val->int_state_arr[7];             /* '<S2>/DataStoreMemory2' */
  AF_Controller_DW.throttle_angle = input_val->int_state_arr[8];             /* '<S2>/DataStoreMemory3' */

  AF_Controller_DW.sensor_fail_detect = (boolean_T)(input_val->int_state_arr[9]);        /* '<S10>/Unit Delay' */
  AF_Controller_DW.power_mode_detect = (boolean_T)(input_val->int_state_arr[10]);         /* '<S9>/Unit Delay1' */
  AF_Controller_DW.normal_mode_detect_1_a = (boolean_T)(input_val->int_state_arr[11]);    /* '<S8>/Unit Delay1' */
  AF_Controller_DW.controller_mode = (boolean_T)(input_val->int_state_arr[12]);           /* '<S1>/mode_fb' */

  AF_Controller_B.Divide2 = input_val->int_state_arr[13];

#ifdef DEBUG
  /*
  printf("normal_mode_detect_1 = %d\t", input_val->int_state_arr[0]);
  printf("pi = %d\t", input_val->int_state_arr[1]);
  printf("air_estimate = %d\t", input_val->int_state_arr[2]);
  printf("commanded_fuel = %d\t", input_val->int_state_arr[3]);
  printf("airbyfuel_ref = %d\t", input_val->int_state_arr[4]);
  printf("engine_speed = %d\t", input_val->int_state_arr[5]);
  printf("throttle_flow = %d\t", input_val->int_state_arr[6]);
  printf("airbyfuel_meas = %d\t", input_val->int_state_arr[7]);
  printf("throttle_angle = %d\n", input_val->int_state_arr[8]);
  printf("sensor_fail_detect = %d\t", input_val->int_state_arr[9]);
  printf("power_mode_detect = %d\t", input_val->int_state_arr[10]);
  printf("normal_mode_detect_1_a = %d\t", input_val->int_state_arr[11]);
  printf("controller_mode = %d\t", input_val->int_state_arr[12]);
  printf("Divide2 = %d\n", input_val->int_state_arr[13]);
  */
#endif

  // actual controller call
  AF_Controller_step(&AF_Controller_B, &AF_Controller_DW, 
      engine_speed, throttle_angle, throttle_flow, airbyfuel_meas,
      &commanded_fuel_gps, &controller_mode, &airbyfuel_ref);

  ret_val->int_state_arr[0] = AF_Controller_DW.normal_mode_detect_1;       /* '<S8>/Unit Delay2' */
  ret_val->int_state_arr[1] = AF_Controller_DW.pi;                         /* '<S6>/UnitDelay1' */
  ret_val->int_state_arr[2] = AF_Controller_DW.air_estimate;               /* '<S5>/UnitDelay1' */
  ret_val->int_state_arr[3] = AF_Controller_DW.commanded_fuel;              /* '<S1>/commanded_fuel' */
  ret_val->int_state_arr[4] = AF_Controller_DW.airbyfuel_ref;               /* '<S1>/mode_fb1' */
  ret_val->int_state_arr[5] = AF_Controller_DW.engine_speed;                /* '<S2>/DataStoreMemory' */
  ret_val->int_state_arr[6] = AF_Controller_DW.throttle_flow;               /* '<S2>/DataStoreMemory1' */
  ret_val->int_state_arr[7] = AF_Controller_DW.airbyfuel_meas;              /* '<S2>/DataStoreMemory2' */
  ret_val->int_state_arr[8] = AF_Controller_DW.throttle_angle;              /* '<S2>/DataStoreMemory3' */

  ret_val->int_state_arr[9] = AF_Controller_DW.sensor_fail_detect;         /* '<S10>/Unit Delay' */
  ret_val->int_state_arr[10] = AF_Controller_DW.power_mode_detect;          /* '<S9>/Unit Delay1' */
  ret_val->int_state_arr[11] = AF_Controller_DW.normal_mode_detect_1_a;     /* '<S8>/Unit Delay1' */
  ret_val->int_state_arr[12] = AF_Controller_DW.controller_mode;            /* '<S1>/mode_fb' */

  ret_val->int_state_arr[13] = AF_Controller_B.Divide2;



  ret_val->output_arr[0] = commanded_fuel_gps;
  ret_val->output_arr[1] = controller_mode;
  ret_val->output_arr[2] = airbyfuel_ref;

#ifdef DEBUG
  printf("CMD_FUEL = %d\n", ret_val->output_arr[0]);
  /*
  printf("CMD_FUEL = %d\t", ret_val->output_arr[0]);
  printf("MODE = %d\t", ret_val->output_arr[1]);
  printf("AF_REF = %d\n", ret_val->output_arr[2]);
  printf("========================================================================\n");
  */
#endif

  return (void*)0;
}

void controller_init(){
}


