//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: ntrp45.h
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//
#ifndef __NTRP45_H__
#define __NTRP45_H__

// Include Files
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rtwtypes.h"
#include "artificial_pancreas_types.h"

// Function Declarations
extern void b_ntrp45(const double t[3], double t0, const double b_y0[10], double
                     h, const double f[70], double y[30]);
extern void ntrp45(const double t[3], double t0, const double b_y0[3], double h,
                   const double f[21], double y[9]);

#endif

//
// File trailer for ntrp45.h
//
// [EOF]
//
