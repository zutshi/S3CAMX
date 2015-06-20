/*
 * File: continuous_kobuna_FP.c
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

#include "continuous_kobuna_FP.h"

/* Model step function */
void continuous_kobuna_FP_step(RT_MODEL_continuous_kobuna_FP_T *const
  continuous_kobuna_FP_M, ExtU_continuous_kobuna_FP_T *continuous_kobuna_FP_U,
  ExtY_continuous_kobuna_FP_T *continuous_kobuna_FP_Y)
{
  P_continuous_kobuna_FP_T *continuous_kobuna_FP_P = ((P_continuous_kobuna_FP_T *)
    continuous_kobuna_FP_M->ModelData.defaultParam);
  DW_continuous_kobuna_FP_T *continuous_kobuna_FP_DW =
    ((DW_continuous_kobuna_FP_T *) continuous_kobuna_FP_M->ModelData.dwork);

  /* local block i/o variables */
  boolean_T rtb_RelationalOperator;
  boolean_T rtb_RelationalOperator_i;
  boolean_T rtb_RelationalOperator_j;
  boolean_T rtb_RelationalOperator_l;
  int32_T tmp;
  int32_T tmp_0;
  int32_T tmp_1;
  int32_T tmp_2;

  /* RelationalOperator: '<S2>/Relational Operator' incorporates:
   *  Constant: '<S2>/Constant3'
   *  Inport: '<Root>/u1'
   */
  rtb_RelationalOperator = (continuous_kobuna_FP_U->s_u1 <=
    continuous_kobuna_FP_P->Constant3_Value);

  /* DiscreteIntegrator: '<S2>/Discrete-Time Integrator' */
  if ((!rtb_RelationalOperator) &&
      (continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRese == 1)) {
    continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE =
      continuous_kobuna_FP_P->DiscreteTimeIntegrator_IC;
  }

  /* RelationalOperator: '<S3>/Relational Operator' incorporates:
   *  Constant: '<S3>/Constant3'
   *  Inport: '<Root>/u3'
   */
  rtb_RelationalOperator_i = (continuous_kobuna_FP_U->s_u3 <=
    continuous_kobuna_FP_P->Constant3_Value_b);

  /* DiscreteIntegrator: '<S3>/Discrete-Time Integrator' */
  if ((!rtb_RelationalOperator_i) &&
      (continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRe_b == 1)) {
    continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE_f =
      continuous_kobuna_FP_P->DiscreteTimeIntegrator_IC_c;
  }

  /* RelationalOperator: '<S4>/Relational Operator' incorporates:
   *  Constant: '<S4>/Constant3'
   *  Inport: '<Root>/u5'
   */
  rtb_RelationalOperator_j = (continuous_kobuna_FP_U->s_u5 <=
    continuous_kobuna_FP_P->Constant3_Value_o);

  /* DiscreteIntegrator: '<S4>/Discrete-Time Integrator' */
  if ((!rtb_RelationalOperator_j) &&
      (continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRe_f == 1)) {
    continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE_h =
      continuous_kobuna_FP_P->DiscreteTimeIntegrator_IC_p;
  }

  /* RelationalOperator: '<S5>/Relational Operator' incorporates:
   *  Constant: '<S5>/Constant3'
   *  Inport: '<Root>/u7'
   */
  rtb_RelationalOperator_l = (continuous_kobuna_FP_U->s_u7 <=
    continuous_kobuna_FP_P->Constant3_Value_p);

  /* DiscreteIntegrator: '<S5>/Discrete-Time Integrator' */
  if ((!rtb_RelationalOperator_l) &&
      (continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRe_n == 1)) {
    continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE_l =
      continuous_kobuna_FP_P->DiscreteTimeIntegrator_IC_m;
  }

  /* Switch: '<S2>/Switch' incorporates:
   *  Constant: '<S2>/Constant1'
   *  Constant: '<S2>/Constant2'
   *  DiscreteIntegrator: '<S2>/Discrete-Time Integrator'
   */
  if (continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE >=
      continuous_kobuna_FP_P->Switch_Threshold) {
    tmp = continuous_kobuna_FP_P->Constant1_Value;
  } else {
    tmp = continuous_kobuna_FP_P->Constant2_Value;
  }

  /* End of Switch: '<S2>/Switch' */

  /* Switch: '<S3>/Switch' incorporates:
   *  Constant: '<S3>/Constant1'
   *  Constant: '<S3>/Constant2'
   *  DiscreteIntegrator: '<S3>/Discrete-Time Integrator'
   */
  if (continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE_f >=
      continuous_kobuna_FP_P->Switch_Threshold_n) {
    tmp_0 = continuous_kobuna_FP_P->Constant1_Value_o;
  } else {
    tmp_0 = continuous_kobuna_FP_P->Constant2_Value_m;
  }

  /* End of Switch: '<S3>/Switch' */

  /* Switch: '<S4>/Switch' incorporates:
   *  Constant: '<S4>/Constant1'
   *  Constant: '<S4>/Constant2'
   *  DiscreteIntegrator: '<S4>/Discrete-Time Integrator'
   */
  if (continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE_h >=
      continuous_kobuna_FP_P->Switch_Threshold_p) {
    tmp_1 = continuous_kobuna_FP_P->Constant1_Value_b;
  } else {
    tmp_1 = continuous_kobuna_FP_P->Constant2_Value_e;
  }

  /* End of Switch: '<S4>/Switch' */

  /* Switch: '<S5>/Switch' incorporates:
   *  Constant: '<S5>/Constant1'
   *  Constant: '<S5>/Constant2'
   *  DiscreteIntegrator: '<S5>/Discrete-Time Integrator'
   */
  if (continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE_l >=
      continuous_kobuna_FP_P->Switch_Threshold_g) {
    tmp_2 = continuous_kobuna_FP_P->Constant1_Value_i;
  } else {
    tmp_2 = continuous_kobuna_FP_P->Constant2_Value_a;
  }

  /* End of Switch: '<S5>/Switch' */

  /* Outport: '<Root>/Out1' incorporates:
   *  Constant: '<S2>/Constant4'
   *  Constant: '<S3>/Constant4'
   *  Constant: '<S4>/Constant4'
   *  Constant: '<S5>/Constant4'
   *  Inport: '<Root>/u2'
   *  Inport: '<Root>/u4'
   *  Inport: '<Root>/u6'
   *  Inport: '<Root>/u8'
   *  Logic: '<S1>/Logical Operator'
   *  Logic: '<S2>/Logical Operator'
   *  Logic: '<S3>/Logical Operator'
   *  Logic: '<S4>/Logical Operator'
   *  Logic: '<S5>/Logical Operator'
   *  RelationalOperator: '<S2>/Relational Operator1'
   *  RelationalOperator: '<S3>/Relational Operator1'
   *  RelationalOperator: '<S4>/Relational Operator1'
   *  RelationalOperator: '<S5>/Relational Operator1'
   */
  continuous_kobuna_FP_Y->Out1 = ((tmp != 0) && (continuous_kobuna_FP_U->s_u2 >=
    continuous_kobuna_FP_P->Constant4_Value) && ((tmp_0 != 0) &&
    (continuous_kobuna_FP_U->s_u4 >= continuous_kobuna_FP_P->Constant4_Value_d))
    && ((tmp_1 != 0) && (continuous_kobuna_FP_U->s_u6 >=
    continuous_kobuna_FP_P->Constant4_Value_e)) && ((tmp_2 != 0) &&
    (continuous_kobuna_FP_U->s_u8 >= continuous_kobuna_FP_P->Constant4_Value_h)));

  /* Switch: '<S2>/Switch1' incorporates:
   *  Constant: '<S2>/Constant'
   *  Constant: '<S2>/Constant6'
   */
  if (rtb_RelationalOperator) {
    tmp = continuous_kobuna_FP_P->Constant_Value;
  } else {
    tmp = continuous_kobuna_FP_P->Constant6_Value;
  }

  /* End of Switch: '<S2>/Switch1' */

  /* Update for DiscreteIntegrator: '<S2>/Discrete-Time Integrator' */
  continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE += tmp;
  if (rtb_RelationalOperator) {
    continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRese = 1;
  } else {
    continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRese = 0;
  }

  /* End of Update for DiscreteIntegrator: '<S2>/Discrete-Time Integrator' */

  /* Switch: '<S3>/Switch1' incorporates:
   *  Constant: '<S3>/Constant'
   *  Constant: '<S3>/Constant6'
   */
  if (rtb_RelationalOperator_i) {
    tmp = continuous_kobuna_FP_P->Constant_Value_g;
  } else {
    tmp = continuous_kobuna_FP_P->Constant6_Value_e;
  }

  /* End of Switch: '<S3>/Switch1' */

  /* Update for DiscreteIntegrator: '<S3>/Discrete-Time Integrator' */
  continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE_f += tmp;
  if (rtb_RelationalOperator_i) {
    continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRe_b = 1;
  } else {
    continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRe_b = 0;
  }

  /* End of Update for DiscreteIntegrator: '<S3>/Discrete-Time Integrator' */

  /* Switch: '<S4>/Switch1' incorporates:
   *  Constant: '<S4>/Constant'
   *  Constant: '<S4>/Constant6'
   */
  if (rtb_RelationalOperator_j) {
    tmp = continuous_kobuna_FP_P->Constant_Value_j;
  } else {
    tmp = continuous_kobuna_FP_P->Constant6_Value_b;
  }

  /* End of Switch: '<S4>/Switch1' */

  /* Update for DiscreteIntegrator: '<S4>/Discrete-Time Integrator' */
  continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE_h += tmp;
  if (rtb_RelationalOperator_j) {
    continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRe_f = 1;
  } else {
    continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRe_f = 0;
  }

  /* End of Update for DiscreteIntegrator: '<S4>/Discrete-Time Integrator' */

  /* Switch: '<S5>/Switch1' incorporates:
   *  Constant: '<S5>/Constant'
   *  Constant: '<S5>/Constant6'
   */
  if (rtb_RelationalOperator_l) {
    tmp = continuous_kobuna_FP_P->Constant_Value_n;
  } else {
    tmp = continuous_kobuna_FP_P->Constant6_Value_k;
  }

  /* End of Switch: '<S5>/Switch1' */

  /* Update for DiscreteIntegrator: '<S5>/Discrete-Time Integrator' */
  continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE_l += tmp;
  if (rtb_RelationalOperator_l) {
    continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRe_n = 1;
  } else {
    continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRe_n = 0;
  }

  /* End of Update for DiscreteIntegrator: '<S5>/Discrete-Time Integrator' */
}

/* Model initialize function */
void continuous_kobuna_FP_initialize(RT_MODEL_continuous_kobuna_FP_T *const
  continuous_kobuna_FP_M, ExtU_continuous_kobuna_FP_T *continuous_kobuna_FP_U,
  ExtY_continuous_kobuna_FP_T *continuous_kobuna_FP_Y)
{
  P_continuous_kobuna_FP_T *continuous_kobuna_FP_P = ((P_continuous_kobuna_FP_T *)
    continuous_kobuna_FP_M->ModelData.defaultParam);
  DW_continuous_kobuna_FP_T *continuous_kobuna_FP_DW =
    ((DW_continuous_kobuna_FP_T *) continuous_kobuna_FP_M->ModelData.dwork);

  /* Registration code */

  /* states (dwork) */
  (void) memset((void *)continuous_kobuna_FP_DW, 0,
                sizeof(DW_continuous_kobuna_FP_T));

  /* external inputs */
  (void) memset((void *)continuous_kobuna_FP_U, 0,
                sizeof(ExtU_continuous_kobuna_FP_T));

  /* external outputs */
  continuous_kobuna_FP_Y->Out1 = FALSE;

  /* InitializeConditions for DiscreteIntegrator: '<S2>/Discrete-Time Integrator' */
  continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE =
    continuous_kobuna_FP_P->DiscreteTimeIntegrator_IC;
  continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRese = 2;

  /* InitializeConditions for DiscreteIntegrator: '<S3>/Discrete-Time Integrator' */
  continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE_f =
    continuous_kobuna_FP_P->DiscreteTimeIntegrator_IC_c;
  continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRe_b = 2;

  /* InitializeConditions for DiscreteIntegrator: '<S4>/Discrete-Time Integrator' */
  continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE_h =
    continuous_kobuna_FP_P->DiscreteTimeIntegrator_IC_p;
  continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRe_f = 2;

  /* InitializeConditions for DiscreteIntegrator: '<S5>/Discrete-Time Integrator' */
  continuous_kobuna_FP_DW->DiscreteTimeIntegrator_DSTATE_l =
    continuous_kobuna_FP_P->DiscreteTimeIntegrator_IC_m;
  continuous_kobuna_FP_DW->DiscreteTimeIntegrator_PrevRe_n = 2;
}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
