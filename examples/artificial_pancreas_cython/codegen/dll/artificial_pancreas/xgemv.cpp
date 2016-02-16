//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: xgemv.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//

// Include Files
#include "artificial_pancreas.h"
#include "xgemv.h"
#include <stdio.h>

// Function Definitions

//
// Arguments    : double alpha1
//                const double A[70]
//                const double x[21]
//                int ix0
//                double y[10]
// Return Type  : void
//
void b_xgemv(double alpha1, const double A[70], const double x[21], int ix0,
             double y[10])
{
  int ix;
  int iac;
  double c;
  int iy;
  int ia;
  if (alpha1 == 0.0) {
  } else {
    ix = ix0;
    for (iac = 0; iac <= 51; iac += 10) {
      c = alpha1 * x[ix - 1];
      iy = 0;
      for (ia = iac; ia + 1 <= iac + 10; ia++) {
        y[iy] += A[ia] * c;
        iy++;
      }

      ix++;
    }
  }
}

//
// Arguments    : int n
//                double alpha1
//                const double A[70]
//                const double x[21]
//                int ix0
//                double y[10]
// Return Type  : void
//
void xgemv(int n, double alpha1, const double A[70], const double x[21], int ix0,
           double y[10])
{
  int ix;
  int c;
  int iac;
  double b_c;
  int iy;
  int ia;
  if (alpha1 == 0.0) {
  } else {
    ix = ix0;
    c = 10 * (n - 1);
    for (iac = 1; iac <= c + 1; iac += 10) {
      b_c = alpha1 * x[ix - 1];
      iy = 0;
      for (ia = iac; ia <= iac + 9; ia++) {
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
