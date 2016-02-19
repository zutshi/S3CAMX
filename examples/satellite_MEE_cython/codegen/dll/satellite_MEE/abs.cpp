//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: abs.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 21:26:11
//

// Include Files
#include "satellite_MEE.h"
#include "abs.h"

// Function Definitions

//
// Arguments    : const double x[6]
//                double y[6]
// Return Type  : void
//
void b_abs(const double x[6], double y[6])
{
  int k;
  for (k = 0; k < 6; k++) {
    y[k] = fabs(x[k]);
  }
}

//
// File trailer for abs.cpp
//
// [EOF]
//
