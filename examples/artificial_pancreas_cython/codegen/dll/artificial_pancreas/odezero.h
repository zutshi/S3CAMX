//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: odezero.h
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//
#ifndef __ODEZERO_H__
#define __ODEZERO_H__

// Include Files
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rtwtypes.h"
#include "artificial_pancreas_types.h"

// Function Declarations
extern void odezero(double v, double t, const double y[3], double tnew, const
                    double ynew[3], double h, const double f[21], const double
                    varargin_1_times[2], int *nout, emxArray_real_T *tout,
                    emxArray_real_T *yout, emxArray_int32_T *iout, double *vnew,
                    boolean_T *stop);

#endif

//
// File trailer for odezero.h
//
// [EOF]
//
