//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: simDallaManModel.h
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//
#ifndef __SIMDALLAMANMODEL_H__
#define __SIMDALLAMANMODEL_H__

// Include Files
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rtwtypes.h"
#include "artificial_pancreas_types.h"

// Function Declarations
extern void simDallaManModel(const double startState[10], double startTime,
  double endTime, const emxArray_real_T *mealRA_times, const emxArray_real_T
  *mealRA_values, const double insulinBasal_times[2], const double
  insulinBasal_values[2], const double insulinBolus_times[2], const double
  insulinBolus_values[2], emxArray_real_T *times, emxArray_real_T *gOut,
  emxArray_real_T *gsOut, double finState_data[], int finState_size[2]);

#endif

//
// File trailer for simDallaManModel.h
//
// [EOF]
//
