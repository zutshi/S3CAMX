/*
 * File: continuous_kobuna_simpleFP.h
 *
 * Code generated for Simulink model 'continuous_kobuna_simpleFP'.
 *
 * Model version                  : 1.25
 * Simulink Coder version         : 8.5 (R2013b) 08-Aug-2013
 * C/C++ source code generated on : Mon Dec  8 15:36:04 2014
 *
 * Target selection: ert.tlc
 * Embedded hardware selection: 32-bit Generic
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#ifndef RTW_HEADER_continuous_kobuna_simpleFP_h_
#define RTW_HEADER_continuous_kobuna_simpleFP_h_
#include "rtwtypes.h"
#ifndef continuous_kobuna_simpleFP_COMMON_INCLUDES_
# define continuous_kobuna_simpleFP_COMMON_INCLUDES_
#include <string.h>
#include "rtwtypes.h"
#endif                                 /* continuous_kobuna_simpleFP_COMMON_INCLUDES_ */

/* Macros for accessing real-time model data structure */
#ifndef rtmGetErrorStatus
# define rtmGetErrorStatus(rtm)        ((rtm)->errorStatus)
#endif

#ifndef rtmSetErrorStatus
# define rtmSetErrorStatus(rtm, val)   ((rtm)->errorStatus = (val))
#endif

/* Forward declaration for rtModel */
typedef struct tag_RTM_continuous_kobuna_sim_T RT_MODEL_continuous_kobuna_si_T;

/* Block signals and states (auto storage) for system '<Root>' */
typedef struct {
  int32_T DiscreteTimeIntegrator_DSTATE;/* '<S2>/Discrete-Time Integrator' */
  int32_T DiscreteTimeIntegrator_DSTATE_f;/* '<S3>/Discrete-Time Integrator' */
  int8_T DiscreteTimeIntegrator_PrevRese;/* '<S2>/Discrete-Time Integrator' */
  int8_T DiscreteTimeIntegrator_PrevRe_b;/* '<S3>/Discrete-Time Integrator' */
} DW_continuous_kobuna_simpleFP_T;

/* External inputs (root inport signals with auto storage) */
typedef struct {
  int32_T s_u1;                        /* '<Root>/u1' */
  int32_T s_u2;                        /* '<Root>/u2' */
  int32_T s_u3;                        /* '<Root>/u3' */
  int32_T s_u4;                        /* '<Root>/u4' */
} ExtU_continuous_kobuna_simple_T;

/* External outputs (root outports fed by signals with auto storage) */
typedef struct {
  boolean_T Out1;                      /* '<Root>/Out1' */
} ExtY_continuous_kobuna_simple_T;

/* Parameters (auto storage) */
struct P_continuous_kobuna_simpleFP_T_ {
  int32_T Constant6_Value;             /* Computed Parameter: Constant6_Value
                                        * Referenced by: '<S2>/Constant6'
                                        */
  int32_T Constant_Value;              /* Computed Parameter: Constant_Value
                                        * Referenced by: '<S2>/Constant'
                                        */
  int32_T Constant2_Value;             /* Computed Parameter: Constant2_Value
                                        * Referenced by: '<S2>/Constant2'
                                        */
  int32_T Constant1_Value;             /* Computed Parameter: Constant1_Value
                                        * Referenced by: '<S2>/Constant1'
                                        */
  int32_T Constant6_Value_e;           /* Computed Parameter: Constant6_Value_e
                                        * Referenced by: '<S3>/Constant6'
                                        */
  int32_T Constant_Value_g;            /* Computed Parameter: Constant_Value_g
                                        * Referenced by: '<S3>/Constant'
                                        */
  int32_T Constant2_Value_m;           /* Computed Parameter: Constant2_Value_m
                                        * Referenced by: '<S3>/Constant2'
                                        */
  int32_T Constant1_Value_o;           /* Computed Parameter: Constant1_Value_o
                                        * Referenced by: '<S3>/Constant1'
                                        */
  int32_T Constant3_Value;             /* Computed Parameter: Constant3_Value
                                        * Referenced by: '<S2>/Constant3'
                                        */
  int32_T DiscreteTimeIntegrator_IC;   /* Computed Parameter: DiscreteTimeIntegrator_IC
                                        * Referenced by: '<S2>/Discrete-Time Integrator'
                                        */
  int32_T Switch_Threshold;            /* Computed Parameter: Switch_Threshold
                                        * Referenced by: '<S2>/Switch'
                                        */
  int32_T Constant4_Value;             /* Computed Parameter: Constant4_Value
                                        * Referenced by: '<S2>/Constant4'
                                        */
  int32_T Constant3_Value_b;           /* Computed Parameter: Constant3_Value_b
                                        * Referenced by: '<S3>/Constant3'
                                        */
  int32_T DiscreteTimeIntegrator_IC_c; /* Computed Parameter: DiscreteTimeIntegrator_IC_c
                                        * Referenced by: '<S3>/Discrete-Time Integrator'
                                        */
  int32_T Switch_Threshold_n;          /* Computed Parameter: Switch_Threshold_n
                                        * Referenced by: '<S3>/Switch'
                                        */
  int32_T Constant4_Value_d;           /* Computed Parameter: Constant4_Value_d
                                        * Referenced by: '<S3>/Constant4'
                                        */
};

/* Parameters (auto storage) */
typedef struct P_continuous_kobuna_simpleFP_T_ P_continuous_kobuna_simpleFP_T;

/* Real-time Model Data Structure */
struct tag_RTM_continuous_kobuna_sim_T {
  const char_T * volatile errorStatus;

  /*
   * ModelData:
   * The following substructure contains information regarding
   * the data used in the model.
   */
  struct {
    P_continuous_kobuna_simpleFP_T *defaultParam;
    DW_continuous_kobuna_simpleFP_T *dwork;
  } ModelData;
};

/* Model entry point functions */
extern void continuous_kobuna_simpleFP_initialize
  (RT_MODEL_continuous_kobuna_si_T *const continuous_kobuna_simpleFP_M,
   ExtU_continuous_kobuna_simple_T *continuous_kobuna_simpleFP_U,
   ExtY_continuous_kobuna_simple_T *continuous_kobuna_simpleFP_Y);
extern void continuous_kobuna_simpleFP_step(RT_MODEL_continuous_kobuna_si_T *
  const continuous_kobuna_simpleFP_M, ExtU_continuous_kobuna_simple_T
  *continuous_kobuna_simpleFP_U, ExtY_continuous_kobuna_simple_T
  *continuous_kobuna_simpleFP_Y);

/*-
 * The generated code includes comments that allow you to trace directly
 * back to the appropriate location in the model.  The basic format
 * is <system>/block_name, where system is the system number (uniquely
 * assigned by Simulink) and block_name is the name of the block.
 *
 * Use the MATLAB hilite_system command to trace the generated code back
 * to the model.  For example,
 *
 * hilite_system('<S3>')    - opens system 3
 * hilite_system('<S3>/Kp') - opens and selects block Kp which resides in S3
 *
 * Here is the system hierarchy for this model
 *
 * '<Root>' : 'continuous_kobuna_simpleFP'
 * '<S1>'   : 'continuous_kobuna_simpleFP/Subsystem'
 * '<S2>'   : 'continuous_kobuna_simpleFP/Subsystem/S1'
 * '<S3>'   : 'continuous_kobuna_simpleFP/Subsystem/S2'
 */
#endif                                 /* RTW_HEADER_continuous_kobuna_simpleFP_h_ */

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
