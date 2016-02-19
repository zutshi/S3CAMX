//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: satellite_MEE.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 21:26:11
//

// Include Files
#include "satellite_MEE.h"
#include "satellite_MEE_emxutil.h"
#include "ode45.h"
#include "norm.h"

// Function Definitions

//
// Arguments    : double t
//                double T
//                const double XX[6]
//                double D
//                double P
//                double U
//                double I
//                double pc
//                double dense_traces
//                emxArray_real_T *t_arr
//                emxArray_real_T *x_arr
//                double *D_
//                double *P_
//                double *prop_violated_flag
// Return Type  : void
//
void satellite_MEE(double t, double T, const double XX[6], double D, double P,
                   double, double, double, double dense_traces, emxArray_real_T *
                   t_arr, emxArray_real_T *x_arr, double *D_, double *P_, double
                   *prop_violated_flag)
{
  double radius;
  double hv[3];
  double hmag;
  double rdotv;
  double uhat[3];
  int k;
  double rzerod;
  double b_XX[3];
  double B;
  double vhat[3];
  double eccen[3];
  int i0;
  double kmee;
  double hmee;
  double fhat[3];
  double ghat[3];
  double ssqrd;
  double fmee;
  double gmee;
  double b_cosl;
  double b_sinl;
  double c_cosl;
  double lmee;
  double c_sinl;
  double c;
  double d_sinl;
  double d_cosl;
  emxArray_real_T *reci;
  emxArray_real_T *mee;
  double mee0[6];
  double b_t[2];
  emxArray_real_T *veci;
  int i;
  double r;
  double a;
  double alpha;
  double ka;
  double s_2;
  double reci1[3];
  double veci1[3];
  int j;
  int b_veci;
  double b_reci[6];
  *D_ = D;
  *P_ = P;
  *prop_violated_flag = 0.0;

  //  ADI: No globals!
  //  global mu J2 Re omega Cd
  //  mu=398603.2;% earth gravitational constant (km**3/sec**2)
  //  J2=0.00108263;
  //  Re=6378.165;% earth equatorial radius (kilometers)
  //  omega = 7.292115486e-5;% earth inertial rotation rate (radians/second)
  //  Cd=2.0e-8;% coef. of atmospheric drag
  // coordinate transformation from Cartesian state to MEE state
  //  ADI: No globals!
  //  global mu
  //  convert eci state vector to
  //  modified equinoctial elements
  //  input
  //   mu   = gravitational constant (km**3/sec**2)
  //   reci = eci position vector (kilometers)
  //   veci = eci velocity vector (kilometers/second)
  //  output
  //   mee(1) = semiparameter (kilometers)
  //   mee(2) = f equinoctial element
  //   mee(3) = g equinoctial element
  //   mee(4) = h equinoctial element
  //   mee(5) = k equinoctial element
  //   mee(6) = true longitude (radians)
  //  Orbital Mechanics with MATLAB
  // %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  radius = norm(*(double (*)[3])&XX[0]);
  hv[0] = XX[1] * XX[5] - XX[2] * XX[4];
  hv[1] = XX[2] * XX[3] - XX[0] * XX[5];
  hv[2] = XX[0] * XX[4] - XX[1] * XX[3];
  hmag = norm(hv);
  rdotv = 0.0;
  for (k = 0; k < 3; k++) {
    rdotv += XX[k] * XX[3 + k];
    uhat[k] = XX[k] / radius;
  }

  rzerod = rdotv / radius;
  b_XX[0] = XX[4] * hv[2] - XX[5] * hv[1];
  b_XX[1] = XX[5] * hv[0] - XX[3] * hv[2];
  b_XX[2] = XX[3] * hv[1] - XX[4] * hv[0];

  //  unit angular momentum vector
  B = norm(hv);
  for (i0 = 0; i0 < 3; i0++) {
    vhat[i0] = (radius * XX[3 + i0] - rzerod * XX[i0]) / hmag;
    eccen[i0] = b_XX[i0] / 398603.2 - uhat[i0];
    hv[i0] /= B;
  }

  //  compute kmee and hmee
  kmee = hv[0] / (1.0 + hv[2]);
  hmee = -hv[1] / (1.0 + hv[2]);

  //  construct unit vectors in the equinoctial frame
  //  ADI: define before subscripting
  fhat[0] = (1.0 - kmee * kmee) + hmee * hmee;
  fhat[1] = 2.0 * kmee * hmee;
  fhat[2] = -2.0 * kmee;
  ghat[0] = fhat[1];
  ghat[1] = (1.0 + kmee * kmee) - hmee * hmee;
  ghat[2] = 2.0 * hmee;
  ssqrd = (1.0 + kmee * kmee) + hmee * hmee;

  //  normalize
  //  compute fmee and gmee
  fmee = 0.0;
  gmee = 0.0;
  for (k = 0; k < 3; k++) {
    fmee += eccen[k] * (fhat[k] / ssqrd);
    gmee += eccen[k] * (ghat[k] / ssqrd);
  }

  //  compute true longitude
  b_cosl = uhat[0] + vhat[1];
  b_sinl = uhat[1] - vhat[0];

  //  four quadrant inverse tangent
  //  input
  //   a = sine of angle
  //   b = cosine of angle
  //  output
  //   y = angle (radians; 0 =< c <= 2 * pi)
  //  Orbital Mechanics with MATLAB
  // %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  if (fabs(b_sinl) < 1.0E-10) {
    if (b_cosl < 0.0) {
      c_cosl = -1.0;
    } else if (b_cosl > 0.0) {
      c_cosl = 1.0;
    } else {
      c_cosl = b_cosl;
    }

    lmee = (1.0 - c_cosl) * 1.5707963267948966;
  } else {
    if (b_sinl < 0.0) {
      c_sinl = -1.0;
    } else if (b_sinl > 0.0) {
      c_sinl = 1.0;
    } else {
      c_sinl = b_sinl;
    }

    c = (2.0 - c_sinl) * 1.5707963267948966;
    if (fabs(b_cosl) < 1.0E-10) {
      lmee = c;
    } else {
      if (b_sinl < 0.0) {
        d_sinl = -1.0;
      } else if (b_sinl > 0.0) {
        d_sinl = 1.0;
      } else {
        d_sinl = b_sinl;
      }

      if (b_cosl < 0.0) {
        d_cosl = -1.0;
      } else if (b_cosl > 0.0) {
        d_cosl = 1.0;
      } else {
        d_cosl = b_cosl;
      }

      lmee = c + d_sinl * d_cosl * (fabs(atan(b_sinl / b_cosl)) -
        1.5707963267948966);
    }
  }

  emxInit_real_T(&reci, 2);
  emxInit_real_T(&mee, 2);

  //  load modified equinoctial orbital elements array
  //  ADI: define before subscripting
  mee0[0] = hmag * hmag / 398603.2;
  mee0[1] = fmee;
  mee0[2] = gmee;
  mee0[3] = hmee;
  mee0[4] = kmee;
  mee0[5] = lmee;
  b_t[0] = t;
  b_t[1] = T;
  ode45(b_t, mee0, t_arr, mee);
  i0 = reci->size[0] * reci->size[1];
  reci->size[0] = t_arr->size[0];
  reci->size[1] = 3;
  emxEnsureCapacity((emxArray__common *)reci, i0, (int)sizeof(double));
  k = t_arr->size[0] * 3;
  for (i0 = 0; i0 < k; i0++) {
    reci->data[i0] = 0.0;
  }

  emxInit_real_T(&veci, 2);
  i0 = veci->size[0] * veci->size[1];
  veci->size[0] = t_arr->size[0];
  veci->size[1] = 3;
  emxEnsureCapacity((emxArray__common *)veci, i0, (int)sizeof(double));
  k = t_arr->size[0] * 3;
  for (i0 = 0; i0 < k; i0++) {
    veci->data[i0] = 0.0;
  }

  for (i = 0; i < t_arr->size[0]; i++) {
    // transformation from mee to Cartitien r,v
    //  ADI: No globals!
    //  global mu
    r = mee->data[i] / ((1.0 + mee->data[i + mee->size[0]] * cos(mee->data[i +
      mee->size[0] * 5])) + mee->data[i + (mee->size[0] << 1)] * sin(mee->data[i
      + mee->size[0] * 5]));
    B = mee->data[i + mee->size[0] * 3];
    a = mee->data[i + (mee->size[0] << 2)];
    alpha = B * B - a * a;
    B = mee->data[i + mee->size[0] * 3];
    a = mee->data[i + (mee->size[0] << 2)];
    ka = sqrt(B * B + a * a);
    s_2 = 1.0 + ka * ka;
    reci1[0] = r / s_2 * ((cos(mee->data[i + mee->size[0] * 5]) + alpha * cos
      (mee->data[i + mee->size[0] * 5])) + 2.0 * mee->data[i + mee->size[0] * 3]
                          * mee->data[i + (mee->size[0] << 2)] * sin(mee->data[i
      + mee->size[0] * 5]));
    reci1[1] = r / s_2 * ((sin(mee->data[i + mee->size[0] * 5]) - alpha * sin
      (mee->data[i + mee->size[0] * 5])) + 2.0 * mee->data[i + mee->size[0] * 3]
                          * mee->data[i + (mee->size[0] << 2)] * cos(mee->data[i
      + mee->size[0] * 5]));
    reci1[2] = 2.0 * r / s_2 * (mee->data[i + mee->size[0] * 3] * sin(mee->
      data[i + mee->size[0] * 5]) - mee->data[i + (mee->size[0] << 2)] * cos
      (mee->data[i + mee->size[0] * 5]));
    veci1[0] = -1.0 / s_2 * sqrt(398603.2 / mee->data[i]) * (((((sin(mee->data[i
      + mee->size[0] * 5]) + alpha * sin(mee->data[i + mee->size[0] * 5])) - 2.0
      * mee->data[i + mee->size[0] * 3] * mee->data[i + (mee->size[0] << 2)] *
      cos(mee->data[i + mee->size[0] * 5])) + mee->data[i + (mee->size[0] << 1)])
      - 2.0 * mee->data[i + mee->size[0]] * mee->data[i + mee->size[0] * 3] *
      mee->data[i + (mee->size[0] << 2)]) + alpha * mee->data[i + (mee->size[0] <<
      1)]);
    veci1[1] = -1.0 / s_2 * sqrt(398603.2 / mee->data[i]) * (((((-cos(mee->
      data[i + mee->size[0] * 5]) + alpha * cos(mee->data[i + mee->size[0] * 5]))
      + 2.0 * mee->data[i + mee->size[0] * 3] * mee->data[i + (mee->size[0] << 2)]
      * sin(mee->data[i + mee->size[0] * 5])) - mee->data[i + mee->size[0]]) +
      2.0 * mee->data[i + (mee->size[0] << 1)] * mee->data[i + mee->size[0] * 3]
      * mee->data[i + (mee->size[0] << 2)]) + alpha * mee->data[i + mee->size[0]]);
    veci1[2] = 2.0 / s_2 * sqrt(398603.2 / mee->data[i]) * (((mee->data[i +
      mee->size[0] * 3] * cos(mee->data[i + mee->size[0] * 5]) + mee->data[i +
      (mee->size[0] << 2)] * sin(mee->data[i + mee->size[0] * 5])) + mee->data[i
      + mee->size[0]] * mee->data[i + mee->size[0] * 3]) + mee->data[i +
      (mee->size[0] << 1)] * mee->data[i + (mee->size[0] << 2)]);
    for (j = 0; j < 3; j++) {
      reci->data[i + reci->size[0] * j] = reci1[j];
      veci->data[i + veci->size[0] * j] = veci1[j];
    }
  }

  emxFree_real_T(&mee);

  //  return dense traces
  if (dense_traces == 1.0) {
    i0 = x_arr->size[0] * x_arr->size[1];
    x_arr->size[0] = reci->size[0];
    x_arr->size[1] = 6;
    emxEnsureCapacity((emxArray__common *)x_arr, i0, (int)sizeof(double));
    for (i0 = 0; i0 < 3; i0++) {
      k = reci->size[0];
      for (b_veci = 0; b_veci < k; b_veci++) {
        x_arr->data[b_veci + x_arr->size[0] * i0] = reci->data[b_veci +
          reci->size[0] * i0];
      }
    }

    for (i0 = 0; i0 < 3; i0++) {
      k = veci->size[0];
      for (b_veci = 0; b_veci < k; b_veci++) {
        x_arr->data[b_veci + x_arr->size[0] * (i0 + 3)] = veci->data[b_veci +
          veci->size[0] * i0];
      }
    }
  } else {
    k = reci->size[0];
    b_veci = veci->size[0];
    for (i0 = 0; i0 < 3; i0++) {
      b_reci[i0] = reci->data[(k + reci->size[0] * i0) - 1];
    }

    for (i0 = 0; i0 < 3; i0++) {
      b_reci[i0 + 3] = veci->data[(b_veci + veci->size[0] * i0) - 1];
    }

    i0 = x_arr->size[0] * x_arr->size[1];
    x_arr->size[0] = 1;
    x_arr->size[1] = 6;
    emxEnsureCapacity((emxArray__common *)x_arr, i0, (int)sizeof(double));
    for (i0 = 0; i0 < 6; i0++) {
      x_arr->data[x_arr->size[0] * i0] = b_reci[i0];
    }

    //      x_arr=zeros(6,1);
    //      x_arr(1:3,1)=reci(end,:);
    //      x_arr(4:6,1)=veci(end,:);
    //      x_arr=x_arr';
    k = t_arr->size[0] - 1;
    B = t_arr->data[k];
    i0 = t_arr->size[0];
    t_arr->size[0] = 1;
    emxEnsureCapacity((emxArray__common *)t_arr, i0, (int)sizeof(double));
    t_arr->data[0] = B;
  }

  emxFree_real_T(&veci);
  emxFree_real_T(&reci);

  // plot3(reci(:,1),reci(:,2),reci(:,3))
  // hold on
}

//
// File trailer for satellite_MEE.cpp
//
// [EOF]
//
