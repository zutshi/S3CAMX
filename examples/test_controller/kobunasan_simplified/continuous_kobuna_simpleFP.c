/*
 * File: continuous_kobuna_simpleFP.c
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

#include "continuous_kobuna_simpleFP.h"

/* Model step function */
void continuous_kobuna_simpleFP_step(RT_MODEL_continuous_kobuna_si_T *const
  continuous_kobuna_simpleFP_M, ExtU_continuous_kobuna_simple_T
  *continuous_kobuna_simpleFP_U, ExtY_continuous_kobuna_simple_T
  *continuous_kobuna_simpleFP_Y)
{
  P_continuous_kobuna_simpleFP_T *continuous_kobuna_simpleFP_P =
    ((P_continuous_kobuna_simpleFP_T *)
     continuous_kobuna_simpleFP_M->ModelData.defaultParam);
  DW_continuous_kobuna_simpleFP_T *continuous_kobuna_simpleFP_DW =
    ((DW_continuous_kobuna_simpleFP_T *)
     continuous_kobuna_simpleFP_M->ModelData.dwork);

  /* local block i/o variables */
  boolean_T rtb_RelationalOperator;
  boolean_T rtb_RelationalOperator_i;
  int32_T tmp;
  int32_T tmp_0;

  /* RelationalOperator: '<S2>/Relational Operator' incorporates:
   *  Constant: '<S2>/Constant3'
   *  Inport: '<Root>/u1'
   */
  rtb_RelationalOperator = (continuous_kobuna_simpleFP_U->s_u1 <=
    continuous_kobuna_simpleFP_P->Constant3_Value);

  /* DiscreteIntegrator: '<S2>/Discrete-Time Integrator' */
  if ((!rtb_RelationalOperator) &&
      (continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_PrevRese == 1)) {
    continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_DSTATE =
      continuous_kobuna_simpleFP_P->DiscreteTimeIntegrator_IC;
  }

  /* RelationalOperator: '<S3>/Relational Operator' incorporates:
   *  Constant: '<S3>/Constant3'
   *  Inport: '<Root>/u3'
   */
  rtb_RelationalOperator_i = (continuous_kobuna_simpleFP_U->s_u3 <=
    continuous_kobuna_simpleFP_P->Constant3_Value_b);

  /* DiscreteIntegrator: '<S3>/Discrete-Time Integrator' */
  if ((!rtb_RelationalOperator_i) &&
      (continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_PrevRe_b == 1)) {
    continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_DSTATE_f =
      continuous_kobuna_simpleFP_P->DiscreteTimeIntegrator_IC_c;
  }

  /* Switch: '<S2>/Switch' incorporates:
   *  Constant: '<S2>/Constant1'
   *  Constant: '<S2>/Constant2'
   *  DiscreteIntegrator: '<S2>/Discrete-Time Integrator'
   */
  if (continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_DSTATE >=
      continuous_kobuna_simpleFP_P->Switch_Threshold) {
    tmp = continuous_kobuna_simpleFP_P->Constant1_Value;
  } else {
    tmp = continuous_kobuna_simpleFP_P->Constant2_Value;
  }

  /* End of Switch: '<S2>/Switch' */

  /* Switch: '<S3>/Switch' incorporates:
   *  Constant: '<S3>/Constant1'
   *  Constant: '<S3>/Constant2'
   *  DiscreteIntegrator: '<S3>/Discrete-Time Integrator'
   */
  if (continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_DSTATE_f >=
      continuous_kobuna_simpleFP_P->Switch_Threshold_n) {
    tmp_0 = continuous_kobuna_simpleFP_P->Constant1_Value_o;
  } else {
    tmp_0 = continuous_kobuna_simpleFP_P->Constant2_Value_m;
  }

  /* End of Switch: '<S3>/Switch' */

  /* Outport: '<Root>/Out1' incorporates:
   *  Constant: '<S2>/Constant4'
   *  Constant: '<S3>/Constant4'
   *  Inport: '<Root>/u2'
   *  Inport: '<Root>/u4'
   *  Logic: '<S1>/Logical Operator'
   *  Logic: '<S2>/Logical Operator'
   *  Logic: '<S3>/Logical Operator'
   *  RelationalOperator: '<S2>/Relational Operator1'
   *  RelationalOperator: '<S3>/Relational Operator1'
   */
  continuous_kobuna_simpleFP_Y->Out1 = ((tmp != 0) &&
    (continuous_kobuna_simpleFP_U->s_u2 >=
     continuous_kobuna_simpleFP_P->Constant4_Value) && ((tmp_0 != 0) &&
    (continuous_kobuna_simpleFP_U->s_u4 >=
     continuous_kobuna_simpleFP_P->Constant4_Value_d)));

  /* Switch: '<S2>/Switch1' incorporates:
   *  Constant: '<S2>/Constant'
   *  Constant: '<S2>/Constant6'
   */
  if (rtb_RelationalOperator) {
    tmp = continuous_kobuna_simpleFP_P->Constant_Value;
  } else {
    tmp = continuous_kobuna_simpleFP_P->Constant6_Value;
  }

  /* End of Switch: '<S2>/Switch1' */

  /* Update for DiscreteIntegrator: '<S2>/Discrete-Time Integrator' */
  continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_DSTATE += tmp;
  if (rtb_RelationalOperator) {
    continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_PrevRese = 1;
  } else {
    continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_PrevRese = 0;
  }

  /* End of Update for DiscreteIntegrator: '<S2>/Discrete-Time Integrator' */

  /* Switch: '<S3>/Switch1' incorporates:
   *  Constant: '<S3>/Constant'
   *  Constant: '<S3>/Constant6'
   */
  if (rtb_RelationalOperator_i) {
    tmp = continuous_kobuna_simpleFP_P->Constant_Value_g;
  } else {
    tmp = continuous_kobuna_simpleFP_P->Constant6_Value_e;
  }

  /* End of Switch: '<S3>/Switch1' */

  /* Update for DiscreteIntegrator: '<S3>/Discrete-Time Integrator' */
  continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_DSTATE_f += tmp;
  if (rtb_RelationalOperator_i) {
    continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_PrevRe_b = 1;
  } else {
    continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_PrevRe_b = 0;
  }

  /* End of Update for DiscreteIntegrator: '<S3>/Discrete-Time Integrator' */
}

/* Model initialize function */
void continuous_kobuna_simpleFP_initialize(RT_MODEL_continuous_kobuna_si_T *
  const continuous_kobuna_simpleFP_M, ExtU_continuous_kobuna_simple_T
  *continuous_kobuna_simpleFP_U, ExtY_continuous_kobuna_simple_T
  *continuous_kobuna_simpleFP_Y)
{
  P_continuous_kobuna_simpleFP_T *continuous_kobuna_simpleFP_P =
    ((P_continuous_kobuna_simpleFP_T *)
     continuous_kobuna_simpleFP_M->ModelData.defaultParam);
  DW_continuous_kobuna_simpleFP_T *continuous_kobuna_simpleFP_DW =
    ((DW_continuous_kobuna_simpleFP_T *)
     continuous_kobuna_simpleFP_M->ModelData.dwork);

  /* Registration code */

  /* states (dwork) */
  (void) memset((void *)continuous_kobuna_simpleFP_DW, 0,
                sizeof(DW_continuous_kobuna_simpleFP_T));

  /* external inputs */
  (void) memset((void *)continuous_kobuna_simpleFP_U, 0,
                sizeof(ExtU_continuous_kobuna_simple_T));

  /* external outputs */
  continuous_kobuna_simpleFP_Y->Out1 = FALSE;

  /* InitializeConditions for DiscreteIntegrator: '<S2>/Discrete-Time Integrator' */
  continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_DSTATE =
    continuous_kobuna_simpleFP_P->DiscreteTimeIntegrator_IC;
  continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_PrevRese = 2;

  /* InitializeConditions for DiscreteIntegrator: '<S3>/Discrete-Time Integrator' */
  continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_DSTATE_f =
    continuous_kobuna_simpleFP_P->DiscreteTimeIntegrator_IC_c;
  continuous_kobuna_simpleFP_DW->DiscreteTimeIntegrator_PrevRe_b = 2;
}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
