//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: ode45.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 21:26:11
//

// Include Files
#include "satellite_MEE.h"
#include "ode45.h"
#include "callODEFunctionNSM.h"
#include "xgemv.h"
#include "satellite_MEE_emxutil.h"
#include "norm.h"
#include "abs.h"
#include "eps.h"

// Function Definitions

//
// Arguments    : const double tspan[2]
//                const double b_y0[6]
//                emxArray_real_T *varargout_1
//                emxArray_real_T *varargout_2
// Return Type  : void
//
void ode45(const double tspan[2], const double b_y0[6], emxArray_real_T
           *varargout_1, emxArray_real_T *varargout_2)
{
  emxArray_real_T *tout;
  double tfinal;
  double f0[6];
  int Bcolidx;
  emxArray_real_T *yout;
  emxArray_int32_T *r0;
  int nout;
  double y;
  double htspan;
  double hmax;
  double hmin;
  double absh;
  double fhBI1[6];
  double b_y[6];
  int k;
  double b_fhBI1;
  double t;
  double f[42];
  double tdir;
  boolean_T MinStepExit;
  boolean_T Done;
  emxArray_real_T *b_yout;
  int exitg1;
  int exponent;
  double h;
  boolean_T NoFailedAttempts;
  int exitg2;
  int iy;
  static const double x[21] = { 0.2, 0.075, 0.225, 0.97777777777777775,
    -3.7333333333333334, 3.5555555555555554, 2.9525986892242035,
    -11.595793324188385, 9.8228928516994358, -0.29080932784636487,
    2.8462752525252526, -10.757575757575758, 8.9064227177434727,
    0.27840909090909088, -0.2735313036020583, 0.091145833333333329, 0.0,
    0.44923629829290207, 0.65104166666666663, -0.322376179245283,
    0.13095238095238096 };

  double tnew;
  double ynew[6];
  int ia;
  double fhBI2[6];
  double tref;
  double err;
  double c_y;
  static const double b[7] = { 0.0012326388888888888, 0.0,
    -0.0042527702905061394, 0.036979166666666667, -0.05086379716981132,
    0.0419047619047619, -0.025 };

  double d0;
  int outidx;
  double b_tref[3];
  double toutnew[4];
  double fhBI4[6];
  static const double b_b[7] = { -2.859375, 0.0, 4.0431266846361185, -3.90625,
    2.7939268867924527, -1.5714285714285714, 1.5 };

  static const double c_b[7] = { 3.0833333333333335, 0.0, -6.2893081761006293,
    10.416666666666666, -6.8773584905660377, 3.6666666666666665, -4.0 };

  static const double d_b[7] = { -1.1328125, 0.0, 2.6954177897574123, -5.859375,
    3.7610554245283021, -1.9642857142857142, 2.5 };

  double d_y[18];
  double youtnew[24];
  emxInit_real_T(&tout, 2);
  tfinal = tspan[1];
  callODEFunctionNSM(b_y0, f0);
  Bcolidx = tout->size[0] * tout->size[1];
  tout->size[0] = 1;
  tout->size[1] = 200;
  emxEnsureCapacity((emxArray__common *)tout, Bcolidx, (int)sizeof(double));
  for (Bcolidx = 0; Bcolidx < 200; Bcolidx++) {
    tout->data[Bcolidx] = 0.0;
  }

  emxInit_real_T(&yout, 2);
  Bcolidx = yout->size[0] * yout->size[1];
  yout->size[0] = 6;
  yout->size[1] = 200;
  emxEnsureCapacity((emxArray__common *)yout, Bcolidx, (int)sizeof(double));
  for (Bcolidx = 0; Bcolidx < 1200; Bcolidx++) {
    yout->data[Bcolidx] = 0.0;
  }

  emxInit_int32_T(&r0, 1);
  nout = 1;
  tout->data[0] = tspan[0];
  Bcolidx = r0->size[0];
  r0->size[0] = 6;
  emxEnsureCapacity((emxArray__common *)r0, Bcolidx, (int)sizeof(int));
  for (Bcolidx = 0; Bcolidx < 6; Bcolidx++) {
    r0->data[Bcolidx] = Bcolidx;
  }

  for (Bcolidx = 0; Bcolidx < 6; Bcolidx++) {
    yout->data[r0->data[Bcolidx]] = b_y0[Bcolidx];
  }

  emxFree_int32_T(&r0);
  y = fabs(tspan[1] - tspan[0]);
  htspan = fabs(0.1 * (tspan[1] - tspan[0]));
  if (y <= htspan) {
    hmax = y;
  } else {
    hmax = htspan;
  }

  hmin = 16.0 * eps(tspan[0]);
  htspan = fabs(tspan[1] - tspan[0]);
  if (hmax <= htspan) {
    absh = hmax;
  } else {
    absh = htspan;
  }

  b_abs(b_y0, fhBI1);
  for (k = 0; k < 6; k++) {
    if (fhBI1[k] >= 1.0E-6) {
      b_fhBI1 = fhBI1[k];
    } else {
      b_fhBI1 = 1.0E-6;
    }

    b_y[k] = f0[k] / b_fhBI1;
  }

  htspan = c_norm(b_y) / 0.050476587558415456;
  if (absh * htspan > 1.0) {
    absh = 1.0 / htspan;
  }

  if (absh >= hmin) {
  } else {
    absh = hmin;
  }

  t = tspan[0];
  for (Bcolidx = 0; Bcolidx < 6; Bcolidx++) {
    b_y[Bcolidx] = b_y0[Bcolidx];
  }

  memset(&f[0], 0, 42U * sizeof(double));
  for (Bcolidx = 0; Bcolidx < 6; Bcolidx++) {
    f[Bcolidx] = f0[Bcolidx];
  }

  htspan = tspan[1] - tspan[0];
  if (htspan < 0.0) {
    tdir = -1.0;
  } else if (htspan > 0.0) {
    tdir = 1.0;
  } else {
    tdir = htspan;
  }

  MinStepExit = false;
  Done = false;
  emxInit_real_T(&b_yout, 2);
  do {
    exitg1 = 0;
    htspan = fabs(t);
    if (htspan <= 2.2250738585072014E-308) {
      htspan = 4.94065645841247E-324;
    } else {
      frexp(htspan, &exponent);
      htspan = ldexp(1.0, exponent - 53);
    }

    hmin = 16.0 * htspan;
    if (hmin >= absh) {
      htspan = hmin;
    } else {
      htspan = absh;
    }

    if (hmax <= htspan) {
      absh = hmax;
    } else {
      absh = htspan;
    }

    h = tdir * absh;
    if (1.1 * absh >= fabs(tfinal - t)) {
      h = tfinal - t;
      absh = fabs(h);
      Done = true;
    }

    NoFailedAttempts = true;
    do {
      exitg2 = 0;
      Bcolidx = 1;
      for (iy = 0; iy < 5; iy++) {
        Bcolidx += iy;
        for (k = 0; k < 6; k++) {
          fhBI1[k] = b_y[k];
        }

        xgemv(iy + 1, h, f, x, Bcolidx, fhBI1);
        callODEFunctionNSM(fhBI1, *(double (*)[6])&f[6 * (iy + 1)]);
      }

      tnew = t + h;
      if (Done) {
        tnew = tfinal;
      }

      for (k = 0; k < 6; k++) {
        ynew[k] = b_y[k];
      }

      if (h == 0.0) {
      } else {
        for (k = 0; k <= 31; k += 6) {
          htspan = h * x[Bcolidx + 4];
          iy = 0;
          for (ia = k; ia + 1 <= k + 6; ia++) {
            ynew[iy] += f[ia] * htspan;
            iy++;
          }

          Bcolidx++;
        }
      }

      callODEFunctionNSM(ynew, *(double (*)[6])&f[36]);
      h = tnew - t;
      y = 0.0;
      for (k = 0; k < 6; k++) {
        htspan = fabs(b_y[k]);
        tref = fabs(ynew[k]);
        if (htspan >= 1.0E-6) {
          err = htspan;
        } else {
          err = 1.0E-6;
        }

        if (tref >= 1.0E-6) {
          c_y = tref;
        } else {
          c_y = 1.0E-6;
        }

        if (htspan > tref) {
          fhBI1[k] = err;
        } else {
          fhBI1[k] = c_y;
        }

        htspan = 0.0;
        for (Bcolidx = 0; Bcolidx < 7; Bcolidx++) {
          htspan += f[k + 6 * Bcolidx] * b[Bcolidx];
        }

        fhBI2[k] = htspan / fhBI1[k];
        htspan = fabs(fhBI2[k]);
        if (htspan > y) {
          y = htspan;
        }
      }

      err = absh * y;
      if (err > 1.0E-6) {
        if (absh <= hmin) {
          MinStepExit = true;
          exitg2 = 1;
        } else {
          if (NoFailedAttempts) {
            NoFailedAttempts = false;
            htspan = 0.8 * pow(1.0E-6 / err, 0.2);
            if (0.1 >= htspan) {
              d0 = 0.1;
            } else {
              d0 = htspan;
            }

            htspan = absh * d0;
            if (hmin >= htspan) {
              absh = hmin;
            } else {
              absh = htspan;
            }
          } else {
            htspan = 0.5 * absh;
            if (hmin >= htspan) {
              absh = hmin;
            } else {
              absh = htspan;
            }
          }

          h = tdir * absh;
          Done = false;
        }
      } else {
        exitg2 = 1;
      }
    } while (exitg2 == 0);

    if (MinStepExit) {
      exitg1 = 1;
    } else {
      outidx = nout;
      htspan = tnew - t;
      for (Bcolidx = 0; Bcolidx < 3; Bcolidx++) {
        tref = t + htspan * (0.25 + 0.25 * (double)Bcolidx);
        toutnew[Bcolidx] = tref;
        b_tref[Bcolidx] = tref;
      }

      toutnew[3] = tnew;
      for (Bcolidx = 0; Bcolidx < 6; Bcolidx++) {
        fhBI1[Bcolidx] = f[Bcolidx] * h;
        fhBI2[Bcolidx] = 0.0;
        f0[Bcolidx] = 0.0;
        fhBI4[Bcolidx] = 0.0;
        for (ia = 0; ia < 7; ia++) {
          fhBI2[Bcolidx] += f[Bcolidx + 6 * ia] * (h * b_b[ia]);
          f0[Bcolidx] += f[Bcolidx + 6 * ia] * (h * c_b[ia]);
          fhBI4[Bcolidx] += f[Bcolidx + 6 * ia] * (h * d_b[ia]);
        }
      }

      for (iy = 0; iy < 3; iy++) {
        htspan = (b_tref[iy] - t) / h;
        for (k = 0; k < 6; k++) {
          d_y[k + 6 * iy] = (((fhBI4[k] * htspan + f0[k]) * htspan + fhBI2[k]) *
                             htspan + fhBI1[k]) * htspan + b_y[k];
          youtnew[k + 6 * iy] = d_y[k + 6 * iy];
        }
      }

      for (Bcolidx = 0; Bcolidx < 6; Bcolidx++) {
        youtnew[18 + Bcolidx] = ynew[Bcolidx];
      }

      nout += 4;
      if (nout > tout->size[1]) {
        k = tout->size[1];
        Bcolidx = tout->size[0] * tout->size[1];
        tout->size[1] = k + 200;
        emxEnsureCapacity((emxArray__common *)tout, Bcolidx, (int)sizeof(double));
        for (Bcolidx = 0; Bcolidx < 200; Bcolidx++) {
          tout->data[k + Bcolidx] = 0.0;
        }

        Bcolidx = b_yout->size[0] * b_yout->size[1];
        b_yout->size[0] = yout->size[0];
        b_yout->size[1] = yout->size[1] + 200;
        emxEnsureCapacity((emxArray__common *)b_yout, Bcolidx, (int)sizeof
                          (double));
        k = yout->size[1];
        for (Bcolidx = 0; Bcolidx < k; Bcolidx++) {
          iy = yout->size[0];
          for (ia = 0; ia < iy; ia++) {
            b_yout->data[ia + b_yout->size[0] * Bcolidx] = yout->data[ia +
              yout->size[0] * Bcolidx];
          }
        }

        for (Bcolidx = 0; Bcolidx < 200; Bcolidx++) {
          for (ia = 0; ia < 6; ia++) {
            b_yout->data[ia + b_yout->size[0] * (Bcolidx + yout->size[1])] = 0.0;
          }
        }

        Bcolidx = yout->size[0] * yout->size[1];
        yout->size[0] = b_yout->size[0];
        yout->size[1] = b_yout->size[1];
        emxEnsureCapacity((emxArray__common *)yout, Bcolidx, (int)sizeof(double));
        k = b_yout->size[1];
        for (Bcolidx = 0; Bcolidx < k; Bcolidx++) {
          iy = b_yout->size[0];
          for (ia = 0; ia < iy; ia++) {
            yout->data[ia + yout->size[0] * Bcolidx] = b_yout->data[ia +
              b_yout->size[0] * Bcolidx];
          }
        }
      }

      for (k = 0; k < 4; k++) {
        tout->data[k + outidx] = toutnew[k];
        for (iy = 0; iy < 6; iy++) {
          yout->data[iy + yout->size[0] * (k + outidx)] = youtnew[iy + 6 * k];
        }
      }

      if (Done) {
        exitg1 = 1;
      } else {
        if (NoFailedAttempts) {
          htspan = 1.25 * pow(err / 1.0E-6, 0.2);
          if (htspan > 0.2) {
            absh /= htspan;
          } else {
            absh *= 5.0;
          }
        }

        t = tnew;
        for (k = 0; k < 6; k++) {
          b_y[k] = ynew[k];
          f[k] = f[36 + k];
        }
      }
    }
  } while (exitg1 == 0);

  emxFree_real_T(&b_yout);
  if (1 > nout) {
    k = 0;
  } else {
    k = nout;
  }

  if (1 > nout) {
    iy = 0;
  } else {
    iy = nout;
  }

  Bcolidx = varargout_1->size[0];
  varargout_1->size[0] = k;
  emxEnsureCapacity((emxArray__common *)varargout_1, Bcolidx, (int)sizeof(double));
  for (Bcolidx = 0; Bcolidx < k; Bcolidx++) {
    varargout_1->data[Bcolidx] = tout->data[Bcolidx];
  }

  emxFree_real_T(&tout);
  Bcolidx = varargout_2->size[0] * varargout_2->size[1];
  varargout_2->size[0] = iy;
  varargout_2->size[1] = 6;
  emxEnsureCapacity((emxArray__common *)varargout_2, Bcolidx, (int)sizeof(double));
  for (Bcolidx = 0; Bcolidx < 6; Bcolidx++) {
    for (ia = 0; ia < iy; ia++) {
      varargout_2->data[ia + varargout_2->size[0] * Bcolidx] = yout->
        data[Bcolidx + yout->size[0] * ia];
    }
  }

  emxFree_real_T(&yout);
}

//
// File trailer for ode45.cpp
//
// [EOF]
//
