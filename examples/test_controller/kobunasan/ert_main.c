/*
 * File: ert_main.c
 *
 * Code generated for Simulink model 'continuous_kobuna_FP'.
 *
 * Model version                  : 1.24
 * Simulink Coder version         : 8.5 (R2013b) 08-Aug-2013
 * C/C++ source code generated on : Thu Dec  4 19:58:11 2014
 *
 * Target selection: ert.tlc
 * Embedded hardware selection: 32-bit Generic
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include <klee/klee.h>
#include "controller.h"

#include <stdio.h>                     /* This ert_main.c example uses printf/fflush */
#include "continuous_kobuna_FP.h"      /* Model's header file */
#include "rtwtypes.h"

static RT_MODEL_continuous_kobuna_FP_T continuous_kobuna_FP_M_;
static RT_MODEL_continuous_kobuna_FP_T *const continuous_kobuna_FP_M = &continuous_kobuna_FP_M_;            /* Real-time model */
static P_continuous_kobuna_FP_T continuous_kobuna_FP_P = {
  0,                                   /* Computed Parameter: Constant6_Value
                                        * Referenced by: '<S2>/Constant6'
                                        */
  1,                                   /* Computed Parameter: Constant_Value
                                        * Referenced by: '<S2>/Constant'
                                        */
  0,                                   /* Computed Parameter: Constant2_Value
                                        * Referenced by: '<S2>/Constant2'
                                        */
  1,                                   /* Computed Parameter: Constant1_Value
                                        * Referenced by: '<S2>/Constant1'
                                        */
  0,                                   /* Computed Parameter: Constant6_Value_e
                                        * Referenced by: '<S3>/Constant6'
                                        */
  1,                                   /* Computed Parameter: Constant_Value_g
                                        * Referenced by: '<S3>/Constant'
                                        */
  0,                                   /* Computed Parameter: Constant2_Value_m
                                        * Referenced by: '<S3>/Constant2'
                                        */
  1,                                   /* Computed Parameter: Constant1_Value_o
                                        * Referenced by: '<S3>/Constant1'
                                        */
  0,                                   /* Computed Parameter: Constant6_Value_b
                                        * Referenced by: '<S4>/Constant6'
                                        */
  1,                                   /* Computed Parameter: Constant_Value_j
                                        * Referenced by: '<S4>/Constant'
                                        */
  0,                                   /* Computed Parameter: Constant2_Value_e
                                        * Referenced by: '<S4>/Constant2'
                                        */
  1,                                   /* Computed Parameter: Constant1_Value_b
                                        * Referenced by: '<S4>/Constant1'
                                        */
  0,                                   /* Computed Parameter: Constant6_Value_k
                                        * Referenced by: '<S5>/Constant6'
                                        */
  1,                                   /* Computed Parameter: Constant_Value_n
                                        * Referenced by: '<S5>/Constant'
                                        */
  0,                                   /* Computed Parameter: Constant2_Value_a
                                        * Referenced by: '<S5>/Constant2'
                                        */
  1,                                   /* Computed Parameter: Constant1_Value_i
                                        * Referenced by: '<S5>/Constant1'
                                        */
  10,                                  /* Computed Parameter: Constant3_Value
                                        * Referenced by: '<S2>/Constant3'
                                        */
  0,                                   /* Computed Parameter: DiscreteTimeIntegrator_IC
                                        * Referenced by: '<S2>/Discrete-Time Integrator'
                                        */
  4,                                   /* Computed Parameter: Switch_Threshold
                                        * Referenced by: '<S2>/Switch'
                                        */
  90,                                  /* Computed Parameter: Constant4_Value
                                        * Referenced by: '<S2>/Constant4'
                                        */
  10,                                  /* Computed Parameter: Constant3_Value_b
                                        * Referenced by: '<S3>/Constant3'
                                        */
  0,                                   /* Computed Parameter: DiscreteTimeIntegrator_IC_c
                                        * Referenced by: '<S3>/Discrete-Time Integrator'
                                        */
  4,                                   /* Computed Parameter: Switch_Threshold_n
                                        * Referenced by: '<S3>/Switch'
                                        */
  90,                                  /* Computed Parameter: Constant4_Value_d
                                        * Referenced by: '<S3>/Constant4'
                                        */
  10,                                  /* Computed Parameter: Constant3_Value_o
                                        * Referenced by: '<S4>/Constant3'
                                        */
  0,                                   /* Computed Parameter: DiscreteTimeIntegrator_IC_p
                                        * Referenced by: '<S4>/Discrete-Time Integrator'
                                        */
  4,                                   /* Computed Parameter: Switch_Threshold_p
                                        * Referenced by: '<S4>/Switch'
                                        */
  90,                                  /* Computed Parameter: Constant4_Value_e
                                        * Referenced by: '<S4>/Constant4'
                                        */
  10,                                  /* Computed Parameter: Constant3_Value_p
                                        * Referenced by: '<S5>/Constant3'
                                        */
  0,                                   /* Computed Parameter: DiscreteTimeIntegrator_IC_m
                                        * Referenced by: '<S5>/Discrete-Time Integrator'
                                        */
  4,                                   /* Computed Parameter: Switch_Threshold_g
                                        * Referenced by: '<S5>/Switch'
                                        */
  90                                   /* Computed Parameter: Constant4_Value_h
                                        * Referenced by: '<S5>/Constant4'
                                        */
};                                     /* Modifiable parameters */

static DW_continuous_kobuna_FP_T continuous_kobuna_FP_DW;/* Observable states */
//static ExtU_continuous_kobuna_FP_T continuous_kobuna_FP_U;/* External inputs */
//static ExtY_continuous_kobuna_FP_T continuous_kobuna_FP_Y;/* External outputs */

/*
 * Associating rt_OneStep with a real-time clock or interrupt service routine
 * is what makes the generated code "real-time".  The function rt_OneStep is
 * always associated with the base rate of the model.  Subrates are managed
 * by the base rate from inside the generated code.  Enabling/disabling
 * interrupts and floating point context switches are target specific.  This
 * example code indicates where these should take place relative to executing
 * the generated code step function.  Overrun behavior should be tailored to
 * your application needs.  This example simply sets an error status in the
 * real-time model and returns from rt_OneStep.
 */
void rt_OneStep(RT_MODEL_continuous_kobuna_FP_T *const continuous_kobuna_FP_M, 
        ExtU_continuous_kobuna_FP_T* continuous_kobuna_FP_U, 
        ExtY_continuous_kobuna_FP_T* continuous_kobuna_FP_Y)
{
  static boolean_T OverrunFlag = 0;

  /* Disable interrupts here */

  /* Check for overrun */
  if (OverrunFlag) {
    rtmSetErrorStatus(continuous_kobuna_FP_M, "Overrun");
    return;
  }

  OverrunFlag = TRUE;

  /* Save FPU context here (if necessary) */
  /* Re-enable timer or interrupt here */
  /* Set model inputs here */

  /* Step the model */
  continuous_kobuna_FP_step(continuous_kobuna_FP_M, continuous_kobuna_FP_U, continuous_kobuna_FP_Y);

  /* Get model outputs here */

  /* Indicate task complete */
  OverrunFlag = FALSE;

  /* Disable interrupts here */
  /* Restore FPU context here (if necessary) */
  /* Enable interrupts here */
}

/*
 * The example "main" function illustrates what is required by your
 * application code to initialize, execute, and terminate the generated code.
 * Attaching rt_OneStep to a real-time clock is target specific.  This example
 * illustates how you do this relative to initializing the model.
 */

void controller_init()
{
  /* Pack model data into RTM */
  continuous_kobuna_FP_M->ModelData.defaultParam = &continuous_kobuna_FP_P;
  continuous_kobuna_FP_M->ModelData.dwork = &continuous_kobuna_FP_DW;

  /* Initialize model */
//  continuous_kobuna_FP_initialize(continuous_kobuna_FP_M,
//    &continuous_kobuna_FP_U, &continuous_kobuna_FP_Y);
}

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
{
  /* Attach rt_OneStep to a timer or interrupt service routine with
   * period 1.0 seconds (the model's base sample time) here.  The
   * call syntax for rt_OneStep is
   *
   *  rt_OneStep(continuous_kobuna_FP_M);
   */
//  rt_OneStep(continuous_kobuna_FP_M);

  ExtU_continuous_kobuna_FP_T continuous_kobuna_FP_U;/* External inputs */
  ExtY_continuous_kobuna_FP_T continuous_kobuna_FP_Y;/* External outputs */
/*
  continuous_kobuna_FP_U->s_u1 = &(input->input_arr[0]);
  continuous_kobuna_FP_U->s_u2 = &(input->input_arr[1]);
  continuous_kobuna_FP_U->s_u3 = &(input->input_arr[2]);
  continuous_kobuna_FP_U->s_u4 = &(input->input_arr[3]);
  continuous_kobuna_FP_U->s_u5 = &(input->input_arr[4]);
  continuous_kobuna_FP_U->s_u6 = &(input->input_arr[5]);
  continuous_kobuna_FP_U->s_u7 = &(input->input_arr[6]);
  continuous_kobuna_FP_U->s_u8 = &(input->input_arr[7]);

  continuous_kobuna_FP_Y->Out1 = &(ret_val->output_arr[0]);
*/

  continuous_kobuna_FP_U.s_u1 = (input->input_arr[0]);
  continuous_kobuna_FP_U.s_u2 = (input->input_arr[1]);
  continuous_kobuna_FP_U.s_u3 = (input->input_arr[2]);
  continuous_kobuna_FP_U.s_u4 = (input->input_arr[3]);
  continuous_kobuna_FP_U.s_u5 = (input->input_arr[4]);
  continuous_kobuna_FP_U.s_u6 = (input->input_arr[5]);
  continuous_kobuna_FP_U.s_u7 = (input->input_arr[6]);
  continuous_kobuna_FP_U.s_u8 = (input->input_arr[7]);

  rt_OneStep(continuous_kobuna_FP_M, &continuous_kobuna_FP_U, &continuous_kobuna_FP_Y);

  ret_val->output_arr[0] = continuous_kobuna_FP_Y.Out1;

//  while (rtmGetErrorStatus(continuous_kobuna_FP_M) == (NULL)) {
//    /*  Perform other application tasks here */
//  }

}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
