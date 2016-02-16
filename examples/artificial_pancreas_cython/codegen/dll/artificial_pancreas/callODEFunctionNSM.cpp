//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: callODEFunctionNSM.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//

// Include Files
#include "artificial_pancreas.h"
#include "callODEFunctionNSM.h"
#include "fprintf.h"
#include "searchSorted.h"
#include <stdio.h>

// Function Definitions

//
// Arguments    : double t
//                const double y[10]
//                double varargin_1
//                const double varargin_2_times[2]
//                const double varargin_2_values[2]
//                const double varargin_3_times[2]
//                const double varargin_3_values[2]
//                const emxArray_real_T *varargin_4_times
//                const emxArray_real_T *varargin_4_values
//                double varargin_5
//                double yp[10]
// Return Type  : void
//
void b_callODEFunctionNSM(double t, const double y[10], double varargin_1, const
  double varargin_2_times[2], const double varargin_2_values[2], const double
  varargin_3_times[2], const double varargin_3_values[2], const emxArray_real_T *
  varargin_4_times, const emxArray_real_T *varargin_4_values, double varargin_5,
  double yp[10])
{
  double tAct;
  double idx;
  double IUhr;
  double jdx;
  int l;
  unsigned int u;
  int b_idx;
  int m;
  double Ra;
  double I;
  double b_y;

  //         %% Sources
  //         %% DM2007: Dalla Man et al. Meal Simulation Model of the Glucose-Insulin System IEEE Trans. on BME, 54(10), 2007 
  //         %% DM2006: Dalla Man et al. A system model for oral glucose absorption: validation on gold standard data. IEEE Trans. on BME. 53(12), 2006. 
  //         %% Inputs
  //         %% tMeal: Meal time.
  //         %% D: meal carbs amount.
  //         %% IIR: subcutaneousinsulin infusion signal.
  // %D = mCarbs;
  //         %% Use insulin Basal as a lookup table
  tAct = t + varargin_1;

  //         %% Find the last where insulin basal <= t
  //        %% idx=find(insulinBasal.times <= tAct,1,'last');
  idx = searchSorted(varargin_2_times, tAct);
  if (idx <= 0.0) {
    IUhr = 0.0;
    b_fprintf(tAct);
  } else {
    // %assert(size(idx,1) ==1);
    IUhr = varargin_2_values[(int)idx - 1];
  }

  //        %% jdx = find(insulinBolus.times <= tAct,1,'last');
  jdx = searchSorted(varargin_3_times, tAct);
  if (jdx > 0.0) {
    IUhr += varargin_3_values[(int)jdx - 1];
  }

  //         %% Convert from U/hr to pMol/min
  tAct = t + varargin_1;

  //  Function: searchSorted
  //  find max_i array(i) <= val
  //  arr is sorted ascending
  l = 1;
  u = varargin_4_times->size[0] + 1U;
  if (varargin_4_times->data[0] > tAct) {
    b_idx = -1;
  } else if (varargin_4_times->data[varargin_4_times->size[0] - 1] < tAct) {
    b_idx = varargin_4_times->size[0];
  } else if (varargin_4_times->size[0] == 1) {
    b_idx = 1;
  } else {
    while (l < (int)(u - 1U)) {
      m = (int)floor((double)(l + u) / 2.0);
      if (varargin_4_times->data[m - 1] <= tAct) {
        l = m;
      } else {
        // % arr(m) >= val
        u = (unsigned int)m;
      }
    }

    b_idx = l;
  }

  if ((b_idx < 0) || (b_idx > varargin_5)) {
    c_fprintf(tAct);
    Ra = 0.0;
  } else {
    Ra = varargin_4_values->data[b_idx - 1];
  }

  //         %% State Variables
  //         %% X: remote chamber insulin conc. X(0) = 0
  //         %% Isc1: Inslin in Subcutaneous chamber. Isc1(0) = params.Isc1ss
  //         %% Isc2: Insulin in Subcutaneous chamber2. Isc2(0) = params.Isc2ss
  //         %% Gt: glucose levels in rapidly equilibriating tissues, Gt(0) = params.Gtb 
  //         %% Gp: glucose level in the plasma. Gp(0) = params.Gpb
  //         %% Il: Insulin in Liver. Il(0) = params.Ilb
  //         %% Ip: Insulin in Plasma. Ip(0) = params.Ipb
  //         %% I1: Insulin in a remote chamber. I1(0) = params.Ib
  //         %% Id: "Delayed" insulin signal. Id(0) = params.Ib
  //         %% Gs: sensor glucose reading. Gs(0) = Gb
  // %GUT Qsto1 = x(10,1);
  // %GUT Qsto2 = x(11,1);
  //         %% GUT Qgut = x(12,1);
  //         %% Calculated Variables
  //         %% EGP  : Endogenous Glucose Production
  //         %% HE: Hepatic extraction of insulin
  //         %% m3: Liver insulin extraction rate
  //         %% Ra: Rate of appearance of glucose
  //         %% Uii: Insulin indepenendent utilization of glucose
  //         %% Uid: Insulin dependent utliziation of glucose.
  //         %% Vm, Km: Linear functions of remote insulin concentrations.
  //         %% R: rate of appearance of insulin in the plasma.
  //         %% E: renal glucose clearnance.
  //         %% G: plasma glucose concentration (mg/dl)
  //         %% I: plasma insulin concentration (pmol/L)
  //         %% Qsto: glucose in stomuch
  //         %% Ra: Rate of appearance of glucose in blood.
  //         %% parameters
  //         %%
  //         %% Equation (1) in DM2007
  //         %% Equation (3) in DM2007fileName
  I = y[6] / 0.0549;

  //         %% Equation (10) in DM2007
  //         %% Equation (8) in DM2007
  //         %% Equation (8) in DM 2007
  // %Db = Sb;
  //         %% Equation (6) in DM 2007
  //         %% Equation (2) of DM-GIM-07
  // %S = params.ka1 * Isc1 + params.ka2 * Isc2;
  // % type 1 diabetes no secretion.
  //         %% Equation (4) in DM 2007
  // %HE = -params.m5 * S + params.m6;
  //         %% Equation(5) in DM 2007
  //         %% Equation (13) in DM 2007
  // %GUT Ra = params.f * params.kabs * Qgut / params.weight;
  //         %% Utilization model
  //         %% Eq. (14) in DM 2007
  //         %% Equation (16) in DM 2007
  //         %% Equation (17) in DM 2007. Note: According to note after (17), Kmx = 0 
  //         %% Equation (15) of DM2007
  //         %% Equation (18) of DM2007
  //         %% Insulin Input Model
  //         %% Equation (1) of DM-GIM-07
  //         %% Equation(1) of DM-GIM-07
  //         %% Glucose Renal Model
  //         %% Equation (27) of DM 2007
  //         %% Glucose Model
  //         %% Equation (1) of DM 2007
  //         %% Insulin action model
  //         %% Equation (3) of DM 2007
  //         %% insulin transport model
  //         %% Equation (11) of DM 2007
  //  %% Equation to model an impuse response function for meal absorption.
  //  %% Gut absorption submodel
  //  D = mCarbs;
  //  if (t > tMeal && t < tMeal + mDuration)
  //      dImp = mCarbs/mDuration;
  //      D = mCarbs * ( t- tMeal)/mDuration;
  //  else
  //      dImp = 0;
  //
  //  end
  //  %% Meal Gut absorption submodel taken from  DM2006
  //
  //  Qsto = Qsto1 + Qsto2;
  //  alpha = 5 / ( 2 * mCarbs * (1-params.b));
  //  beta = 5/ (2 * mCarbs * params.c);
  //
  //  kempt =  params.kmin + (params.kmax - params.kmin)/2 * ( 2+  tanh( alpha * (Qsto - params.b * D) ) - tanh( beta * (Qsto - params.c * D))); 
  //  d_Qsto1 = - params.kmax * Qsto1 + dImp;
  //  d_Qsto2 = - kempt * Qsto2 + params.kmax * Qsto1;
  //  d_Qgut = - params.kabs * Qgut + kempt * Qsto2;
  yp[0] = -0.0278 * y[0] + 0.0278 * (I - 100.25);
  yp[1] = -0.0171 * y[1] + 100.0 * IUhr / 102.32;
  yp[2] = 0.0152 * y[1] - 0.0078 * y[2];
  yp[3] = (-((3.2667 + 0.0313 * y[0]) * y[3] / (253.52 + y[3])) + 0.0581 * y[4])
    - 0.0871 * y[3];
  if (y[4] > 339.0) {
    b_y = 0.0005 * (y[4] - 339.0);
  } else {
    b_y = 0.0;
  }

  yp[4] = ((((((4.7314 - 0.0047 * y[4]) - 0.0121 * y[8]) + Ra) - 1.0) - b_y) -
           0.0581 * y[4]) + 0.0871 * y[3];
  yp[5] = -0.42201584266593828 * y[5] + 0.225 * y[6];
  yp[6] = (-0.315 * y[6] + 0.1545 * y[5]) + (0.0019 * y[1] + 0.0078 * y[2]);
  yp[7] = -0.0046 * (y[7] - I);
  yp[8] = -0.0046 * (y[8] - y[7]);

  //  y(10,1) = d_Qsto1 ;
  //  y(11,1) = d_Qsto2;
  //  y(12,1) = d_Qgut;
  yp[9] = 0.1 * (y[4] / 1.9152 - y[9]);
}

//
// Arguments    : double t
//                const double y[3]
//                const double varargin_1_times[2]
//                const double varargin_1_carbs[2]
//                double yp[3]
// Return Type  : void
//
void callODEFunctionNSM(double t, const double y[3], const double
  varargin_1_times[2], const double varargin_1_carbs[2], double yp[3])
{
  double tMealCurrent;
  double mCarbsCurrent;
  int i;
  double D_;
  double dImp;
  double Qsto;
  double kempt;

  // end of getMeal()
  // end of mealEvents()
  // number of meals
  tMealCurrent = varargin_1_times[0];

  //  time of first meal
  mCarbsCurrent = varargin_1_carbs[0];

  //  carbs of the first meal
  //  meal duration
  for (i = 0; i < 2; i++) {
    //  for all the meals
    if (t >= varargin_1_times[i]) {
      tMealCurrent = varargin_1_times[i];
      mCarbsCurrent = varargin_1_carbs[i] * 1000.0;

      // % Assume that we have 15 minutes for each meal.
    }
  }

  D_ = mCarbsCurrent;
  if ((t > tMealCurrent) && (t < tMealCurrent + 15.0)) {
    dImp = mCarbsCurrent / 15.0;
    D_ = mCarbsCurrent * (t - tMealCurrent) / 15.0;
  } else {
    dImp = 0.0;
    mCarbsCurrent = 0.0;
  }

  // % Meal Gut absorption submodel taken from  DM2006
  // % Parameters
  // % 0.0038;
  // % 0.0461;
  // % 0.0891;
  Qsto = y[0] + y[1];

  // % hack to avoid division by zero is to add 0.01 to mCarbsCurrent.
  // % ..hack to avoid a division by zero
  kempt = 0.0038 + 0.021150000000000002 * ((2.0 + tanh(5.0 / (2.0 * (0.01 +
    mCarbsCurrent) * 0.29610000000000003) * (Qsto - 0.7039 * D_))) - tanh(5.0 /
    (2.0 * (0.01 + mCarbsCurrent) * 0.2106) * (Qsto - 0.2106 * D_)));

  // see paper[17] equation 18
  yp[0] = -0.0461 * y[0] + dImp;
  yp[1] = -kempt * y[1] + 0.0461 * y[0];
  yp[2] = -0.0891 * y[2] + kempt * y[1];
}

//
// File trailer for callODEFunctionNSM.cpp
//
// [EOF]
//
