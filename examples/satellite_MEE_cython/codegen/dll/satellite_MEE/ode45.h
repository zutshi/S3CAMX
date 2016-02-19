//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: ode45.h
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 21:26:11
//
#ifndef __ODE45_H__
#define __ODE45_H__

// Include Files
#include <math.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "rtwtypes.h"
#include "satellite_MEE_types.h"

// Function Declarations
extern void ode45(const double tspan[2], const double b_y0[6], emxArray_real_T
                  *varargout_1, emxArray_real_T *varargout_2);

#endif

//
// File trailer for ode45.h
//
// [EOF]
//
