//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: artificial_pancreas.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//

// Include Files
#include "artificial_pancreas.h"
#include "artificial_pancreas_emxutil.h"
#include "simDallaManModel.h"
#include "ode45.h"
#include "computeInsulinOnBoard.h"
#include <stdio.h>

// Function Declarations
static void simulatePIDSystem(const double simParams_mealTimes[2], const double
  simParams_mealCarbs[2], const double simParams_bolusTimes[2], const double
  simParams_bolusAmts[2], double simParams_openLoopBasal, double
  simParams_controllerStartTime, double simParams_totalSimulationTime, double
  simParams_startingGlucose, double timeElapsed, double isPIDInitialized, double
  D[24], const double XX[3], double t_start, double T_end, double I, double *tt,
  emxArray_real_T *times, double YY[3], emxArray_real_T *YY_);

// Function Definitions

//
// 1. Get the meal rate of appearance.
// Arguments    : const double simParams_mealTimes[2]
//                const double simParams_mealCarbs[2]
//                const double simParams_bolusTimes[2]
//                const double simParams_bolusAmts[2]
//                double simParams_openLoopBasal
//                double simParams_controllerStartTime
//                double simParams_totalSimulationTime
//                double simParams_startingGlucose
//                double timeElapsed
//                double isPIDInitialized
//                double D[24]
//                const double XX[3]
//                double t_start
//                double T_end
//                double I
//                double *tt
//                emxArray_real_T *times
//                double YY[3]
//                emxArray_real_T *YY_
// Return Type  : void
//
static void simulatePIDSystem(const double simParams_mealTimes[2], const double
  simParams_mealCarbs[2], const double simParams_bolusTimes[2], const double
  simParams_bolusAmts[2], double simParams_openLoopBasal, double
  simParams_controllerStartTime, double simParams_totalSimulationTime, double
  simParams_startingGlucose, double timeElapsed, double isPIDInitialized, double
  D[24], const double XX[3], double t_start, double T_end, double I, double *tt,
  emxArray_real_T *times, double YY[3], emxArray_real_T *YY_)
{
  double mealData_times[2];
  double mealData_carbs[2];
  int i;
  emxArray_real_T *mealRA_times;
  emxArray_real_T *RATimes;
  emxArray_real_T *intrnlValues;
  emxArray_real_T *x;
  double dv13[2];
  int i7;
  emxArray_real_T *mealRA_values;
  double insulinBolus_times[2];
  double insulinBolus_values[2];
  unsigned int sz;
  double curState_data[10];
  emxArray_real_T *gValues;
  emxArray_real_T *gsValues;
  emxArray_real_T *iValues;
  double params_Gpb;
  double clBasal_times[2];
  double clBasal_values[2];
  double dv14[10];
  int curState_size[2];
  double b_curState_data[10];
  double curGs;
  double curTime;
  double ctrlState_oldG;
  double ctrlState_Kp;
  double ctrlState_Td;
  double ctrlState_Ti;
  double ctrlState_insulinMax;
  double ctrlState_I;
  double ctrlState_target;
  double ctrlState_dt;
  double ctrlState_gamma;
  emxArray_real_T *gsOut;
  emxArray_int32_T *r0;
  emxArray_real_T *T;
  emxArray_real_T *b_x;
  int loop_ub;
  double times_data[100];
  int times_size[1];
  double iValues_data[100];
  double IpPred;
  double rawBasal;
  double dv15[2];
  emxArray_real_T *b_times;
  emxArray_real_T *b_gValues;
  emxArray_real_T *b_gsValues;
  emxArray_real_T *b_iValues;
  int iValues_idx_0;

  // end of pidSimulationWrapper()
  // %%%%%%%%%%%%%%%%%%%%%%%%% simulatePIDSystem.m %%%%%%%%%%%%%%%%%%%%%%%%%%%%
  for (i = 0; i < 2; i++) {
    mealData_times[i] = simParams_mealTimes[i];
    mealData_carbs[i] = simParams_mealCarbs[i];
  }

  emxInit_real_T(&mealRA_times, 1);
  emxInit_real_T(&RATimes, 1);
  emxInit_real_T(&intrnlValues, 1);
  emxInit_real_T1(&x, 2);

  // end of mealModelODE()
  // %%%%%%%%%%%%%%%%%%% simMealsToObtainRateOfAppearance.m %%%%%%%%%%%%%%%%%%%
  dv13[0] = 0.0;
  dv13[1] = simParams_totalSimulationTime;
  ode45(dv13, mealData_times, mealData_carbs, RATimes, x, intrnlValues);

  // 0:1:(endTime)
  //  end of simulatePIDSystem()
  // % Equation (13) in dallaman
  // % Parameters
  // end of simMealsToObtainRateOfAppearance()
  i7 = mealRA_times->size[0];
  mealRA_times->size[0] = RATimes->size[0];
  emxEnsureCapacity((emxArray__common *)mealRA_times, i7, (int)sizeof(double));
  i = RATimes->size[0];
  for (i7 = 0; i7 < i; i7++) {
    mealRA_times->data[i7] = RATimes->data[i7];
  }

  emxInit_real_T(&mealRA_values, 1);
  i = x->size[0];
  i7 = mealRA_values->size[0];
  mealRA_values->size[0] = i;
  emxEnsureCapacity((emxArray__common *)mealRA_values, i7, (int)sizeof(double));
  for (i7 = 0; i7 < i; i7++) {
    mealRA_values->data[i7] = 0.08019 * x->data[i7 + (x->size[0] << 1)] / 102.32;
  }

  emxFree_real_T(&x);
  for (i = 0; i < 2; i++) {
    insulinBolus_times[i] = simParams_bolusTimes[i];
    insulinBolus_values[i] = simParams_bolusAmts[i];
  }

  sz = 0U;

  // % Nonsense
  curState_data[0] = 0.0;

  // Switch between open-loop and closed-loop
  emxInit_real_T(&gValues, 1);
  emxInit_real_T(&gsValues, 1);
  emxInit_real_T(&iValues, 1);
  if (timeElapsed < simParams_controllerStartTime) {
    //          fprintf('\nOpen Loop');
    // 2. Simulate until the start of the controller.
    params_Gpb = 1.9152 * simParams_startingGlucose;
    clBasal_times[0] = 0.0;
    clBasal_times[1] = simParams_controllerStartTime;
    clBasal_values[0] = simParams_openLoopBasal;
    clBasal_values[1] = 0.0;
    dv14[0] = 0.0;
    dv14[1] = 72.4342;
    dv14[2] = 141.1538;
    dv14[3] = ((0.0581 * params_Gpb - 2.2758) + 1.0) / 0.0871;
    dv14[4] = params_Gpb;
    dv14[5] = 3.2076;
    dv14[6] = 5.5043;
    dv14[7] = 100.25;
    dv14[8] = 100.25;
    dv14[9] = simParams_startingGlucose;
    simDallaManModel(dv14, t_start, T_end, mealRA_times, mealRA_values,
                     clBasal_times, clBasal_values, insulinBolus_times,
                     insulinBolus_values, intrnlValues, gValues, gsValues,
                     b_curState_data, curState_size);
    memcpy(&curState_data[0], &b_curState_data[0], 10U * sizeof(double));

    //  Initialize the outputs
    //      times        = [];
    //      gValues      = [];
    //      gsValues     = [];
    //      iValues      = [];
    // intrnlValues = zeros(1,1);
    //  copy data over
    sz = (unsigned int)intrnlValues->size[0];
    i7 = times->size[0];
    times->size[0] = intrnlValues->size[0];
    emxEnsureCapacity((emxArray__common *)times, i7, (int)sizeof(double));
    i = intrnlValues->size[0];
    for (i7 = 0; i7 < i; i7++) {
      times->data[i7] = intrnlValues->data[i7];
    }

    times->data[0] = t_start;
    i7 = iValues->size[0];
    iValues->size[0] = intrnlValues->size[0];
    emxEnsureCapacity((emxArray__common *)iValues, i7, (int)sizeof(double));
    i = intrnlValues->size[0];
    for (i7 = 0; i7 < i; i7++) {
      iValues->data[i7] = simParams_openLoopBasal;
    }

    iValues->data[0] = XX[2];
  } else {
    //          fprintf('\nClosed Loop');
    // 3. Simulate in closed loop.
    curGs = XX[1];
    curTime = timeElapsed;
    if (isPIDInitialized == 0.0) {
      ctrlState_oldG = XX[1];
      ctrlState_Kp = 0.023076923076923078;
      ctrlState_Td = 60.0;
      ctrlState_Ti = 160.0;
      ctrlState_insulinMax = 5.0 * simParams_openLoopBasal + 14.167384615384615;
      ctrlState_I = simParams_openLoopBasal;
      ctrlState_target = 100.0;
      ctrlState_dt = 5.0;
      ctrlState_gamma = 0.5;
      D[14] = XX[1];
      D[15] = 0.023076923076923078;
      D[16] = 60.0;
      D[17] = 160.0;
      D[18] = ctrlState_insulinMax;
      D[19] = simParams_openLoopBasal;
      D[20] = 100.0;
      D[21] = 5.0;
      D[22] = 3.0 * simParams_openLoopBasal;
      D[23] = 0.5;
      isPIDInitialized = 1.0;
    } else {
      ctrlState_oldG = D[14];
      ctrlState_Kp = D[15];
      ctrlState_Td = D[16];
      ctrlState_Ti = D[17];
      ctrlState_insulinMax = D[18];
      ctrlState_I = D[19];
      ctrlState_target = D[20];
      ctrlState_dt = D[21];
      ctrlState_gamma = D[23];
    }

    //     %% Nonsense
    //  Allocate a known bound (guesstimate) of memory
    //  The code after the while loop makes up for this nonsense by
    //  re-assigning only the right amount of data
    i7 = times->size[0];
    times->size[0] = 100;
    emxEnsureCapacity((emxArray__common *)times, i7, (int)sizeof(double));
    for (i7 = 0; i7 < 100; i7++) {
      times->data[i7] = 0.0;
    }

    i7 = gValues->size[0];
    gValues->size[0] = 100;
    emxEnsureCapacity((emxArray__common *)gValues, i7, (int)sizeof(double));
    for (i7 = 0; i7 < 100; i7++) {
      gValues->data[i7] = 0.0;
    }

    i7 = gsValues->size[0];
    gsValues->size[0] = 100;
    emxEnsureCapacity((emxArray__common *)gsValues, i7, (int)sizeof(double));
    for (i7 = 0; i7 < 100; i7++) {
      gsValues->data[i7] = 0.0;
    }

    i7 = iValues->size[0];
    iValues->size[0] = 100;
    emxEnsureCapacity((emxArray__common *)iValues, i7, (int)sizeof(double));
    for (i7 = 0; i7 < 100; i7++) {
      iValues->data[i7] = 0.0;
    }

    emxInit_real_T(&gsOut, 1);
    emxInit_int32_T1(&r0, 1);
    emxInit_real_T(&T, 1);
    emxInit_real_T1(&b_x, 2);
    while (curTime < T_end) {
      curGs += I;

      //  adding noise generated by SECAM
      //         %% Run the controller
      if (1U > sz) {
        i = 0;
      } else {
        i = (int)sz;
      }

      if (1 > (int)sz) {
        loop_ub = 0;
      } else {
        loop_ub = (int)sz;
      }

      times_size[0] = i;
      for (i7 = 0; i7 < i; i7++) {
        times_data[i7] = times->data[i7];
      }

      for (i7 = 0; i7 < loop_ub; i7++) {
        iValues_data[i7] = iValues->data[i7];
      }

      IpPred = computeInsulinOnBoard(insulinBolus_times, insulinBolus_values,
        times_data, times_size, iValues_data, curTime);

      //  [curTime IpPred]
      //      if ( I >= ctrlState.iMax)
      //         I = ctrlState.iMax;
      //      end
      rawBasal = ((ctrlState_Kp * (curGs - ctrlState_target) + (ctrlState_I +
        ctrlState_Kp / ctrlState_Ti * (curGs - ctrlState_target))) +
                  ctrlState_Kp * ctrlState_Td * ((curGs - ctrlState_oldG) /
        ctrlState_dt)) - ctrlState_gamma * IpPred;
      if (rawBasal <= 0.0) {
        rawBasal = 0.0;
      } else {
        if (rawBasal >= ctrlState_insulinMax) {
          rawBasal = ctrlState_insulinMax;
        }
      }

      ctrlState_oldG = curGs;
      clBasal_times[0] = curTime;
      clBasal_times[1] = curTime + 5.0;
      clBasal_values[0] = rawBasal;
      clBasal_values[1] = rawBasal;

      //  Function: simDallaManModel
      //  Simulate the DL model for a given starting state, starting time, ending 
      //  time, meal rate of appearance signal, insulin basal level and parameters 
      //  Inputs:
      //    startState: starting state for the simulation
      //    startTime: start time for simulation
      //    endTime: end time for simulation
      //    mealRA: meal rate of appearance structure
      //    insulinBasal: insulinBasal structure
      //    params: patient parameters
      //  Outputs:
      //    times : array of times
      //    gOut: array of plasma glucose simulated outputs
      //    gsOut: array of CGM sensor values (without noise)
      //    finState: the final state of the simulation
      //  Simulation total time
      //  if (~exists('mealRAIdx','var'))
      //  assert(mealRAIdx <= m,' start time past the simulate times for meal rate of arrivals'); 
      //  end
      //  Set ODE solver option to have a maximum step size of 0.5 minutes
      //  Call ODE45 solver
      dv15[0] = 0.0;
      dv15[1] = (curTime + 5.0) - curTime;
      c_ode45(dv15, *(double (*)[10])&D[3], curTime, clBasal_times,
              clBasal_values, insulinBolus_times, insulinBolus_values,
              mealRA_times, mealRA_values, (double)RATimes->size[0], T, b_x);

      // 0:1:simTime  %ERROR THROWN: The last entry in tspan must be different from the first entry. 
      //  Final state
      //  The output glucose value
      //  The output glucose sensor values
      i = b_x->size[0];
      i7 = gsOut->size[0];
      gsOut->size[0] = i;
      emxEnsureCapacity((emxArray__common *)gsOut, i7, (int)sizeof(double));
      for (i7 = 0; i7 < i; i7++) {
        gsOut->data[i7] = b_x->data[i7 + b_x->size[0] * 9];
      }

      //  Adjust the times array with starting time
      i7 = T->size[0];
      emxEnsureCapacity((emxArray__common *)T, i7, (int)sizeof(double));
      i = T->size[0];
      for (i7 = 0; i7 < i; i7++) {
        T->data[i7] += curTime;
      }

      i = b_x->size[0];
      for (i7 = 0; i7 < 10; i7++) {
        curState_data[i7] = b_x->data[(i + b_x->size[0] * i7) - 1];
      }

      i7 = T->size[0];
      i = r0->size[0];
      r0->size[0] = (int)((double)i7 - 1.0) + 1;
      emxEnsureCapacity((emxArray__common *)r0, i, (int)sizeof(int));
      i = (int)((double)i7 - 1.0);
      for (i7 = 0; i7 <= i; i7++) {
        r0->data[i7] = (int)((double)sz + (1.0 + (double)i7)) - 1;
      }

      i = T->size[0];
      for (i7 = 0; i7 < i; i7++) {
        times->data[r0->data[i7]] = T->data[i7];
      }

      i7 = T->size[0];
      i = r0->size[0];
      r0->size[0] = (int)((double)i7 - 1.0) + 1;
      emxEnsureCapacity((emxArray__common *)r0, i, (int)sizeof(int));
      i = (int)((double)i7 - 1.0);
      for (i7 = 0; i7 <= i; i7++) {
        r0->data[i7] = (int)((double)sz + (1.0 + (double)i7)) - 1;
      }

      i = b_x->size[0] - 1;
      for (i7 = 0; i7 <= i; i7++) {
        gValues->data[r0->data[i7]] = b_x->data[i7 + (b_x->size[0] << 2)] /
          1.9152;
      }

      i7 = T->size[0];
      i = r0->size[0];
      r0->size[0] = (int)((double)i7 - 1.0) + 1;
      emxEnsureCapacity((emxArray__common *)r0, i, (int)sizeof(int));
      i = (int)((double)i7 - 1.0);
      for (i7 = 0; i7 <= i; i7++) {
        r0->data[i7] = (int)((double)sz + (1.0 + (double)i7)) - 1;
      }

      i = gsOut->size[0];
      for (i7 = 0; i7 < i; i7++) {
        gsValues->data[r0->data[i7]] = gsOut->data[i7];
      }

      i7 = T->size[0];
      i = r0->size[0];
      r0->size[0] = (int)((double)i7 - 1.0) + 1;
      emxEnsureCapacity((emxArray__common *)r0, i, (int)sizeof(int));
      i = (int)((double)i7 - 1.0);
      for (i7 = 0; i7 <= i; i7++) {
        r0->data[i7] = (int)((double)sz + (1.0 + (double)i7)) - 1;
      }

      i = T->size[0];
      for (i7 = 0; i7 < i; i7++) {
        iValues->data[r0->data[i7]] = rawBasal;
      }

      i7 = b_x->size[0] - 1;
      curGs = gsOut->data[i7];
      curTime += 5.0;
      sz += T->size[0];
    }

    emxFree_real_T(&b_x);
    emxFree_real_T(&T);
    emxFree_int32_T(&r0);
    emxFree_real_T(&gsOut);
  }

  emxFree_real_T(&intrnlValues);
  emxFree_real_T(&RATimes);
  emxFree_real_T(&mealRA_values);
  emxFree_real_T(&mealRA_times);
  D[13] = isPIDInitialized;

  // % Nonsense: Prevents stuff from going nuts!
  if (1U > sz) {
    i = 0;
  } else {
    i = (int)sz;
  }

  emxInit_real_T(&b_times, 1);
  i7 = b_times->size[0];
  b_times->size[0] = i;
  emxEnsureCapacity((emxArray__common *)b_times, i7, (int)sizeof(double));
  for (i7 = 0; i7 < i; i7++) {
    b_times->data[i7] = times->data[i7];
  }

  i7 = times->size[0];
  times->size[0] = b_times->size[0];
  emxEnsureCapacity((emxArray__common *)times, i7, (int)sizeof(double));
  i = b_times->size[0];
  for (i7 = 0; i7 < i; i7++) {
    times->data[i7] = b_times->data[i7];
  }

  emxFree_real_T(&b_times);
  if (1 > (int)sz) {
    i = 0;
  } else {
    i = (int)sz;
  }

  emxInit_real_T(&b_gValues, 1);
  i7 = b_gValues->size[0];
  b_gValues->size[0] = i;
  emxEnsureCapacity((emxArray__common *)b_gValues, i7, (int)sizeof(double));
  for (i7 = 0; i7 < i; i7++) {
    b_gValues->data[i7] = gValues->data[i7];
  }

  i7 = gValues->size[0];
  gValues->size[0] = b_gValues->size[0];
  emxEnsureCapacity((emxArray__common *)gValues, i7, (int)sizeof(double));
  i = b_gValues->size[0];
  for (i7 = 0; i7 < i; i7++) {
    gValues->data[i7] = b_gValues->data[i7];
  }

  emxFree_real_T(&b_gValues);
  if (1 > (int)sz) {
    i = 0;
  } else {
    i = (int)sz;
  }

  emxInit_real_T(&b_gsValues, 1);
  i7 = b_gsValues->size[0];
  b_gsValues->size[0] = i;
  emxEnsureCapacity((emxArray__common *)b_gsValues, i7, (int)sizeof(double));
  for (i7 = 0; i7 < i; i7++) {
    b_gsValues->data[i7] = gsValues->data[i7];
  }

  i7 = gsValues->size[0];
  gsValues->size[0] = b_gsValues->size[0];
  emxEnsureCapacity((emxArray__common *)gsValues, i7, (int)sizeof(double));
  i = b_gsValues->size[0];
  for (i7 = 0; i7 < i; i7++) {
    gsValues->data[i7] = b_gsValues->data[i7];
  }

  emxFree_real_T(&b_gsValues);
  if (1 > (int)sz) {
    i = 0;
  } else {
    i = (int)sz;
  }

  emxInit_real_T(&b_iValues, 1);
  i7 = b_iValues->size[0];
  b_iValues->size[0] = i;
  emxEnsureCapacity((emxArray__common *)b_iValues, i7, (int)sizeof(double));
  for (i7 = 0; i7 < i; i7++) {
    b_iValues->data[i7] = iValues->data[i7];
  }

  i7 = iValues->size[0];
  iValues->size[0] = b_iValues->size[0];
  emxEnsureCapacity((emxArray__common *)iValues, i7, (int)sizeof(double));
  i = b_iValues->size[0];
  for (i7 = 0; i7 < i; i7++) {
    iValues->data[i7] = b_iValues->data[i7];
  }

  emxFree_real_T(&b_iValues);
  i = gValues->size[0];
  loop_ub = gsValues->size[0];
  iValues_idx_0 = iValues->size[0];
  i7 = YY_->size[0] * YY_->size[1];
  YY_->size[0] = i;
  YY_->size[1] = 3;
  emxEnsureCapacity((emxArray__common *)YY_, i7, (int)sizeof(double));
  for (i7 = 0; i7 < i; i7++) {
    YY_->data[i7] = gValues->data[i7];
  }

  emxFree_real_T(&gValues);
  for (i7 = 0; i7 < loop_ub; i7++) {
    YY_->data[i7 + YY_->size[0]] = gsValues->data[i7];
  }

  emxFree_real_T(&gsValues);
  for (i7 = 0; i7 < iValues_idx_0; i7++) {
    YY_->data[i7 + (YY_->size[0] << 1)] = iValues->data[i7];
  }

  emxFree_real_T(&iValues);
  *tt = times->data[times->size[0] - 1];

  // T_end
  i = YY_->size[0];
  for (i7 = 0; i7 < 3; i7++) {
    YY[i7] = YY_->data[(i + YY_->size[0] * i7) - 1];
  }

  // YY = [YY_(end,:) curState];
  memcpy(&D[3], &curState_data[0], 10U * sizeof(double));
}

//
// Arguments    : double t_start
//                double T_end
//                const double XX[3]
//                double D[24]
//                double P
//                double U
//                double I
//                double property_check
//                double *tt
//                double YY[3]
//                double D_[24]
//                double *P_
//                double *prop_violated_flag
// Return Type  : void
//
void artificial_pancreas(double t_start, double T_end, const double XX[3],
  double D[24], double P, double, double I, double, double *tt, double YY[3],
  double D_[24], double *P_, double *prop_violated_flag)
{
  double timeElapsed;
  double simParams_mealTimes[2];
  double simParams_mealCarbs[2];
  double simParams_bolusTimes[2];
  double simParams_bolusAmts[2];
  int ix;
  static const double mealCarbs[2] = { 249.3545, 1.2403 };

  static const double dv0[2] = { 1.92002965, 0.0037209 };

  emxArray_real_T *times;
  emxArray_real_T *YY_;
  emxArray_boolean_T *x;
  int i0;
  boolean_T y;
  boolean_T exitg1;
  boolean_T b0;

  // [t_arr,X_arr,D_arr,P_arr,prop_violated_flag] = sim_function(t0,t0+T,X0,D0,P0,U0,I0,property_check); 
  *prop_violated_flag = 0.0;

  //  t_start
  //  T_end
  //  Time Elapsed; cumulated
  timeElapsed = D[1];

  //  Update time elapsed for the next iteration
  D[1] += T_end - t_start;

  // Controller Start Time
  D[2] = 53.0687;

  //  Random Number Generator For Noise
  //  rng('shuffle','twister');
  // Load Patient Parameters from the external file
  //  patientParams = load ('d1.mat');
  // end of artificial_pancreas()
  // %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  for (ix = 0; ix < 2; ix++) {
    simParams_mealTimes[ix] = 29.4881 + 266.29040000000003 * (double)ix;
    simParams_mealCarbs[ix] = mealCarbs[ix];
    simParams_bolusTimes[ix] = 24.3555 + 286.1552 * (double)ix;
    simParams_bolusAmts[ix] = dv0[ix];
  }

  // %simParams.cgmNoisePattern = inps(12:111,1);
  // %simParams.cgmNoisePattern=zeros(100,1);
  memcpy(&D_[0], &D[0], 24U * sizeof(double));
  emxInit_real_T(&times, 1);
  emxInit_real_T1(&YY_, 2);
  emxInit_boolean_T(&x, 1);
  simulatePIDSystem(simParams_mealTimes, simParams_mealCarbs,
                    simParams_bolusTimes, simParams_bolusAmts, 0.9654, 53.0687,
                    D[0], XX[0], timeElapsed, D[13], D_, XX, t_start, T_end, I,
                    tt, times, YY, YY_);

  //  Y=[]; L= []; CLG = []; GRD=[];
  ix = YY_->size[0];
  i0 = x->size[0];
  x->size[0] = ix;
  emxEnsureCapacity((emxArray__common *)x, i0, (int)sizeof(boolean_T));
  emxFree_real_T(&times);
  for (i0 = 0; i0 < ix; i0++) {
    x->data[i0] = (YY_->data[i0] < 75.0);
  }

  emxFree_real_T(&YY_);
  y = false;
  ix = 1;
  exitg1 = false;
  while ((!exitg1) && (ix <= x->size[0])) {
    b0 = !x->data[ix - 1];
    if (!b0) {
      y = true;
      exitg1 = true;
    } else {
      ix++;
    }
  }

  emxFree_boolean_T(&x);
  if (y) {
    //      YY_
    *prop_violated_flag = 1.0;
  }

  *P_ = P;
}

//
// % Nonsense: replace Inf by a sufficiently large value
//  tMealCurrent = Inf;
// Arguments    : double t
//                const double mealData_times[2]
// Return Type  : double
//
double mealEvents(double t, const double mealData_times[2])
{
  double value;
  double tMealCurrent;
  int i;

  // end of getRateOfAppearance()
  tMealCurrent = 10000.0;
  for (i = 0; i < 2; i++) {
    if (t >= mealData_times[i]) {
      tMealCurrent = mealData_times[i];
    }
  }

  if ((t >= tMealCurrent) && (t <= tMealCurrent + 15.0)) {
    value = 0.0;
  } else {
    value = 1.0;
  }

  return value;
}

//
// File trailer for artificial_pancreas.cpp
//
// [EOF]
//
