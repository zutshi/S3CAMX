//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: odezero.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//

// Include Files
#include "artificial_pancreas.h"
#include "odezero.h"
#include "artificial_pancreas_emxutil.h"
#include <stdio.h>

// Function Declarations
static void nfindcrossing(double vL, double vR, int *idx, int *nidx);

// Function Definitions

//
// Arguments    : double vL
//                double vR
//                int *idx
//                int *nidx
// Return Type  : void
//
static void nfindcrossing(double vL, double vR, int *idx, int *nidx)
{
  double b_vL;
  double b_vR;
  *idx = 0;
  *nidx = 0;
  if (vL < 0.0) {
    b_vL = -1.0;
  } else if (vL > 0.0) {
    b_vL = 1.0;
  } else {
    b_vL = vL;
  }

  if (vR < 0.0) {
    b_vR = -1.0;
  } else if (vR > 0.0) {
    b_vR = 1.0;
  } else {
    b_vR = vR;
  }

  if (b_vL != b_vR) {
    *nidx = 1;
    *idx = 1;
  }
}

//
// Arguments    : double v
//                double t
//                const double y[3]
//                double tnew
//                const double ynew[3]
//                double h
//                const double f[21]
//                const double varargin_1_times[2]
//                int *nout
//                emxArray_real_T *tout
//                emxArray_real_T *yout
//                emxArray_int32_T *iout
//                double *vnew
//                boolean_T *stop
// Return Type  : void
//
void odezero(double v, double t, const double y[3], double tnew, const double
             ynew[3], double h, const double f[21], const double
             varargin_1_times[2], int *nout, emxArray_real_T *tout,
             emxArray_real_T *yout, emxArray_int32_T *iout, double *vnew,
             boolean_T *stop)
{
  int i1;
  double absxk;
  double vtry;
  int exponent;
  int b_exponent;
  double b_vtry;
  double tol;
  double tdir;
  double tL;
  double vL;
  double tMealCurrent;
  int i;
  int b_vnew;
  double tR;
  double yR[3];
  double vR;
  double ttry;
  emxArray_real_T *b_yout;
  int exitg2;
  char lastmoved;
  int exitg1;
  int indzc;
  double delta;
  boolean_T lzrnz;
  boolean_T exitg3;
  double change;
  double c_vtry;
  double ytry[3];
  double fhBI1[3];
  double fhBI2[3];
  double fhBI3[3];
  double fhBI4[3];
  static const double b[7] = { -2.859375, 0.0, 4.0431266846361185, -3.90625,
    2.7939268867924527, -1.5714285714285714, 1.5 };

  static const double b_b[7] = { 3.0833333333333335, 0.0, -6.2893081761006293,
    10.416666666666666, -6.8773584905660377, 3.6666666666666665, -4.0 };

  static const double c_b[7] = { -1.1328125, 0.0, 2.6954177897574123, -5.859375,
    3.7610554245283021, -1.9642857142857142, 2.5 };

  *nout = 0;
  i1 = tout->size[0] * tout->size[1];
  tout->size[0] = 1;
  tout->size[1] = 0;
  emxEnsureCapacity((emxArray__common *)tout, i1, (int)sizeof(double));
  i1 = yout->size[0] * yout->size[1];
  yout->size[0] = 3;
  yout->size[1] = 0;
  emxEnsureCapacity((emxArray__common *)yout, i1, (int)sizeof(double));
  i1 = iout->size[0] * iout->size[1];
  iout->size[0] = 1;
  iout->size[1] = 0;
  emxEnsureCapacity((emxArray__common *)iout, i1, (int)sizeof(int));
  absxk = fabs(t);
  if (absxk <= 2.2250738585072014E-308) {
    vtry = 4.94065645841247E-324;
  } else {
    frexp(absxk, &exponent);
    vtry = ldexp(1.0, exponent - 53);
  }

  absxk = fabs(tnew);
  if (absxk <= 2.2250738585072014E-308) {
    absxk = 4.94065645841247E-324;
  } else {
    frexp(absxk, &b_exponent);
    absxk = ldexp(1.0, b_exponent - 53);
  }

  if (vtry >= absxk) {
    b_vtry = vtry;
  } else {
    b_vtry = absxk;
  }

  tol = 128.0 * b_vtry;
  vtry = fabs(tnew - t);
  if (tol <= vtry) {
  } else {
    tol = vtry;
  }

  absxk = tnew - t;
  if (absxk < 0.0) {
    tdir = -1.0;
  } else if (absxk > 0.0) {
    tdir = 1.0;
  } else {
    tdir = absxk;
  }

  *stop = false;
  tL = t;
  vL = v;

  // % Nonsense: replace Inf by a sufficiently large value
  //  tMealCurrent = Inf;
  // end of getRateOfAppearance()
  tMealCurrent = 10000.0;
  for (i = 0; i < 2; i++) {
    if (tnew >= varargin_1_times[i]) {
      tMealCurrent = varargin_1_times[i];
    }
  }

  if ((tnew >= tMealCurrent) && (tnew <= tMealCurrent + 15.0)) {
    b_vnew = 0;
  } else {
    b_vnew = 1;
  }

  *vnew = b_vnew;
  tR = tnew;
  for (i = 0; i < 3; i++) {
    yR[i] = ynew[i];
  }

  vR = b_vnew;
  vtry = 0.0;
  ttry = tnew;
  emxInit_real_T1(&b_yout, 2);
  do {
    exitg2 = 0;
    lastmoved = 'N';
    do {
      exitg1 = 0;
      nfindcrossing(vL, vR, &indzc, &exponent);
      if (exponent < 1) {
        exitg1 = 2;
      } else {
        delta = tR - tL;
        if (fabs(delta) <= tol) {
          exponent = tout->size[1];
          i1 = tout->size[0] * tout->size[1];
          tout->size[1] = exponent + 1;
          emxEnsureCapacity((emxArray__common *)tout, i1, (int)sizeof(double));
          tout->data[exponent] = 0.0;
          i1 = b_yout->size[0] * b_yout->size[1];
          b_yout->size[0] = 3;
          b_yout->size[1] = yout->size[1] + 1;
          emxEnsureCapacity((emxArray__common *)b_yout, i1, (int)sizeof(double));
          exponent = yout->size[1];
          for (i1 = 0; i1 < exponent; i1++) {
            for (b_exponent = 0; b_exponent < 3; b_exponent++) {
              b_yout->data[b_exponent + b_yout->size[0] * i1] = yout->
                data[b_exponent + yout->size[0] * i1];
            }
          }

          for (i1 = 0; i1 < 3; i1++) {
            b_yout->data[i1 + b_yout->size[0] * yout->size[1]] = 0.0;
          }

          i1 = yout->size[0] * yout->size[1];
          yout->size[0] = 3;
          yout->size[1] = b_yout->size[1];
          emxEnsureCapacity((emxArray__common *)yout, i1, (int)sizeof(double));
          exponent = b_yout->size[1];
          for (i1 = 0; i1 < exponent; i1++) {
            for (b_exponent = 0; b_exponent < 3; b_exponent++) {
              yout->data[b_exponent + yout->size[0] * i1] = b_yout->
                data[b_exponent + b_yout->size[0] * i1];
            }
          }

          exponent = iout->size[1];
          i1 = iout->size[0] * iout->size[1];
          iout->size[1] = exponent + 1;
          emxEnsureCapacity((emxArray__common *)iout, i1, (int)sizeof(int));
          iout->data[exponent] = 0;
          tout->data[*nout] = tR;
          iout->data[*nout] = indzc;
          for (i1 = 0; i1 < 3; i1++) {
            yout->data[i1 + yout->size[0] * *nout] = yR[i1];
          }

          (*nout)++;
          exitg1 = 1;
        } else {
          lzrnz = (tL == t);
          if (lzrnz) {
            lzrnz = false;
            exponent = 1;
            exitg3 = false;
            while ((!exitg3) && (exponent <= 1)) {
              if ((vL == 0.0) && (vR != 0.0)) {
                lzrnz = true;
                exitg3 = true;
              } else {
                exponent = 2;
              }
            }
          }

          if (lzrnz) {
            ttry = tL + tdir * 0.5 * tol;
          } else {
            change = 1.0;
            if (vL == 0.0) {
              if ((tdir * ttry > tdir * tR) && (vtry != vR)) {
                ttry = vR * (ttry - tR);
                absxk = (vtry - vR) * delta;
                vtry = ttry / absxk;
                absxk = 1.0 - ttry / absxk;
                if ((1.0 - vtry < 0.0) || (1.0 - vtry > 1.0)) {
                  absxk = 0.5;
                }
              } else {
                absxk = 0.5;
              }
            } else if (vR == 0.0) {
              if ((tdir * ttry < tdir * tL) && (vtry != vL)) {
                absxk = vL * (tL - ttry) / ((vtry - vL) * delta);
                if ((absxk < 0.0) || (absxk > 1.0)) {
                  absxk = 0.5;
                }
              } else {
                absxk = 0.5;
              }
            } else {
              absxk = -vL / (vR - vL);
            }

            if (absxk < 1.0) {
              change = absxk;
            }

            change *= fabs(delta);
            absxk = fabs(delta) - 0.5 * tol;
            if (change <= absxk) {
              absxk = change;
            }

            vtry = 0.5 * tol;
            if (vtry >= absxk) {
              c_vtry = vtry;
            } else {
              c_vtry = absxk;
            }

            ttry = tL + tdir * c_vtry;
          }

          absxk = (ttry - t) / h;
          for (exponent = 0; exponent < 3; exponent++) {
            fhBI1[exponent] = f[exponent] * h;
            fhBI2[exponent] = 0.0;
            fhBI3[exponent] = 0.0;
            fhBI4[exponent] = 0.0;
            for (i1 = 0; i1 < 7; i1++) {
              fhBI2[exponent] += f[exponent + 3 * i1] * (h * b[i1]);
              fhBI3[exponent] += f[exponent + 3 * i1] * (h * b_b[i1]);
              fhBI4[exponent] += f[exponent + 3 * i1] * (h * c_b[i1]);
            }

            ytry[exponent] = (((fhBI4[exponent] * absxk + fhBI3[exponent]) *
                               absxk + fhBI2[exponent]) * absxk + fhBI1[exponent])
              * absxk + y[exponent];
          }

          vtry = mealEvents(ttry, varargin_1_times);
          nfindcrossing(vL, vtry, &indzc, &exponent);
          if (exponent > 0) {
            absxk = tR;
            tR = ttry;
            ttry = absxk;
            for (i = 0; i < 3; i++) {
              yR[i] = ytry[i];
            }

            absxk = vR;
            vR = vtry;
            vtry = absxk;
            if (lastmoved == 'R') {
              absxk = 0.5 * vL;
              if (fabs(absxk) >= 2.2250738585072014E-308) {
                vL = absxk;
              }
            }

            lastmoved = 'R';
          } else {
            absxk = tL;
            tL = ttry;
            ttry = absxk;
            absxk = vL;
            vL = vtry;
            vtry = absxk;
            if (lastmoved == 'L') {
              absxk = 0.5 * vR;
              if (fabs(absxk) >= 2.2250738585072014E-308) {
                vR = absxk;
              }
            }

            lastmoved = 'L';
          }
        }
      }
    } while (exitg1 == 0);

    if (exitg1 == 1) {
      if (fabs(tnew - tR) <= tol) {
        exitg2 = 1;
      } else {
        ttry = tR;
        vtry = vR;
        tL = tR + tdir * 0.5 * tol;
        vL = mealEvents(tL, varargin_1_times);
        tR = tnew;
        for (i = 0; i < 3; i++) {
          yR[i] = ynew[i];
        }

        vR = b_vnew;
      }
    } else {
      exitg2 = 1;
    }
  } while (exitg2 == 0);

  emxFree_real_T(&b_yout);
}

//
// File trailer for odezero.cpp
//
// [EOF]
//
