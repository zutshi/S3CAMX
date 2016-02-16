//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: simDallaManModel.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//

// Include Files
#include "artificial_pancreas.h"
#include "simDallaManModel.h"
#include "artificial_pancreas_emxutil.h"
#include "ode45.h"
#include <stdio.h>

// Function Definitions

//
// Function: simDallaManModel
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
// Arguments    : const double startState[10]
//                double startTime
//                double endTime
//                const emxArray_real_T *mealRA_times
//                const emxArray_real_T *mealRA_values
//                const double insulinBasal_times[2]
//                const double insulinBasal_values[2]
//                const double insulinBolus_times[2]
//                const double insulinBolus_values[2]
//                emxArray_real_T *times
//                emxArray_real_T *gOut
//                emxArray_real_T *gsOut
//                double finState_data[]
//                int finState_size[2]
// Return Type  : void
//
void simDallaManModel(const double startState[10], double startTime, double
                      endTime, const emxArray_real_T *mealRA_times, const
                      emxArray_real_T *mealRA_values, const double
                      insulinBasal_times[2], const double insulinBasal_values[2],
                      const double insulinBolus_times[2], const double
                      insulinBolus_values[2], emxArray_real_T *times,
                      emxArray_real_T *gOut, emxArray_real_T *gsOut, double
                      finState_data[], int finState_size[2])
{
  emxArray_real_T *x;
  double dv4[2];
  int b_x;
  int i2;
  emxInit_real_T1(&x, 2);

  //  Simulation total time
  //  if (~exists('mealRAIdx','var'))
  //  assert(mealRAIdx <= m,' start time past the simulate times for meal rate of arrivals'); 
  //  end
  //  Set ODE solver option to have a maximum step size of 0.5 minutes
  //  Call ODE45 solver
  dv4[0] = 0.0;
  dv4[1] = endTime - startTime;
  b_ode45(dv4, startState, startTime, insulinBasal_times, insulinBasal_values,
          insulinBolus_times, insulinBolus_values, mealRA_times, mealRA_values,
          (double)mealRA_times->size[0], times, x);

  // 0:1:simTime  %ERROR THROWN: The last entry in tspan must be different from the first entry. 
  //  Final state
  b_x = x->size[0];
  finState_size[0] = 1;
  finState_size[1] = 10;
  for (i2 = 0; i2 < 10; i2++) {
    finState_data[finState_size[0] * i2] = x->data[(b_x + x->size[0] * i2) - 1];
  }

  //  The output glucose value
  b_x = x->size[0];
  i2 = gOut->size[0];
  gOut->size[0] = b_x;
  emxEnsureCapacity((emxArray__common *)gOut, i2, (int)sizeof(double));
  for (i2 = 0; i2 < b_x; i2++) {
    gOut->data[i2] = x->data[i2 + (x->size[0] << 2)] / 1.9152;
  }

  //  The output glucose sensor values
  b_x = x->size[0];
  i2 = gsOut->size[0];
  gsOut->size[0] = b_x;
  emxEnsureCapacity((emxArray__common *)gsOut, i2, (int)sizeof(double));
  for (i2 = 0; i2 < b_x; i2++) {
    gsOut->data[i2] = x->data[i2 + x->size[0] * 9];
  }

  emxFree_real_T(&x);

  //  Adjust the times array with starting time
  i2 = times->size[0];
  emxEnsureCapacity((emxArray__common *)times, i2, (int)sizeof(double));
  b_x = times->size[0];
  for (i2 = 0; i2 < b_x; i2++) {
    times->data[i2] += startTime;
  }
}

//
// File trailer for simDallaManModel.cpp
//
// [EOF]
//
