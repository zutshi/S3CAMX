//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: satellite_MEE.h
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 21:26:11
//
#ifndef __SATELLITE_MEE_H__
#define __SATELLITE_MEE_H__

// Include Files
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rtwtypes.h"
#include "satellite_MEE_types.h"

// Function Declarations
extern void satellite_MEE(double t, double T, const double XX[6], double D,
  double P, double U, double I, double pc, double dense_traces, emxArray_real_T *
  t_arr, emxArray_real_T *x_arr, double *D_, double *P_, double
  *prop_violated_flag);

#endif

//
// File trailer for satellite_MEE.h
//
// [EOF]
//
