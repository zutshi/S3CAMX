//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: computeInsulinOnBoard.h
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//
#ifndef __COMPUTEINSULINONBOARD_H__
#define __COMPUTEINSULINONBOARD_H__

// Include Files
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rtwtypes.h"
#include "artificial_pancreas_types.h"

// Function Declarations
extern double computeInsulinOnBoard(const double bolus_times[2], const double
  bolus_values[2], const double T_data[], const int T_size[1], const double
  iValues_data[], double curTime);

#endif

//
// File trailer for computeInsulinOnBoard.h
//
// [EOF]
//
