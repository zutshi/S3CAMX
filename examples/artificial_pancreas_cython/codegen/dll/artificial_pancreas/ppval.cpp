//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: ppval.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//

// Include Files
#include "artificial_pancreas.h"
#include "ppval.h"
#include <stdio.h>

// Function Definitions

//
// Arguments    : const double pp_breaks[21]
//                const double pp_coefs[80]
//                double x
// Return Type  : double
//
double ppval(const double pp_breaks[21], const double pp_coefs[80], double x)
{
  double v;
  int low_i;
  int low_ip1;
  int high_i;
  int mid_i;
  double xloc;
  low_i = 0;
  low_ip1 = 2;
  high_i = 21;
  while (high_i > low_ip1) {
    mid_i = ((low_i + high_i) + 1) >> 1;
    if (x >= pp_breaks[mid_i - 1]) {
      low_i = mid_i - 1;
      low_ip1 = mid_i + 1;
    } else {
      high_i = mid_i;
    }
  }

  xloc = x - pp_breaks[low_i];
  v = pp_coefs[low_i];
  for (low_ip1 = 0; low_ip1 < 3; low_ip1++) {
    v = xloc * v + pp_coefs[low_i + (low_ip1 + 1) * 20];
  }

  return v;
}

//
// File trailer for ppval.cpp
//
// [EOF]
//
