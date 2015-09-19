/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * File: shift_controller.c
 *
 * Code generated for Simulink model 'shift_controller'.
 *
 * Model version                  : 1.351
 * Simulink Coder version         : 8.8 (R2015a) 09-Feb-2015
 * C/C++ source code generated on : Mon Aug 17 11:57:04 2015
 *
 * Target selection: ert.tlc
 * Embedded hardware selection: 32-bit Generic
 * Emulation hardware selection:
 *    Differs from embedded hardware (MATLAB Host)
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "shift_controller.h"
#include "shift_controller_private.h"

/* Named constants for Chart: '<S1>/ShiftLogic' */
#define shift_contro_IN_NO_ACTIVE_CHILD ((uint8_T)0U)
#define shift_controlle_IN_downshifting ((uint8_T)1U)
#define shift_controlle_IN_steady_state ((uint8_T)2U)
#define shift_controller_CALL_EVENT    (-1)
#define shift_controller_IN_first      ((uint8_T)1U)
#define shift_controller_IN_fourth     ((uint8_T)2U)
#define shift_controller_IN_second     ((uint8_T)3U)
#define shift_controller_IN_third      ((uint8_T)4U)
#define shift_controller_IN_upshifting ((uint8_T)3U)
#define shift_controller_event_DOWN    (0)
#define shift_controller_event_UP      (1)

/* Forward declaration for local functions */
static void shift_controller_gear_state(const int32_T *sfEvent,
  DW_shift_controller_T *shift_controller_DW);
real_T look2_binlxpw(real_T u0, real_T u1, const real_T bp0[], const real_T bp1[],
                     const real_T table[], const uint32_T maxIndex[], uint32_T
                     stride)
{
  real_T frac;
  uint32_T bpIndices[2];
  real_T fractions[2];
  real_T yL_1d;
  uint32_T iRght;
  uint32_T bpIdx;
  uint32_T iLeft;

  /* Lookup 2-D
     Search method: 'binary'
     Use previous index: 'off'
     Interpolation method: 'Linear'
     Extrapolation method: 'Linear'
     Use last breakpoint for index at or above upper limit: 'off'
     Remove protection against out-of-range input in generated code: 'off'
   */
  /* Prelookup - Index and Fraction
     Index Search method: 'binary'
     Extrapolation method: 'Linear'
     Use previous index: 'off'
     Use last breakpoint for index at or above upper limit: 'off'
     Remove protection against out-of-range input in generated code: 'off'
   */
  if (u0 <= bp0[0U]) {
    iLeft = 0U;
    frac = (u0 - bp0[0U]) / (bp0[1U] - bp0[0U]);
  } else if (u0 < bp0[maxIndex[0U]]) {
    /* Binary Search */
    bpIdx = maxIndex[0U] >> 1U;
    iLeft = 0U;
    iRght = maxIndex[0U];
    while (iRght - iLeft > 1U) {
      if (u0 < bp0[bpIdx]) {
        iRght = bpIdx;
      } else {
        iLeft = bpIdx;
      }

      bpIdx = (iRght + iLeft) >> 1U;
    }

    frac = (u0 - bp0[iLeft]) / (bp0[iLeft + 1U] - bp0[iLeft]);
  } else {
    iLeft = maxIndex[0U] - 1U;
    frac = (u0 - bp0[maxIndex[0U] - 1U]) / (bp0[maxIndex[0U]] - bp0[maxIndex[0U]
      - 1U]);
  }

  fractions[0U] = frac;
  bpIndices[0U] = iLeft;

  /* Prelookup - Index and Fraction
     Index Search method: 'binary'
     Extrapolation method: 'Linear'
     Use previous index: 'off'
     Use last breakpoint for index at or above upper limit: 'off'
     Remove protection against out-of-range input in generated code: 'off'
   */
  if (u1 <= bp1[0U]) {
    iLeft = 0U;
    frac = (u1 - bp1[0U]) / (bp1[1U] - bp1[0U]);
  } else if (u1 < bp1[maxIndex[1U]]) {
    /* Binary Search */
    bpIdx = maxIndex[1U] >> 1U;
    iLeft = 0U;
    iRght = maxIndex[1U];
    while (iRght - iLeft > 1U) {
      if (u1 < bp1[bpIdx]) {
        iRght = bpIdx;
      } else {
        iLeft = bpIdx;
      }

      bpIdx = (iRght + iLeft) >> 1U;
    }

    frac = (u1 - bp1[iLeft]) / (bp1[iLeft + 1U] - bp1[iLeft]);
  } else {
    iLeft = maxIndex[1U] - 1U;
    frac = (u1 - bp1[maxIndex[1U] - 1U]) / (bp1[maxIndex[1U]] - bp1[maxIndex[1U]
      - 1U]);
  }

  /* Interpolation 2-D
     Interpolation method: 'Linear'
     Use last breakpoint for index at or above upper limit: 'off'
     Overflow mode: 'portable wrapping'
   */
  bpIdx = iLeft * stride + bpIndices[0U];
  yL_1d = (table[bpIdx + 1U] - table[bpIdx]) * fractions[0U] + table[bpIdx];
  bpIdx += stride;
  return (((table[bpIdx + 1U] - table[bpIdx]) * fractions[0U] + table[bpIdx]) -
          yL_1d) * frac + yL_1d;
}

/* Function for Chart: '<S1>/ShiftLogic' */
static void shift_controller_gear_state(const int32_T *sfEvent,
  DW_shift_controller_T *shift_controller_DW)
{
  /* During 'gear_state': '<S2>:2' */
  switch (shift_controller_DW->is_gear_state) {
   case shift_controller_IN_first:
    /* During 'first': '<S2>:6' */
    if (*sfEvent == shift_controller_event_UP) {
      /* Transition: '<S2>:12' */
      shift_controller_DW->is_gear_state = shift_controller_IN_second;

      /* Entry 'second': '<S2>:4' */
      shift_controller_DW->Gear = 2.0;
    }
    break;

   case shift_controller_IN_fourth:
    /* During 'fourth': '<S2>:3' */
    if (*sfEvent == shift_controller_event_DOWN) {
      /* Transition: '<S2>:14' */
      shift_controller_DW->is_gear_state = shift_controller_IN_third;

      /* Entry 'third': '<S2>:5' */
      shift_controller_DW->Gear = 3.0;
    }
    break;

   case shift_controller_IN_second:
    /* During 'second': '<S2>:4' */
    if (*sfEvent == shift_controller_event_UP) {
      /* Transition: '<S2>:11' */
      shift_controller_DW->is_gear_state = shift_controller_IN_third;

      /* Entry 'third': '<S2>:5' */
      shift_controller_DW->Gear = 3.0;
    } else {
      if (*sfEvent == shift_controller_event_DOWN) {
        /* Transition: '<S2>:16' */
        shift_controller_DW->is_gear_state = shift_controller_IN_first;

        /* Entry 'first': '<S2>:6' */
        shift_controller_DW->Gear = 1.0;
      }
    }
    break;

   case shift_controller_IN_third:
    /* During 'third': '<S2>:5' */
    if (*sfEvent == shift_controller_event_UP) {
      /* Transition: '<S2>:10' */
      shift_controller_DW->is_gear_state = shift_controller_IN_fourth;

      /* Entry 'fourth': '<S2>:3' */
      shift_controller_DW->Gear = 4.0;
    } else {
      if (*sfEvent == shift_controller_event_DOWN) {
        /* Transition: '<S2>:15' */
        shift_controller_DW->is_gear_state = shift_controller_IN_second;

        /* Entry 'second': '<S2>:4' */
        shift_controller_DW->Gear = 2.0;
      }
    }
    break;

   default:
    /* Unreachable state, for coverage only */
    shift_controller_DW->is_gear_state = shift_contro_IN_NO_ACTIVE_CHILD;
    break;
  }
}

/* Model step function */
void shift_controller_step(RT_MODEL_shift_controller_T *const shift_controller_M)
{
  P_shift_controller_T *shift_controller_P = ((P_shift_controller_T *)
    shift_controller_M->ModelData.defaultParam);
  DW_shift_controller_T *shift_controller_DW = ((DW_shift_controller_T *)
    shift_controller_M->ModelData.dwork);
  ExtU_shift_controller_T *shift_controller_U = (ExtU_shift_controller_T *)
    shift_controller_M->ModelData.inputs;
  ExtY_shift_controller_T *shift_controller_Y = (ExtY_shift_controller_T *)
    shift_controller_M->ModelData.outputs;
  int32_T sfEvent;
  real_T InterpDown;
  real_T InterpUp;

  /* Outputs for Atomic SubSystem: '<Root>/shift_controller' */
  /* Inport: '<S1>/disturbance' incorporates:
   *  Inport: '<Root>/disturbance'
   */
  shift_controller_DW->disturbance[0] = shift_controller_U->disturbance[0];
  shift_controller_DW->disturbance[1] = shift_controller_U->disturbance[1];

  /* Chart: '<S1>/ShiftLogic' incorporates:
   *  Inport: '<Root>/VehicleSpeed'
   */
  /* Gateway: shift_controller/ShiftLogic */
  sfEvent = shift_controller_CALL_EVENT;
  if (shift_controller_DW->temporalCounter_i1 < MAX_uint32_T) {
    shift_controller_DW->temporalCounter_i1++;
  }

  /* During: shift_controller/ShiftLogic */
  if (shift_controller_DW->is_active_c1_shift_controller == 0U) {
    /* Entry: shift_controller/ShiftLogic */
    shift_controller_DW->is_active_c1_shift_controller = 1U;

    /* Entry Internal: shift_controller/ShiftLogic */
    shift_controller_DW->is_active_gear_state = 1U;

    /* Entry Internal 'gear_state': '<S2>:2' */
    /* Transition: '<S2>:13' */
    if (shift_controller_DW->is_gear_state == shift_controller_IN_first) {
    } else {
      shift_controller_DW->is_gear_state = shift_controller_IN_first;

      /* Entry 'first': '<S2>:6' */
      shift_controller_DW->Gear = 1.0;
    }

    shift_controller_DW->is_active_selection_state = 1U;

    /* Entry Internal 'selection_state': '<S2>:7' */
    /* Transition: '<S2>:17' */
    shift_controller_DW->is_selection_state = shift_controlle_IN_steady_state;
  } else {
    if (shift_controller_DW->is_active_gear_state == 0U) {
    } else {
      shift_controller_gear_state(&sfEvent, shift_controller_DW);
    }

    if (shift_controller_DW->is_active_selection_state == 0U) {
    } else {
      /* Outputs for Function Call SubSystem: '<S2>/ComputeThreshold' */
      /* Lookup_n-D: '<S3>/InterpDown' */
      /* During 'selection_state': '<S2>:7' */
      /* Simulink Function 'ComputeThreshold': '<S2>:33' */
      InterpDown = look2_binlxpw(shift_controller_DW->disturbance[0],
        shift_controller_DW->Gear, shift_controller_P->InterpDown_bp01Data,
        shift_controller_P->InterpDown_bp02Data,
        shift_controller_P->InterpDown_tableData,
        shift_controller_P->InterpDown_maxIndex, 6U);

      /* Lookup_n-D: '<S3>/InterpUp' */
      InterpUp = look2_binlxpw(shift_controller_DW->disturbance[0],
        shift_controller_DW->Gear, shift_controller_P->InterpUp_bp01Data,
        shift_controller_P->InterpUp_bp02Data,
        shift_controller_P->InterpUp_tableData,
        shift_controller_P->InterpUp_maxIndex, 6U);

      /* End of Outputs for SubSystem: '<S2>/ComputeThreshold' */
      switch (shift_controller_DW->is_selection_state) {
       case shift_controlle_IN_downshifting:
        /* During 'downshifting': '<S2>:1' */
        if ((shift_controller_DW->temporalCounter_i1 >= (uint32_T)
             shift_controller_P->ShiftLogic_TWAIT) &&
            (shift_controller_U->VehicleSpeed <= InterpDown)) {
          /* Transition: '<S2>:22' */
          /* Event: '<S2>:30' */
          sfEvent = shift_controller_event_DOWN;
          if (shift_controller_DW->is_active_gear_state == 0U) {
          } else {
            shift_controller_gear_state(&sfEvent, shift_controller_DW);
          }

          shift_controller_DW->is_selection_state =
            shift_controlle_IN_steady_state;
        } else {
          if (shift_controller_U->VehicleSpeed > InterpDown) {
            /* Transition: '<S2>:21' */
            shift_controller_DW->is_selection_state =
              shift_controlle_IN_steady_state;
          }
        }
        break;

       case shift_controlle_IN_steady_state:
        /* During 'steady_state': '<S2>:9' */
        if (shift_controller_U->VehicleSpeed > InterpUp) {
          /* Transition: '<S2>:18' */
          shift_controller_DW->is_selection_state =
            shift_controller_IN_upshifting;
          shift_controller_DW->temporalCounter_i1 = 0U;
        } else {
          if (shift_controller_U->VehicleSpeed < InterpDown) {
            /* Transition: '<S2>:19' */
            shift_controller_DW->is_selection_state =
              shift_controlle_IN_downshifting;
            shift_controller_DW->temporalCounter_i1 = 0U;
          }
        }
        break;

       case shift_controller_IN_upshifting:
        /* During 'upshifting': '<S2>:8' */
        if ((shift_controller_DW->temporalCounter_i1 >= (uint32_T)
             shift_controller_P->ShiftLogic_TWAIT) &&
            (shift_controller_U->VehicleSpeed >= InterpUp)) {
          /* Transition: '<S2>:23' */
          /* Event: '<S2>:31' */
          sfEvent = shift_controller_event_UP;
          if (shift_controller_DW->is_active_gear_state == 0U) {
          } else {
            shift_controller_gear_state(&sfEvent, shift_controller_DW);
          }

          shift_controller_DW->is_selection_state =
            shift_controlle_IN_steady_state;
        } else {
          if (shift_controller_U->VehicleSpeed < InterpUp) {
            /* Transition: '<S2>:20' */
            shift_controller_DW->is_selection_state =
              shift_controlle_IN_steady_state;
          }
        }
        break;

       default:
        /* Unreachable state, for coverage only */
        shift_controller_DW->is_selection_state =
          shift_contro_IN_NO_ACTIVE_CHILD;
        break;
      }
    }
  }

  /* End of Chart: '<S1>/ShiftLogic' */
  /* End of Outputs for SubSystem: '<Root>/shift_controller' */

  /* Outport: '<Root>/Gear' */
  shift_controller_Y->Gear = shift_controller_DW->Gear;

  /* Outport: '<Root>/throttle_op' */
  shift_controller_Y->throttle_op = shift_controller_DW->disturbance[0];

  /* Outport: '<Root>/brake_op' */
  shift_controller_Y->brake_op = shift_controller_DW->disturbance[1];
}

/* Model initialize function */
void shift_controller_initialize(RT_MODEL_shift_controller_T *const
  shift_controller_M)
{
  DW_shift_controller_T *shift_controller_DW = ((DW_shift_controller_T *)
    shift_controller_M->ModelData.dwork);
  ExtY_shift_controller_T *shift_controller_Y = (ExtY_shift_controller_T *)
    shift_controller_M->ModelData.outputs;
  ExtU_shift_controller_T *shift_controller_U = (ExtU_shift_controller_T *)
    shift_controller_M->ModelData.inputs;

  /* Registration code */

  /* states (dwork) */
  (void) memset((void *)shift_controller_DW, 0,
                sizeof(DW_shift_controller_T));

  {
    shift_controller_DW->disturbance[0] = 0.0;
    shift_controller_DW->disturbance[1] = 0.0;
    shift_controller_DW->Gear = 0.0;
  }

  /* external inputs */
  shift_controller_U->VehicleSpeed = 0.0;
  shift_controller_U->disturbance[0] = 0.0;
  shift_controller_U->disturbance[1] = 0.0;

  /* external outputs */
  shift_controller_Y->Gear = 0.0;
  shift_controller_Y->throttle_op = 0.0;
  shift_controller_Y->brake_op = 0.0;

  /* Start for Outport: '<Root>/Gear' */
  shift_controller_Y->Gear = shift_controller_DW->Gear;

  /* Start for Outport: '<Root>/throttle_op' */
  shift_controller_Y->throttle_op = shift_controller_DW->disturbance[0];

  /* Start for Outport: '<Root>/brake_op' */
  shift_controller_Y->brake_op = shift_controller_DW->disturbance[1];

  /* InitializeConditions for Atomic SubSystem: '<Root>/shift_controller' */
  /* InitializeConditions for Chart: '<S1>/ShiftLogic' */
  shift_controller_DW->is_active_gear_state = 0U;
  shift_controller_DW->is_gear_state = shift_contro_IN_NO_ACTIVE_CHILD;
  shift_controller_DW->is_active_selection_state = 0U;
  shift_controller_DW->is_selection_state = shift_contro_IN_NO_ACTIVE_CHILD;
  shift_controller_DW->temporalCounter_i1 = 0U;
  shift_controller_DW->is_active_c1_shift_controller = 0U;
  shift_controller_DW->Gear = 0.0;

  /* End of InitializeConditions for SubSystem: '<Root>/shift_controller' */
}

/* Model terminate function */
void shift_controller_terminate(RT_MODEL_shift_controller_T *const
  shift_controller_M)
{
  /* (no terminate code required) */
  UNUSED_PARAMETER(shift_controller_M);
}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
