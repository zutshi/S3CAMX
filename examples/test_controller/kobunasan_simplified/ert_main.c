/*
 * File: ert_main.c
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


#include "controller.h"
#include <stdio.h>                     /* This ert_main.c example uses printf/fflush */
#include "continuous_kobuna_simpleFP.h" /* Model's header file */
#include "rtwtypes.h"

static RT_MODEL_continuous_kobuna_si_T continuous_kobuna_simpleFP_M_;
static RT_MODEL_continuous_kobuna_si_T *const continuous_kobuna_simpleFP_M = &continuous_kobuna_simpleFP_M_;      /* Real-time model */
static P_continuous_kobuna_simpleFP_T continuous_kobuna_simpleFP_P = {
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
  90                                   /* Computed Parameter: Constant4_Value_d
                                        * Referenced by: '<S3>/Constant4'
                                        */
};                                     /* Modifiable parameters */

static DW_continuous_kobuna_simpleFP_T continuous_kobuna_simpleFP_DW;/* Observable states */
//static ExtU_continuous_kobuna_simple_T continuous_kobuna_simpleFP_U;/* External inputs */
//static ExtY_continuous_kobuna_simple_T continuous_kobuna_simpleFP_Y;/* External outputs */

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
void rt_OneStep(RT_MODEL_continuous_kobuna_si_T *const continuous_kobuna_simpleFP_M,
        ExtU_continuous_kobuna_simple_T* continuous_kobuna_simpleFP_U,
        ExtY_continuous_kobuna_simple_T* continuous_kobuna_simpleFP_Y)
{
  static boolean_T OverrunFlag = 0;

  /* Disable interrupts here */

  /* Check for overrun */
  if (OverrunFlag) {
    rtmSetErrorStatus(continuous_kobuna_simpleFP_M, "Overrun");
    return;
  }

  OverrunFlag = TRUE;

  /* Save FPU context here (if necessary) */
  /* Re-enable timer or interrupt here */
  /* Set model inputs here */

  /* Step the model */
  continuous_kobuna_simpleFP_step(continuous_kobuna_simpleFP_M, continuous_kobuna_simpleFP_U, continuous_kobuna_simpleFP_Y);

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
  continuous_kobuna_simpleFP_M->ModelData.defaultParam = &continuous_kobuna_simpleFP_P;
  continuous_kobuna_simpleFP_M->ModelData.dwork = &continuous_kobuna_simpleFP_DW;

}

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
{

  ExtU_continuous_kobuna_simple_T continuous_kobuna_simpleFP_U;/* External inputs */
  ExtY_continuous_kobuna_simple_T continuous_kobuna_simpleFP_Y;/* External outputs */

  continuous_kobuna_simpleFP_U.s_u1 = (input->input_arr[0]);
  continuous_kobuna_simpleFP_U.s_u2 = (input->input_arr[1]);
  continuous_kobuna_simpleFP_U.s_u3 = (input->input_arr[2]);
  continuous_kobuna_simpleFP_U.s_u4 = (input->input_arr[3]);

// controller state
#if MODE == UNROLL
  // no need to expose the state or do anything special
#elif MODE == CONCOLIC
  // expose all internal states!
  continuous_kobuna_simpleFP_M->ModelData.dwork->DiscreteTimeIntegrator_DSTATE = input->state_arr[0];/* '<S2>/Discrete-Time Integrator' */
  continuous_kobuna_simpleFP_M->ModelData.dwork->DiscreteTimeIntegrator_DSTATE_f = input->state_arr[1];/* '<S3>/Discrete-Time Integrator' */
  continuous_kobuna_simpleFP_M->ModelData.dwork->DiscreteTimeIntegrator_PrevRese = input->state_arr[2];/* '<S2>/Discrete-Time Integrator' */
  continuous_kobuna_simpleFP_M->ModelData.dwork->DiscreteTimeIntegrator_PrevRe_b = input->state_arr[3];/* '<S3>/Discrete-Time Integrator' */
#elif MODE == SYMBOLIC
  //same as concolic
  continuous_kobuna_simpleFP_M->ModelData.dwork->DiscreteTimeIntegrator_DSTATE = input->state_arr[0];/* '<S2>/Discrete-Time Integrator' */
  continuous_kobuna_simpleFP_M->ModelData.dwork->DiscreteTimeIntegrator_DSTATE_f = input->state_arr[1];/* '<S3>/Discrete-Time Integrator' */
  continuous_kobuna_simpleFP_M->ModelData.dwork->DiscreteTimeIntegrator_PrevRese = input->state_arr[2];/* '<S2>/Discrete-Time Integrator' */
  continuous_kobuna_simpleFP_M->ModelData.dwork->DiscreteTimeIntegrator_PrevRe_b = input->state_arr[3];/* '<S3>/Discrete-Time Integrator' */
#else
"I can not be compiled"
#endif
  rt_OneStep(continuous_kobuna_simpleFP_M, &continuous_kobuna_simpleFP_U, &continuous_kobuna_simpleFP_Y);

  ret_val->state_arr[0] = continuous_kobuna_simpleFP_M->ModelData.dwork->DiscreteTimeIntegrator_DSTATE;/* '<S2>/Discrete-Time Integrator' */
  ret_val->state_arr[1] = continuous_kobuna_simpleFP_M->ModelData.dwork->DiscreteTimeIntegrator_DSTATE_f;/* '<S3>/Discrete-Time Integrator' */
  ret_val->state_arr[2] = continuous_kobuna_simpleFP_M->ModelData.dwork->DiscreteTimeIntegrator_PrevRese;/* '<S2>/Discrete-Time Integrator' */
  ret_val->state_arr[3] = continuous_kobuna_simpleFP_M->ModelData.dwork->DiscreteTimeIntegrator_PrevRe_b;/* '<S3>/Discrete-Time Integrator' */

  ret_val->output_arr[0] = (int)continuous_kobuna_simpleFP_Y.Out1;
  return (void*)0;
}


/*
 * File trailer for generated code.
 *
 * [EOF]
 */
