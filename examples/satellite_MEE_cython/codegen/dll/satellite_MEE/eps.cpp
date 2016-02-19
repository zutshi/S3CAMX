//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: eps.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 21:26:11
//

// Include Files
#include "satellite_MEE.h"
#include "eps.h"

// Function Definitions

//
// Arguments    : double x
// Return Type  : double
//
double eps(double x)
{
  double r;
  double absxk;
  int exponent;
  absxk = fabs(x);
  if (absxk <= 2.2250738585072014E-308) {
    r = 4.94065645841247E-324;
  } else {
    frexp(absxk, &exponent);
    r = ldexp(1.0, exponent - 53);
  }

  return r;
}

//
// File trailer for eps.cpp
//
// [EOF]
//
