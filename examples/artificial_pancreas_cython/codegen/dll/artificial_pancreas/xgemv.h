//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: xgemv.h
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//
#ifndef __XGEMV_H__
#define __XGEMV_H__

// Include Files
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rtwtypes.h"
#include "artificial_pancreas_types.h"

// Function Declarations
extern void b_xgemv(double alpha1, const double A[70], const double x[21], int
                    ix0, double y[10]);
extern void xgemv(int n, double alpha1, const double A[70], const double x[21],
                  int ix0, double y[10]);

#endif

//
// File trailer for xgemv.h
//
// [EOF]
//
