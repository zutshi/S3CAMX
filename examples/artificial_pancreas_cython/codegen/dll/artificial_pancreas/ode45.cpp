//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: ode45.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//

// Include Files
#include "artificial_pancreas.h"
#include "ode45.h"
#include "callODEFunctionNSM.h"
#include "xgemv.h"
#include "artificial_pancreas_emxutil.h"
#include "ntrp45.h"
#include "odezero.h"
#include <stdio.h>

// Function Definitions

//
// Arguments    : const double tspan[2]
//                const double b_y0[10]
//                double varargin_1
//                const double varargin_2_times[2]
//                const double varargin_2_values[2]
//                const double varargin_3_times[2]
//                const double varargin_3_values[2]
//                const emxArray_real_T *varargin_4_times
//                const emxArray_real_T *varargin_4_values
//                double varargin_5
//                emxArray_real_T *varargout_1
//                emxArray_real_T *varargout_2
// Return Type  : void
//
void b_ode45(const double tspan[2], const double b_y0[10], double varargin_1,
             const double varargin_2_times[2], const double varargin_2_values[2],
             const double varargin_3_times[2], const double varargin_3_values[2],
             const emxArray_real_T *varargin_4_times, const emxArray_real_T
             *varargin_4_values, double varargin_5, emxArray_real_T *varargout_1,
             emxArray_real_T *varargout_2)
{
  emxArray_real_T *tout;
  double tfinal;
  double f0[10];
  int i3;
  emxArray_real_T *yout;
  int nout;
  double y;
  double hmax;
  double htspan;
  double absh;
  int Bcolidx;
  double b_htspan;
  double t;
  double b_y[10];
  double f[70];
  double tdir;
  boolean_T MinStepExit;
  boolean_T Done;
  emxArray_real_T *b_yout;
  int exitg1;
  int exponent;
  double hmin;
  boolean_T NoFailedAttempts;
  int exitg2;
  int j;
  static const double dv5[21] = { 0.2, 0.075, 0.225, 0.97777777777777775,
    -3.7333333333333334, 3.5555555555555554, 2.9525986892242035,
    -11.595793324188385, 9.8228928516994358, -0.29080932784636487,
    2.8462752525252526, -10.757575757575758, 8.9064227177434727,
    0.27840909090909088, -0.2735313036020583, 0.091145833333333329, 0.0,
    0.44923629829290207, 0.65104166666666663, -0.322376179245283,
    0.13095238095238096 };

  static const double dv6[6] = { 0.2, 0.3, 0.8, 0.88888888888888884, 1.0, 1.0 };

  double tnew;
  double maxval[10];
  double z[10];
  double tref;
  double err;
  double c_y;
  static const double b[7] = { 0.0012326388888888888, 0.0,
    -0.0042527702905061394, 0.036979166666666667, -0.05086379716981132,
    0.0419047619047619, -0.025 };

  double d1;
  int outidx;
  double b_tref[3];
  double toutnew[4];
  double dv7[30];
  double youtnew[40];
  int i4;
  emxInit_real_T1(&tout, 2);
  tfinal = tspan[1];
  b_callODEFunctionNSM(0.0, b_y0, varargin_1, varargin_2_times,
                       varargin_2_values, varargin_3_times, varargin_3_values,
                       varargin_4_times, varargin_4_values, varargin_5, f0);
  i3 = tout->size[0] * tout->size[1];
  tout->size[0] = 1;
  tout->size[1] = 200;
  emxEnsureCapacity((emxArray__common *)tout, i3, (int)sizeof(double));
  for (i3 = 0; i3 < 200; i3++) {
    tout->data[i3] = 0.0;
  }

  emxInit_real_T1(&yout, 2);
  i3 = yout->size[0] * yout->size[1];
  yout->size[0] = 10;
  yout->size[1] = 200;
  emxEnsureCapacity((emxArray__common *)yout, i3, (int)sizeof(double));
  for (i3 = 0; i3 < 2000; i3++) {
    yout->data[i3] = 0.0;
  }

  nout = 1;
  tout->data[0] = 0.0;
  for (i3 = 0; i3 < 10; i3++) {
    yout->data[i3] = b_y0[i3];
  }

  y = fabs(tspan[1]);
  if (y <= 0.5) {
    hmax = y;
  } else {
    hmax = 0.5;
  }

  htspan = fabs(tspan[1]);
  if (hmax <= htspan) {
    absh = hmax;
  } else {
    absh = htspan;
  }

  y = 0.0;
  for (Bcolidx = 0; Bcolidx < 10; Bcolidx++) {
    htspan = fabs(b_y0[Bcolidx]);
    if (htspan >= 0.001) {
      b_htspan = htspan;
    } else {
      b_htspan = 0.001;
    }

    htspan = fabs(f0[Bcolidx] / b_htspan);
    if (htspan > y) {
      y = htspan;
    }
  }

  htspan = y / 0.20095091452076641;
  if (absh * htspan > 1.0) {
    absh = 1.0 / htspan;
  }

  if (absh >= 7.90505033345994E-323) {
  } else {
    absh = 7.90505033345994E-323;
  }

  t = 0.0;
  memcpy(&b_y[0], &b_y0[0], 10U * sizeof(double));
  memset(&f[0], 0, 70U * sizeof(double));
  memcpy(&f[0], &f0[0], 10U * sizeof(double));
  if (tspan[1] < 0.0) {
    tdir = -1.0;
  } else if (tspan[1] > 0.0) {
    tdir = 1.0;
  } else {
    tdir = tspan[1];
  }

  MinStepExit = false;
  Done = false;
  emxInit_real_T1(&b_yout, 2);
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

    htspan = tdir * absh;
    if (1.1 * absh >= fabs(tfinal - t)) {
      htspan = tfinal - t;
      absh = fabs(htspan);
      Done = true;
    }

    NoFailedAttempts = true;
    do {
      exitg2 = 0;
      Bcolidx = 6;
      for (j = 0; j < 5; j++) {
        Bcolidx += j;
        memcpy(&f0[0], &b_y[0], 10U * sizeof(double));
        xgemv(j + 1, htspan, f, dv5, Bcolidx - 5, f0);
        b_callODEFunctionNSM(t + htspan * dv6[j], f0, varargin_1,
                             varargin_2_times, varargin_2_values,
                             varargin_3_times, varargin_3_values,
                             varargin_4_times, varargin_4_values, varargin_5,
                             *(double (*)[10])&f[10 * (j + 1)]);
      }

      tnew = t + htspan;
      if (Done) {
        tnew = tfinal;
      }

      memcpy(&f0[0], &b_y[0], 10U * sizeof(double));
      b_xgemv(htspan, f, dv5, Bcolidx, f0);
      b_callODEFunctionNSM(tnew, f0, varargin_1, varargin_2_times,
                           varargin_2_values, varargin_3_times,
                           varargin_3_values, varargin_4_times,
                           varargin_4_values, varargin_5, *(double (*)[10])&f[60]);
      y = 0.0;
      for (Bcolidx = 0; Bcolidx < 10; Bcolidx++) {
        htspan = fabs(b_y[Bcolidx]);
        tref = fabs(f0[Bcolidx]);
        if (htspan >= 0.001) {
          err = htspan;
        } else {
          err = 0.001;
        }

        if (tref >= 0.001) {
          c_y = tref;
        } else {
          c_y = 0.001;
        }

        if (htspan > tref) {
          maxval[Bcolidx] = err;
        } else {
          maxval[Bcolidx] = c_y;
        }

        htspan = 0.0;
        for (i3 = 0; i3 < 7; i3++) {
          htspan += f[Bcolidx + 10 * i3] * b[i3];
        }

        z[Bcolidx] = htspan / maxval[Bcolidx];
        htspan = fabs(z[Bcolidx]);
        if (htspan > y) {
          y = htspan;
        }
      }

      err = absh * y;
      if (err > 0.001) {
        if (absh <= hmin) {
          MinStepExit = true;
          exitg2 = 1;
        } else {
          if (NoFailedAttempts) {
            NoFailedAttempts = false;
            htspan = 0.8 * pow(0.001 / err, 0.2);
            if (0.1 >= htspan) {
              d1 = 0.1;
            } else {
              d1 = htspan;
            }

            htspan = absh * d1;
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

          htspan = tdir * absh;
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
      for (i3 = 0; i3 < 3; i3++) {
        tref = t + htspan * (0.25 + 0.25 * (double)i3);
        toutnew[i3] = tref;
        b_tref[i3] = tref;
      }

      toutnew[3] = tnew;
      b_ntrp45(b_tref, t, b_y, tnew - t, f, dv7);
      for (i3 = 0; i3 < 3; i3++) {
        memcpy(&youtnew[i3 * 10], &dv7[i3 * 10], 10U * sizeof(double));
      }

      memcpy(&youtnew[30], &f0[0], 10U * sizeof(double));
      nout += 4;
      if (nout > tout->size[1]) {
        Bcolidx = tout->size[1];
        i3 = tout->size[0] * tout->size[1];
        tout->size[1] = Bcolidx + 200;
        emxEnsureCapacity((emxArray__common *)tout, i3, (int)sizeof(double));
        for (i3 = 0; i3 < 200; i3++) {
          tout->data[Bcolidx + i3] = 0.0;
        }

        i3 = b_yout->size[0] * b_yout->size[1];
        b_yout->size[0] = 10;
        b_yout->size[1] = yout->size[1] + 200;
        emxEnsureCapacity((emxArray__common *)b_yout, i3, (int)sizeof(double));
        j = yout->size[1];
        for (i3 = 0; i3 < j; i3++) {
          for (i4 = 0; i4 < 10; i4++) {
            b_yout->data[i4 + b_yout->size[0] * i3] = yout->data[i4 + yout->
              size[0] * i3];
          }
        }

        for (i3 = 0; i3 < 200; i3++) {
          for (i4 = 0; i4 < 10; i4++) {
            b_yout->data[i4 + b_yout->size[0] * (i3 + yout->size[1])] = 0.0;
          }
        }

        i3 = yout->size[0] * yout->size[1];
        yout->size[0] = 10;
        yout->size[1] = b_yout->size[1];
        emxEnsureCapacity((emxArray__common *)yout, i3, (int)sizeof(double));
        j = b_yout->size[1];
        for (i3 = 0; i3 < j; i3++) {
          for (i4 = 0; i4 < 10; i4++) {
            yout->data[i4 + yout->size[0] * i3] = b_yout->data[i4 + b_yout->
              size[0] * i3];
          }
        }
      }

      for (Bcolidx = 0; Bcolidx < 4; Bcolidx++) {
        tout->data[Bcolidx + outidx] = toutnew[Bcolidx];
        for (j = 0; j < 10; j++) {
          yout->data[j + yout->size[0] * (Bcolidx + outidx)] = youtnew[j + 10 *
            Bcolidx];
        }
      }

      if (Done) {
        exitg1 = 1;
      } else {
        if (NoFailedAttempts) {
          htspan = 1.25 * pow(err / 0.001, 0.2);
          if (htspan > 0.2) {
            absh /= htspan;
          } else {
            absh *= 5.0;
          }
        }

        t = tnew;
        memcpy(&b_y[0], &f0[0], 10U * sizeof(double));
        memcpy(&f[0], &f[60], 10U * sizeof(double));
      }
    }
  } while (exitg1 == 0);

  emxFree_real_T(&b_yout);
  if (1 > nout) {
    j = 0;
  } else {
    j = nout;
  }

  if (1 > nout) {
    Bcolidx = 0;
  } else {
    Bcolidx = nout;
  }

  i3 = varargout_1->size[0];
  varargout_1->size[0] = j;
  emxEnsureCapacity((emxArray__common *)varargout_1, i3, (int)sizeof(double));
  for (i3 = 0; i3 < j; i3++) {
    varargout_1->data[i3] = tout->data[i3];
  }

  emxFree_real_T(&tout);
  i3 = varargout_2->size[0] * varargout_2->size[1];
  varargout_2->size[0] = Bcolidx;
  varargout_2->size[1] = 10;
  emxEnsureCapacity((emxArray__common *)varargout_2, i3, (int)sizeof(double));
  for (i3 = 0; i3 < 10; i3++) {
    for (i4 = 0; i4 < Bcolidx; i4++) {
      varargout_2->data[i4 + varargout_2->size[0] * i3] = yout->data[i3 +
        yout->size[0] * i4];
    }
  }

  emxFree_real_T(&yout);
}

//
// Arguments    : const double tspan[2]
//                const double b_y0[10]
//                double varargin_1
//                const double varargin_2_times[2]
//                const double varargin_2_values[2]
//                const double varargin_3_times[2]
//                const double varargin_3_values[2]
//                const emxArray_real_T *varargin_4_times
//                const emxArray_real_T *varargin_4_values
//                double varargin_5
//                emxArray_real_T *varargout_1
//                emxArray_real_T *varargout_2
// Return Type  : void
//
void c_ode45(const double tspan[2], const double b_y0[10], double varargin_1,
             const double varargin_2_times[2], const double varargin_2_values[2],
             const double varargin_3_times[2], const double varargin_3_values[2],
             const emxArray_real_T *varargin_4_times, const emxArray_real_T
             *varargin_4_values, double varargin_5, emxArray_real_T *varargout_1,
             emxArray_real_T *varargout_2)
{
  emxArray_real_T *tout;
  double tfinal;
  double f0[10];
  int i5;
  emxArray_real_T *yout;
  int nout;
  double y;
  double hmax;
  double htspan;
  double absh;
  int Bcolidx;
  double b_htspan;
  double t;
  double b_y[10];
  double f[70];
  double tdir;
  boolean_T MinStepExit;
  boolean_T Done;
  emxArray_real_T *b_yout;
  int exitg1;
  int exponent;
  double hmin;
  boolean_T NoFailedAttempts;
  int exitg2;
  int j;
  static const double dv8[21] = { 0.2, 0.075, 0.225, 0.97777777777777775,
    -3.7333333333333334, 3.5555555555555554, 2.9525986892242035,
    -11.595793324188385, 9.8228928516994358, -0.29080932784636487,
    2.8462752525252526, -10.757575757575758, 8.9064227177434727,
    0.27840909090909088, -0.2735313036020583, 0.091145833333333329, 0.0,
    0.44923629829290207, 0.65104166666666663, -0.322376179245283,
    0.13095238095238096 };

  static const double dv9[6] = { 0.2, 0.3, 0.8, 0.88888888888888884, 1.0, 1.0 };

  double tnew;
  double maxval[10];
  double z[10];
  double tref;
  double err;
  double c_y;
  static const double b[7] = { 0.0012326388888888888, 0.0,
    -0.0042527702905061394, 0.036979166666666667, -0.05086379716981132,
    0.0419047619047619, -0.025 };

  double d2;
  int outidx;
  double b_tref[3];
  double toutnew[4];
  double dv10[30];
  double youtnew[40];
  int i6;
  emxInit_real_T1(&tout, 2);
  tfinal = tspan[1];
  b_callODEFunctionNSM(0.0, b_y0, varargin_1, varargin_2_times,
                       varargin_2_values, varargin_3_times, varargin_3_values,
                       varargin_4_times, varargin_4_values, varargin_5, f0);
  i5 = tout->size[0] * tout->size[1];
  tout->size[0] = 1;
  tout->size[1] = 200;
  emxEnsureCapacity((emxArray__common *)tout, i5, (int)sizeof(double));
  for (i5 = 0; i5 < 200; i5++) {
    tout->data[i5] = 0.0;
  }

  emxInit_real_T1(&yout, 2);
  i5 = yout->size[0] * yout->size[1];
  yout->size[0] = 10;
  yout->size[1] = 200;
  emxEnsureCapacity((emxArray__common *)yout, i5, (int)sizeof(double));
  for (i5 = 0; i5 < 2000; i5++) {
    yout->data[i5] = 0.0;
  }

  nout = 1;
  tout->data[0] = 0.0;
  for (i5 = 0; i5 < 10; i5++) {
    yout->data[i5] = b_y0[i5];
  }

  y = fabs(tspan[1]);
  if (y <= 0.5) {
    hmax = y;
  } else {
    hmax = 0.5;
  }

  htspan = fabs(tspan[1]);
  if (hmax <= htspan) {
    absh = hmax;
  } else {
    absh = htspan;
  }

  y = 0.0;
  for (Bcolidx = 0; Bcolidx < 10; Bcolidx++) {
    htspan = fabs(b_y0[Bcolidx]);
    if (htspan >= 0.001) {
      b_htspan = htspan;
    } else {
      b_htspan = 0.001;
    }

    htspan = fabs(f0[Bcolidx] / b_htspan);
    if (htspan > y) {
      y = htspan;
    }
  }

  htspan = y / 0.20095091452076641;
  if (absh * htspan > 1.0) {
    absh = 1.0 / htspan;
  }

  if (absh >= 7.90505033345994E-323) {
  } else {
    absh = 7.90505033345994E-323;
  }

  t = 0.0;
  memcpy(&b_y[0], &b_y0[0], 10U * sizeof(double));
  memset(&f[0], 0, 70U * sizeof(double));
  memcpy(&f[0], &f0[0], 10U * sizeof(double));
  if (tspan[1] < 0.0) {
    tdir = -1.0;
  } else if (tspan[1] > 0.0) {
    tdir = 1.0;
  } else {
    tdir = tspan[1];
  }

  MinStepExit = false;
  Done = false;
  emxInit_real_T1(&b_yout, 2);
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

    htspan = tdir * absh;
    if (1.1 * absh >= fabs(tfinal - t)) {
      htspan = tfinal - t;
      absh = fabs(htspan);
      Done = true;
    }

    NoFailedAttempts = true;
    do {
      exitg2 = 0;
      Bcolidx = 6;
      for (j = 0; j < 5; j++) {
        Bcolidx += j;
        memcpy(&f0[0], &b_y[0], 10U * sizeof(double));
        xgemv(j + 1, htspan, f, dv8, Bcolidx - 5, f0);
        b_callODEFunctionNSM(t + htspan * dv9[j], f0, varargin_1,
                             varargin_2_times, varargin_2_values,
                             varargin_3_times, varargin_3_values,
                             varargin_4_times, varargin_4_values, varargin_5,
                             *(double (*)[10])&f[10 * (j + 1)]);
      }

      tnew = t + htspan;
      if (Done) {
        tnew = tfinal;
      }

      memcpy(&f0[0], &b_y[0], 10U * sizeof(double));
      b_xgemv(htspan, f, dv8, Bcolidx, f0);
      b_callODEFunctionNSM(tnew, f0, varargin_1, varargin_2_times,
                           varargin_2_values, varargin_3_times,
                           varargin_3_values, varargin_4_times,
                           varargin_4_values, varargin_5, *(double (*)[10])&f[60]);
      y = 0.0;
      for (Bcolidx = 0; Bcolidx < 10; Bcolidx++) {
        htspan = fabs(b_y[Bcolidx]);
        tref = fabs(f0[Bcolidx]);
        if (htspan >= 0.001) {
          err = htspan;
        } else {
          err = 0.001;
        }

        if (tref >= 0.001) {
          c_y = tref;
        } else {
          c_y = 0.001;
        }

        if (htspan > tref) {
          maxval[Bcolidx] = err;
        } else {
          maxval[Bcolidx] = c_y;
        }

        htspan = 0.0;
        for (i5 = 0; i5 < 7; i5++) {
          htspan += f[Bcolidx + 10 * i5] * b[i5];
        }

        z[Bcolidx] = htspan / maxval[Bcolidx];
        htspan = fabs(z[Bcolidx]);
        if (htspan > y) {
          y = htspan;
        }
      }

      err = absh * y;
      if (err > 0.001) {
        if (absh <= hmin) {
          MinStepExit = true;
          exitg2 = 1;
        } else {
          if (NoFailedAttempts) {
            NoFailedAttempts = false;
            htspan = 0.8 * pow(0.001 / err, 0.2);
            if (0.1 >= htspan) {
              d2 = 0.1;
            } else {
              d2 = htspan;
            }

            htspan = absh * d2;
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

          htspan = tdir * absh;
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
      for (i5 = 0; i5 < 3; i5++) {
        tref = t + htspan * (0.25 + 0.25 * (double)i5);
        toutnew[i5] = tref;
        b_tref[i5] = tref;
      }

      toutnew[3] = tnew;
      b_ntrp45(b_tref, t, b_y, tnew - t, f, dv10);
      for (i5 = 0; i5 < 3; i5++) {
        memcpy(&youtnew[i5 * 10], &dv10[i5 * 10], 10U * sizeof(double));
      }

      memcpy(&youtnew[30], &f0[0], 10U * sizeof(double));
      nout += 4;
      if (nout > tout->size[1]) {
        Bcolidx = tout->size[1];
        i5 = tout->size[0] * tout->size[1];
        tout->size[1] = Bcolidx + 200;
        emxEnsureCapacity((emxArray__common *)tout, i5, (int)sizeof(double));
        for (i5 = 0; i5 < 200; i5++) {
          tout->data[Bcolidx + i5] = 0.0;
        }

        i5 = b_yout->size[0] * b_yout->size[1];
        b_yout->size[0] = 10;
        b_yout->size[1] = yout->size[1] + 200;
        emxEnsureCapacity((emxArray__common *)b_yout, i5, (int)sizeof(double));
        j = yout->size[1];
        for (i5 = 0; i5 < j; i5++) {
          for (i6 = 0; i6 < 10; i6++) {
            b_yout->data[i6 + b_yout->size[0] * i5] = yout->data[i6 + yout->
              size[0] * i5];
          }
        }

        for (i5 = 0; i5 < 200; i5++) {
          for (i6 = 0; i6 < 10; i6++) {
            b_yout->data[i6 + b_yout->size[0] * (i5 + yout->size[1])] = 0.0;
          }
        }

        i5 = yout->size[0] * yout->size[1];
        yout->size[0] = 10;
        yout->size[1] = b_yout->size[1];
        emxEnsureCapacity((emxArray__common *)yout, i5, (int)sizeof(double));
        j = b_yout->size[1];
        for (i5 = 0; i5 < j; i5++) {
          for (i6 = 0; i6 < 10; i6++) {
            yout->data[i6 + yout->size[0] * i5] = b_yout->data[i6 + b_yout->
              size[0] * i5];
          }
        }
      }

      for (Bcolidx = 0; Bcolidx < 4; Bcolidx++) {
        tout->data[Bcolidx + outidx] = toutnew[Bcolidx];
        for (j = 0; j < 10; j++) {
          yout->data[j + yout->size[0] * (Bcolidx + outidx)] = youtnew[j + 10 *
            Bcolidx];
        }
      }

      if (Done) {
        exitg1 = 1;
      } else {
        if (NoFailedAttempts) {
          htspan = 1.25 * pow(err / 0.001, 0.2);
          if (htspan > 0.2) {
            absh /= htspan;
          } else {
            absh *= 5.0;
          }
        }

        t = tnew;
        memcpy(&b_y[0], &f0[0], 10U * sizeof(double));
        memcpy(&f[0], &f[60], 10U * sizeof(double));
      }
    }
  } while (exitg1 == 0);

  emxFree_real_T(&b_yout);
  if (1 > nout) {
    j = 0;
  } else {
    j = nout;
  }

  if (1 > nout) {
    Bcolidx = 0;
  } else {
    Bcolidx = nout;
  }

  i5 = varargout_1->size[0];
  varargout_1->size[0] = j;
  emxEnsureCapacity((emxArray__common *)varargout_1, i5, (int)sizeof(double));
  for (i5 = 0; i5 < j; i5++) {
    varargout_1->data[i5] = tout->data[i5];
  }

  emxFree_real_T(&tout);
  i5 = varargout_2->size[0] * varargout_2->size[1];
  varargout_2->size[0] = Bcolidx;
  varargout_2->size[1] = 10;
  emxEnsureCapacity((emxArray__common *)varargout_2, i5, (int)sizeof(double));
  for (i5 = 0; i5 < 10; i5++) {
    for (i6 = 0; i6 < Bcolidx; i6++) {
      varargout_2->data[i6 + varargout_2->size[0] * i5] = yout->data[i5 +
        yout->size[0] * i6];
    }
  }

  emxFree_real_T(&yout);
}

//
// Arguments    : const double tspan[2]
//                const double varargin_1_times[2]
//                const double varargin_1_carbs[2]
//                emxArray_real_T *varargout_1
//                emxArray_real_T *varargout_2
//                emxArray_real_T *varargout_3
// Return Type  : void
//
void ode45(const double tspan[2], const double varargin_1_times[2], const double
           varargin_1_carbs[2], emxArray_real_T *varargout_1, emxArray_real_T
           *varargout_2, emxArray_real_T *varargout_3)
{
  double tfinal;
  double f3BI3[3];
  int k;
  emxArray_real_T *teout;
  emxArray_real_T *tout;
  double f0[3];
  double valt;
  int c;
  emxArray_real_T *yout;
  int nout;
  double y;
  double hmax;
  double htspan;
  double absh;
  double t;
  double b_y[3];
  double f[21];
  double tdir;
  boolean_T MinStepExit;
  boolean_T Done;
  emxArray_real_T *te;
  emxArray_real_T *ye;
  emxArray_int32_T *ie;
  emxArray_real_T *b_yout;
  int exitg1;
  int exponent;
  double hmin;
  double h;
  boolean_T NoFailedAttempts;
  int exitg2;
  int Bcolidx;
  int j;
  int outidx;
  static const double x[21] = { 0.2, 0.075, 0.225, 0.97777777777777775,
    -3.7333333333333334, 3.5555555555555554, 2.9525986892242035,
    -11.595793324188385, 9.8228928516994358, -0.29080932784636487,
    2.8462752525252526, -10.757575757575758, 8.9064227177434727,
    0.27840909090909088, -0.2735313036020583, 0.091145833333333329, 0.0,
    0.44923629829290207, 0.65104166666666663, -0.322376179245283,
    0.13095238095238096 };

  int iy;
  int ia;
  static const double dv1[6] = { 0.2, 0.3, 0.8, 0.88888888888888884, 1.0, 1.0 };

  double tnew;
  double f4BI4[3];
  double tref;
  double err;
  double c_y;
  static const double b[7] = { 0.0012326388888888888, 0.0,
    -0.0042527702905061394, 0.036979166666666667, -0.05086379716981132,
    0.0419047619047619, -0.025 };

  double d0;
  boolean_T b1;
  double taux[6];
  static const double A[6] = { 0.2, 0.3, 0.8, 0.88888888888888884, 1.0, 1.0 };

  static const double b_b[7] = { -5.71875, 0.0, 8.0862533692722369, -7.8125,
    5.5878537735849054, -3.1428571428571428, 3.0 };

  static const double c_b[7] = { 9.25, 0.0, -18.867924528301888, 31.25,
    -20.632075471698112, 11.0, -12.0 };

  static const double d_b[7] = { -4.53125, 0.0, 10.781671159029649, -23.4375,
    15.044221698113208, -7.8571428571428568, 10.0 };

  double dv2[18];
  double toutnew[4];
  double dv3[9];
  double youtnew[12];
  tfinal = tspan[1];
  for (k = 0; k < 3; k++) {
    f3BI3[k] = 0.0;
  }

  emxInit_real_T1(&teout, 2);
  emxInit_real_T1(&tout, 2);
  callODEFunctionNSM(0.0, f3BI3, varargin_1_times, varargin_1_carbs, f0);
  valt = mealEvents(0.0, varargin_1_times);
  c = teout->size[0] * teout->size[1];
  teout->size[0] = 1;
  teout->size[1] = 0;
  emxEnsureCapacity((emxArray__common *)teout, c, (int)sizeof(double));
  c = tout->size[0] * tout->size[1];
  tout->size[0] = 1;
  tout->size[1] = 200;
  emxEnsureCapacity((emxArray__common *)tout, c, (int)sizeof(double));
  for (c = 0; c < 200; c++) {
    tout->data[c] = 0.0;
  }

  emxInit_real_T1(&yout, 2);
  c = yout->size[0] * yout->size[1];
  yout->size[0] = 3;
  yout->size[1] = 200;
  emxEnsureCapacity((emxArray__common *)yout, c, (int)sizeof(double));
  for (c = 0; c < 600; c++) {
    yout->data[c] = 0.0;
  }

  nout = 1;
  tout->data[0] = 0.0;
  for (c = 0; c < 3; c++) {
    yout->data[c] = 0.0;
  }

  y = fabs(tspan[1]);
  if (y <= 1.0) {
    hmax = y;
  } else {
    hmax = 1.0;
  }

  htspan = fabs(tspan[1]);
  if (hmax <= htspan) {
    absh = hmax;
  } else {
    absh = htspan;
  }

  y = 0.0;
  for (k = 0; k < 3; k++) {
    htspan = fabs(f0[k] / 0.001);
    if (htspan > y) {
      y = htspan;
    }
  }

  htspan = y / 0.20095091452076641;
  if (absh * htspan > 1.0) {
    absh = 1.0 / htspan;
  }

  if (absh >= 7.90505033345994E-323) {
  } else {
    absh = 7.90505033345994E-323;
  }

  t = 0.0;
  for (k = 0; k < 3; k++) {
    b_y[k] = 0.0;
  }

  memset(&f[0], 0, 21U * sizeof(double));
  for (c = 0; c < 3; c++) {
    f[c] = f0[c];
  }

  if (tspan[1] < 0.0) {
    tdir = -1.0;
  } else if (tspan[1] > 0.0) {
    tdir = 1.0;
  } else {
    tdir = tspan[1];
  }

  MinStepExit = false;
  Done = false;
  emxInit_real_T1(&te, 2);
  emxInit_real_T1(&ye, 2);
  emxInit_int32_T(&ie, 2);
  emxInit_real_T1(&b_yout, 2);
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
      Bcolidx = 6;
      for (j = 0; j < 5; j++) {
        Bcolidx += j;
        for (k = 0; k < 3; k++) {
          f0[k] = b_y[k];
        }

        if (h == 0.0) {
        } else {
          outidx = Bcolidx;
          c = 3 * j;
          for (k = 1; k <= c + 1; k += 3) {
            htspan = h * x[outidx - 6];
            iy = 0;
            for (ia = k; ia <= k + 2; ia++) {
              f0[iy] += f[ia - 1] * htspan;
              iy++;
            }

            outidx++;
          }
        }

        callODEFunctionNSM(t + h * dv1[j], f0, varargin_1_times,
                           varargin_1_carbs, *(double (*)[3])&f[3 * (j + 1)]);
      }

      tnew = t + h;
      if (Done) {
        tnew = tfinal;
      }

      for (k = 0; k < 3; k++) {
        f0[k] = b_y[k];
      }

      if (h == 0.0) {
      } else {
        for (k = 0; k <= 16; k += 3) {
          htspan = h * x[Bcolidx - 1];
          iy = 0;
          for (ia = k; ia + 1 <= k + 3; ia++) {
            f0[iy] += f[ia] * htspan;
            iy++;
          }

          Bcolidx++;
        }
      }

      callODEFunctionNSM(tnew, f0, varargin_1_times, varargin_1_carbs, *(double
        (*)[3])&f[18]);
      h = tnew - t;
      y = 0.0;
      for (k = 0; k < 3; k++) {
        htspan = fabs(b_y[k]);
        tref = fabs(f0[k]);
        if (htspan >= 0.001) {
          err = htspan;
        } else {
          err = 0.001;
        }

        if (tref >= 0.001) {
          c_y = tref;
        } else {
          c_y = 0.001;
        }

        if (htspan > tref) {
          f3BI3[k] = err;
        } else {
          f3BI3[k] = c_y;
        }

        htspan = 0.0;
        for (c = 0; c < 7; c++) {
          htspan += f[k + 3 * c] * b[c];
        }

        f4BI4[k] = htspan / f3BI3[k];
        htspan = fabs(f4BI4[k]);
        if (htspan > y) {
          y = htspan;
        }
      }

      err = absh * y;
      if (err > 0.001) {
        if (absh <= hmin) {
          MinStepExit = true;
          exitg2 = 1;
        } else {
          if (NoFailedAttempts) {
            NoFailedAttempts = false;
            htspan = 0.8 * pow(0.001 / err, 0.2);
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
      odezero(valt, t, b_y, tnew, f0, h, f, varargin_1_times, &k, te, ye, ie,
              &valt, &b1);
      if (k > 0) {
        iy = teout->size[1];
        k = te->size[1];
        c = teout->size[0] * teout->size[1];
        teout->size[1] = iy + k;
        emxEnsureCapacity((emxArray__common *)teout, c, (int)sizeof(double));
        for (c = 0; c < k; c++) {
          teout->data[iy + c] = te->data[c];
        }

        if (b1) {
          htspan = te->data[te->size[1] - 1] - t;
          for (c = 0; c < 6; c++) {
            taux[c] = t + htspan * A[c];
          }

          for (c = 0; c < 3; c++) {
            f0[c] = 0.0;
            f3BI3[c] = 0.0;
            f4BI4[c] = 0.0;
            for (ia = 0; ia < 7; ia++) {
              f0[c] += f[c + 3 * ia] * b_b[ia];
              f3BI3[c] += f[c + 3 * ia] * c_b[ia];
              f4BI4[c] += f[c + 3 * ia] * d_b[ia];
            }
          }

          for (j = 0; j < 6; j++) {
            htspan = (taux[j] - t) / h;
            for (k = 0; k < 3; k++) {
              dv2[k + 3 * j] = ((f4BI4[k] * htspan + f3BI3[k]) * htspan + f0[k])
                * htspan + f[k];
              f[k + 3 * (1 + j)] = dv2[k + 3 * j];
            }
          }

          tnew = te->data[te->size[1] - 1];
          k = ye->size[1];
          for (c = 0; c < 3; c++) {
            f0[c] = ye->data[c + ye->size[0] * (k - 1)];
          }

          h = te->data[te->size[1] - 1] - t;
          Done = true;
        }
      }

      outidx = nout;
      htspan = tnew - t;
      for (c = 0; c < 3; c++) {
        tref = t + htspan * (0.25 + 0.25 * (double)c);
        toutnew[c] = tref;
        f3BI3[c] = tref;
      }

      toutnew[3] = tnew;
      ntrp45(f3BI3, t, b_y, h, f, dv3);
      for (c = 0; c < 3; c++) {
        for (ia = 0; ia < 3; ia++) {
          youtnew[ia + 3 * c] = dv3[ia + 3 * c];
        }

        youtnew[9 + c] = f0[c];
      }

      nout += 4;
      if (nout > tout->size[1]) {
        iy = tout->size[1];
        c = tout->size[0] * tout->size[1];
        tout->size[1] = iy + 200;
        emxEnsureCapacity((emxArray__common *)tout, c, (int)sizeof(double));
        for (c = 0; c < 200; c++) {
          tout->data[iy + c] = 0.0;
        }

        c = b_yout->size[0] * b_yout->size[1];
        b_yout->size[0] = 3;
        b_yout->size[1] = yout->size[1] + 200;
        emxEnsureCapacity((emxArray__common *)b_yout, c, (int)sizeof(double));
        iy = yout->size[1];
        for (c = 0; c < iy; c++) {
          for (ia = 0; ia < 3; ia++) {
            b_yout->data[ia + b_yout->size[0] * c] = yout->data[ia + yout->size
              [0] * c];
          }
        }

        for (c = 0; c < 200; c++) {
          for (ia = 0; ia < 3; ia++) {
            b_yout->data[ia + b_yout->size[0] * (c + yout->size[1])] = 0.0;
          }
        }

        c = yout->size[0] * yout->size[1];
        yout->size[0] = 3;
        yout->size[1] = b_yout->size[1];
        emxEnsureCapacity((emxArray__common *)yout, c, (int)sizeof(double));
        iy = b_yout->size[1];
        for (c = 0; c < iy; c++) {
          for (ia = 0; ia < 3; ia++) {
            yout->data[ia + yout->size[0] * c] = b_yout->data[ia + b_yout->size
              [0] * c];
          }
        }
      }

      for (k = 0; k < 4; k++) {
        tout->data[k + outidx] = toutnew[k];
        for (j = 0; j < 3; j++) {
          yout->data[j + yout->size[0] * (k + outidx)] = youtnew[j + 3 * k];
        }
      }

      if (Done) {
        exitg1 = 1;
      } else {
        if (NoFailedAttempts) {
          htspan = 1.25 * pow(err / 0.001, 0.2);
          if (htspan > 0.2) {
            absh /= htspan;
          } else {
            absh *= 5.0;
          }
        }

        t = tnew;
        for (k = 0; k < 3; k++) {
          b_y[k] = f0[k];
          f[k] = f[18 + k];
        }
      }
    }
  } while (exitg1 == 0);

  emxFree_real_T(&b_yout);
  emxFree_int32_T(&ie);
  emxFree_real_T(&ye);
  emxFree_real_T(&te);
  if (1 > nout) {
    iy = 0;
  } else {
    iy = nout;
  }

  if (1 > nout) {
    k = 0;
  } else {
    k = nout;
  }

  c = varargout_1->size[0];
  varargout_1->size[0] = iy;
  emxEnsureCapacity((emxArray__common *)varargout_1, c, (int)sizeof(double));
  for (c = 0; c < iy; c++) {
    varargout_1->data[c] = tout->data[c];
  }

  emxFree_real_T(&tout);
  c = varargout_2->size[0] * varargout_2->size[1];
  varargout_2->size[0] = k;
  varargout_2->size[1] = 3;
  emxEnsureCapacity((emxArray__common *)varargout_2, c, (int)sizeof(double));
  for (c = 0; c < 3; c++) {
    for (ia = 0; ia < k; ia++) {
      varargout_2->data[ia + varargout_2->size[0] * c] = yout->data[c +
        yout->size[0] * ia];
    }
  }

  emxFree_real_T(&yout);
  c = varargout_3->size[0];
  varargout_3->size[0] = teout->size[1];
  emxEnsureCapacity((emxArray__common *)varargout_3, c, (int)sizeof(double));
  iy = teout->size[1];
  for (c = 0; c < iy; c++) {
    varargout_3->data[c] = teout->data[teout->size[0] * c];
  }

  emxFree_real_T(&teout);
}

//
// File trailer for ode45.cpp
//
// [EOF]
//
