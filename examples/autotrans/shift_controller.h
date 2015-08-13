/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * File: shift_controller.h
 *
 * Code generated for Simulink model 'shift_controller'.
 *
 * Model version                  : 1.346
 * Simulink Coder version         : 8.8 (R2015a) 09-Feb-2015
 * C/C++ source code generated on : Wed Aug 12 15:25:17 2015
 *
 * Target selection: ert.tlc
 * Embedded hardware selection: 32-bit Generic
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#ifndef RTW_HEADER_shift_controller_h_
#define RTW_HEADER_shift_controller_h_
#include <string.h>
#ifndef shift_controller_COMMON_INCLUDES_
# define shift_controller_COMMON_INCLUDES_
#include "rtwtypes.h"
#endif                                 /* shift_controller_COMMON_INCLUDES_ */

#include "shift_controller_types.h"

/* Macros for accessing real-time model data structure */
#ifndef rtmGetErrorStatus
# define rtmGetErrorStatus(rtm)        ((rtm)->errorStatus)
#endif

#ifndef rtmSetErrorStatus
# define rtmSetErrorStatus(rtm, val)   ((rtm)->errorStatus = (val))
#endif

/* Block signals and states (auto storage) for system '<Root>' */
typedef struct {
  real_T disturbance[2];               /* '<S1>/disturbance' */
  real_T Gear;                         /* '<S1>/ShiftLogic' */
  uint32_T temporalCounter_i1;         /* '<S1>/ShiftLogic' */
  uint8_T is_active_c1_shift_controller;/* '<S1>/ShiftLogic' */
  uint8_T is_gear_state;               /* '<S1>/ShiftLogic' */
  uint8_T is_active_gear_state;        /* '<S1>/ShiftLogic' */
  uint8_T is_selection_state;          /* '<S1>/ShiftLogic' */
  uint8_T is_active_selection_state;   /* '<S1>/ShiftLogic' */
} DW_shift_controller_T;

/* External inputs (root inport signals with auto storage) */
typedef struct {
  real_T VehicleSpeed;                 /* '<Root>/VehicleSpeed' */
  real_T disturbance[2];               /* '<Root>/disturbance' */
} ExtU_shift_controller_T;

/* External outputs (root outports fed by signals with auto storage) */
typedef struct {
  real_T Gear;                         /* '<Root>/Gear' */
  real_T throttle_op;                  /* '<Root>/throttle_op' */
  real_T brake_op;                     /* '<Root>/brake_op' */
} ExtY_shift_controller_T;

/* Parameters (auto storage) */
struct P_shift_controller_T_ {
  real_T down_th_Y0;                   /* Expression: 0
                                        * Referenced by: '<S3>/down_th'
                                        */
  real_T up_th_Y0;                     /* Expression: 0
                                        * Referenced by: '<S3>/up_th'
                                        */
  real_T InterpDown_tableData[24];     /* Expression: DOWN_TABLE
                                        * Referenced by: '<S3>/InterpDown'
                                        */
  real_T InterpDown_bp01Data[6];       /* Expression: DOWN_TH_BP
                                        * Referenced by: '<S3>/InterpDown'
                                        */
  real_T InterpDown_bp02Data[4];       /* Expression: [1:4]
                                        * Referenced by: '<S3>/InterpDown'
                                        */
  real_T InterpUp_tableData[24];       /* Expression: UP_TABLE
                                        * Referenced by: '<S3>/InterpUp'
                                        */
  real_T InterpUp_bp01Data[6];         /* Expression: UP_TH_BP
                                        * Referenced by: '<S3>/InterpUp'
                                        */
  real_T InterpUp_bp02Data[4];         /* Expression: [1:4]
                                        * Referenced by: '<S3>/InterpUp'
                                        */
  real_T ShiftLogic_TWAIT;             /* Expression: TWAIT
                                        * Referenced by: '<S1>/ShiftLogic'
                                        */
  uint32_T InterpDown_maxIndex[2];     /* Computed Parameter: InterpDown_maxIndex
                                        * Referenced by: '<S3>/InterpDown'
                                        */
  uint32_T InterpUp_maxIndex[2];       /* Computed Parameter: InterpUp_maxIndex
                                        * Referenced by: '<S3>/InterpUp'
                                        */
};

/* Real-time Model Data Structure */
struct tag_RTM_shift_controller_T {
  const char_T * volatile errorStatus;

  /*
   * ModelData:
   * The following substructure contains information regarding
   * the data used in the model.
   */
  struct {
    P_shift_controller_T *defaultParam;
    DW_shift_controller_T *dwork;
  } ModelData;
};

/* Model entry point functions */
extern void shift_controller_initialize(RT_MODEL_shift_controller_T *const
  shift_controller_M, ExtU_shift_controller_T *shift_controller_U,
  ExtY_shift_controller_T *shift_controller_Y);
extern void shift_controller_step(RT_MODEL_shift_controller_T *const
  shift_controller_M, ExtU_shift_controller_T *shift_controller_U,
  ExtY_shift_controller_T *shift_controller_Y);

/*-
 * The generated code includes comments that allow you to trace directly
 * back to the appropriate location in the model.  The basic format
 * is <system>/block_name, where system is the system number (uniquely
 * assigned by Simulink) and block_name is the name of the block.
 *
 * Note that this particular code originates from a subsystem build,
 * and has its own system numbers different from the parent model.
 * Refer to the system hierarchy for this subsystem below, and use the
 * MATLAB hilite_system command to trace the generated code back
 * to the parent model.  For example,
 *
 * hilite_system('autotrans/shift_controller')    - opens subsystem autotrans/shift_controller
 * hilite_system('autotrans/shift_controller/Kp') - opens and selects block Kp
 *
 * Here is the system hierarchy for this model
 *
 * '<Root>' : 'autotrans'
 * '<S1>'   : 'autotrans/shift_controller'
 * '<S2>'   : 'autotrans/shift_controller/ShiftLogic'
 * '<S3>'   : 'autotrans/shift_controller/ShiftLogic/ComputeThreshold'
 */
#endif                                 /* RTW_HEADER_shift_controller_h_ */

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
