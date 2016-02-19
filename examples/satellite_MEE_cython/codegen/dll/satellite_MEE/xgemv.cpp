//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: xgemv.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 21:26:11
//

// Include Files
#include "satellite_MEE.h"
#include "xgemv.h"

// Function Definitions

//
// Arguments    : int n
//                double alpha1
//                const double A[42]
//                const double x[21]
//                int ix0
//                double y[6]
// Return Type  : void
//
void xgemv(int n, double alpha1, const double A[42], const double x[21], int ix0,
           double y[6])
{
  int ix;
  int c;
  int iac;
  double b_c;
  int iy;
  int ia;
  if ((n == 0) || (alpha1 == 0.0)) {
  } else {
    ix = ix0;
    c = 6 * (n - 1);
    for (iac = 1; iac <= c + 1; iac += 6) {
      b_c = alpha1 * x[ix - 1];
      iy = 0;
      for (ia = iac; ia <= iac + 5; ia++) {
        y[iy] += A[ia - 1] * b_c;
        iy++;
      }

      ix++;
    }
  }
}

//
// File trailer for xgemv.cpp
//
// [EOF]
//
