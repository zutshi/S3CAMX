/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * File: ert_main.c
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

//#include <stddef.h>
//#include <stdio.h>                     /* This ert_main.c example uses printf/fflush */
#include "shift_controller.h"          /* Model's header file */
#include "rtwtypes.h"
#include "controller.h"

static RT_MODEL_shift_controller_T shift_controller_M_;
static RT_MODEL_shift_controller_T *const shift_controller_M =
  &shift_controller_M_;                /* Real-time model */
static P_shift_controller_T shift_controller_P = {
  0.0,                                 /* Expression: 0
                                        * Referenced by: '<S3>/down_th'
                                        */
  0.0,                                 /* Expression: 0
                                        * Referenced by: '<S3>/up_th'
                                        */

  /*  Expression: DOWN_TABLE
   * Referenced by: '<S3>/InterpDown'
   */
  { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 5.0, 5.0, 5.0, 30.0, 30.0, 20.0, 20.0,
    25.0, 30.0, 50.0, 50.0, 35.0, 35.0, 40.0, 50.0, 80.0, 80.0 },

  /*  Expression: DOWN_TH_BP
   * Referenced by: '<S3>/InterpDown'
   */
  { 0.0, 5.0, 40.0, 50.0, 90.0, 100.0 },

  /*  Expression: [1:4]
   * Referenced by: '<S3>/InterpDown'
   */
  { 1.0, 2.0, 3.0, 4.0 },

  /*  Expression: UP_TABLE
   * Referenced by: '<S3>/InterpUp'
   */
  { 10.0, 10.0, 15.0, 23.0, 40.0, 40.0, 30.0, 30.0, 30.0, 41.0, 70.0, 70.0, 50.0,
    50.0, 50.0, 60.0, 100.0, 100.0, 1.0E+6, 1.0E+6, 1.0E+6, 1.0E+6, 1.0E+6,
    1.0E+6 },

  /*  Expression: UP_TH_BP
   * Referenced by: '<S3>/InterpUp'
   */
  { 0.0, 25.0, 35.0, 50.0, 90.0, 100.0 },

  /*  Expression: [1:4]
   * Referenced by: '<S3>/InterpUp'
   */
  { 1.0, 2.0, 3.0, 4.0 },
  2.0,                                 /* Expression: TWAIT
                                        * Referenced by: '<S1>/ShiftLogic'
                                        */

  /*  Computed Parameter: InterpDown_maxIndex
   * Referenced by: '<S3>/InterpDown'
   */
  { 5U, 3U },

  /*  Computed Parameter: InterpUp_maxIndex
   * Referenced by: '<S3>/InterpUp'
   */
  { 5U, 3U }
};                                     /* Modifiable parameters */

static DW_shift_controller_T shift_controller_DW;/* Observable states */
static ExtU_shift_controller_T shift_controller_U;/* External inputs */
static ExtY_shift_controller_T shift_controller_Y;/* External outputs */

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
void rt_OneStep(RT_MODEL_shift_controller_T *const shift_controller_M);
void rt_OneStep(RT_MODEL_shift_controller_T *const shift_controller_M)
{
  static boolean_T OverrunFlag = false;

  /* Disable interrupts here */

  /* Check for overrun */
  if (OverrunFlag) {
    rtmSetErrorStatus(shift_controller_M, "Overrun");
    return;
  }

  OverrunFlag = true;

  /* Save FPU context here (if necessary) */
  /* Re-enable timer or interrupt here */
  /* Set model inputs here */

  /* Step the model */
  shift_controller_step(shift_controller_M, &shift_controller_U,
                        &shift_controller_Y);

  /* Get model outputs here */

  /* Indicate task complete */
  OverrunFlag = false;

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
/*
int_T main(int_T argc, const char *argv[])
{
  (void)(argc);
  (void)(argv);

  shift_controller_M->ModelData.defaultParam = &shift_controller_P;
  shift_controller_M->ModelData.dwork = &shift_controller_DW;

  shift_controller_initialize(shift_controller_M, &shift_controller_U,
    &shift_controller_Y);

  printf("Warning: The simulation will run forever. "
         "Generated ERT main won't simulate model step behavior. "
         "To change this behavior select the 'MAT-file logging' option.\n");
  fflush((NULL));
  while (rtmGetErrorStatus(shift_controller_M) == (NULL)) {
  }

  return 0;
}*/
void controller_init(){
  shift_controller_M->ModelData.defaultParam = &shift_controller_P;
  shift_controller_M->ModelData.dwork = &shift_controller_DW;

  /* Initialize model */
  shift_controller_initialize(shift_controller_M, &shift_controller_U,
    &shift_controller_Y);
}

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
{

  shift_controller_U.VehicleSpeed = input->x_arr[0];

  // Throttle
  shift_controller_U.disturbance[0] = input->input_arr[0];
  // Brake
  shift_controller_U.disturbance[1] = input->input_arr[1];
  

  rt_OneStep(shift_controller_M);

  ret_val->output_arr[0] = shift_controller_Y.Gear;
  ret_val->output_arr[1] = shift_controller_Y.throttle_op;
  ret_val->output_arr[2] = shift_controller_Y.brake_op;

  return (void*)0;
}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
