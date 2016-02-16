//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: ntrp45.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//

// Include Files
#include "artificial_pancreas.h"
#include "ntrp45.h"
#include <stdio.h>

// Function Definitions

//
// Arguments    : const double t[3]
//                double t0
//                const double b_y0[10]
//                double h
//                const double f[70]
//                double y[30]
// Return Type  : void
//
void b_ntrp45(const double t[3], double t0, const double b_y0[10], double h,
              const double f[70], double y[30])
{
  double fhBI1[10];
  int j;
  double fhBI2[10];
  double fhBI3[10];
  double fhBI4[10];
  int k;
  static const double b[7] = { -2.859375, 0.0, 4.0431266846361185, -3.90625,
    2.7939268867924527, -1.5714285714285714, 1.5 };

  static const double b_b[7] = { 3.0833333333333335, 0.0, -6.2893081761006293,
    10.416666666666666, -6.8773584905660377, 3.6666666666666665, -4.0 };

  static const double c_b[7] = { -1.1328125, 0.0, 2.6954177897574123, -5.859375,
    3.7610554245283021, -1.9642857142857142, 2.5 };

  double s;
  for (j = 0; j < 10; j++) {
    fhBI1[j] = f[j] * h;
    fhBI2[j] = 0.0;
    fhBI3[j] = 0.0;
    fhBI4[j] = 0.0;
    for (k = 0; k < 7; k++) {
      fhBI2[j] += f[j + 10 * k] * (h * b[k]);
      fhBI3[j] += f[j + 10 * k] * (h * b_b[k]);
      fhBI4[j] += f[j + 10 * k] * (h * c_b[k]);
    }
  }

  for (j = 0; j < 3; j++) {
    s = (t[j] - t0) / h;
    for (k = 0; k < 10; k++) {
      y[k + 10 * j] = (((fhBI4[k] * s + fhBI3[k]) * s + fhBI2[k]) * s + fhBI1[k])
        * s + b_y0[k];
    }
  }
}

//
// Arguments    : const double t[3]
//                double t0
//                const double b_y0[3]
//                double h
//                const double f[21]
//                double y[9]
// Return Type  : void
//
void ntrp45(const double t[3], double t0, const double b_y0[3], double h, const
            double f[21], double y[9])
{
  double fhBI1[3];
  int j;
  double fhBI2[3];
  double fhBI3[3];
  double fhBI4[3];
  int k;
  static const double b[7] = { -2.859375, 0.0, 4.0431266846361185, -3.90625,
    2.7939268867924527, -1.5714285714285714, 1.5 };

  static const double b_b[7] = { 3.0833333333333335, 0.0, -6.2893081761006293,
    10.416666666666666, -6.8773584905660377, 3.6666666666666665, -4.0 };

  static const double c_b[7] = { -1.1328125, 0.0, 2.6954177897574123, -5.859375,
    3.7610554245283021, -1.9642857142857142, 2.5 };

  double s;
  for (j = 0; j < 3; j++) {
    fhBI1[j] = f[j] * h;
    fhBI2[j] = 0.0;
    fhBI3[j] = 0.0;
    fhBI4[j] = 0.0;
    for (k = 0; k < 7; k++) {
      fhBI2[j] += f[j + 3 * k] * (h * b[k]);
      fhBI3[j] += f[j + 3 * k] * (h * b_b[k]);
      fhBI4[j] += f[j + 3 * k] * (h * c_b[k]);
    }
  }

  for (j = 0; j < 3; j++) {
    s = (t[j] - t0) / h;
    for (k = 0; k < 3; k++) {
      y[k + 3 * j] = (((fhBI4[k] * s + fhBI3[k]) * s + fhBI2[k]) * s + fhBI1[k])
        * s + b_y0[k];
    }
  }
}

//
// File trailer for ntrp45.cpp
//
// [EOF]
//
