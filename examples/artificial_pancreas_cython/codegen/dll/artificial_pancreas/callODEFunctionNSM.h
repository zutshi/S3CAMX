//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: callODEFunctionNSM.h
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//
#ifndef __CALLODEFUNCTIONNSM_H__
#define __CALLODEFUNCTIONNSM_H__

// Include Files
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rtwtypes.h"
#include "artificial_pancreas_types.h"

// Function Declarations
extern void b_callODEFunctionNSM(double t, const double y[10], double varargin_1,
  const double varargin_2_times[2], const double varargin_2_values[2], const
  double varargin_3_times[2], const double varargin_3_values[2], const
  emxArray_real_T *varargin_4_times, const emxArray_real_T *varargin_4_values,
  double varargin_5, double yp[10]);
extern void callODEFunctionNSM(double t, const double y[3], const double
  varargin_1_times[2], const double varargin_1_carbs[2], double yp[3]);

#endif

//
// File trailer for callODEFunctionNSM.h
//
// [EOF]
//
