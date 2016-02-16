//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: artificial_pancreas.h
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//
#ifndef __ARTIFICIAL_PANCREAS_H__
#define __ARTIFICIAL_PANCREAS_H__

// Include Files
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rtwtypes.h"
#include "artificial_pancreas_types.h"

// Function Declarations
extern void artificial_pancreas(double t_start, double T_end, const double XX[3],
  double D[24], double P, double U, double I, double property_check, double *tt,
  double YY[3], double D_[24], double *P_, double *prop_violated_flag);
extern double mealEvents(double t, const double mealData_times[2]);

#endif

//
// File trailer for artificial_pancreas.h
//
// [EOF]
//
