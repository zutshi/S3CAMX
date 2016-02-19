//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: callODEFunctionNSM.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 21:26:11
//

// Include Files
#include "satellite_MEE.h"
#include "callODEFunctionNSM.h"
#include "norm.h"

// Function Definitions

//
// Arguments    : const double y[6]
//                double yp[6]
// Return Type  : void
//
void callODEFunctionNSM(const double y[6], double yp[6])
{
  double r;
  double alpha;
  double ka;
  double s_2;
  double reci[3];
  double veci_idx_0;
  double veci_idx_1;
  double veci_idx_2;
  double radius;
  double zhat[3];
  int k;
  double xhat[3];
  double xnorm;
  double sinphi;
  double accg_n;
  double accg_r;
  double B;
  double a[3];
  double b_B;
  double ageci[3];
  double b_xhat;
  double ey[3];
  double accg[3];
  double vrel;
  double eta;
  double dv0[18];
  double b_accg[3];
  double dv1[6];
  double dv2[6];
  int i1;

  //  ADI: No globals!
  //  global mu J2 Re
  //  compute eci state vector
  // transformation from mee to Cartitien r,v
  //  ADI: No globals!
  //  global mu
  r = y[0] / ((1.0 + y[1] * cos(y[5])) + y[2] * sin(y[5]));
  alpha = y[3] * y[3] - y[4] * y[4];
  ka = sqrt(y[3] * y[3] + y[4] * y[4]);
  s_2 = 1.0 + ka * ka;
  reci[0] = r / s_2 * ((cos(y[5]) + alpha * cos(y[5])) + 2.0 * y[3] * y[4] * sin
                       (y[5]));
  reci[1] = r / s_2 * ((sin(y[5]) - alpha * sin(y[5])) + 2.0 * y[3] * y[4] * cos
                       (y[5]));
  reci[2] = 2.0 * r / s_2 * (y[3] * sin(y[5]) - y[4] * cos(y[5]));
  veci_idx_0 = -1.0 / s_2 * sqrt(398603.2 / y[0]) * (((((sin(y[5]) + alpha * sin
    (y[5])) - 2.0 * y[3] * y[4] * cos(y[5])) + y[2]) - 2.0 * y[1] * y[3] * y[4])
    + alpha * y[2]);
  veci_idx_1 = -1.0 / s_2 * sqrt(398603.2 / y[0]) * (((((-cos(y[5]) + alpha *
    cos(y[5])) + 2.0 * y[3] * y[4] * sin(y[5])) - y[1]) + 2.0 * y[2] * y[3] * y
    [4]) + alpha * y[1]);
  veci_idx_2 = 2.0 / s_2 * sqrt(398603.2 / y[0]) * (((y[3] * cos(y[5]) + y[4] *
    sin(y[5])) + y[1] * y[3]) + y[2] * y[4]);

  // compute disturbing acceleration
  // compute acceleration caused by J2
  //  ADI: No globals!
  //  global mu J2 Re
  radius = b_norm(reci);

  //  construct unit vectors for local horizontal frame
  for (k = 0; k < 3; k++) {
    zhat[k] = -reci[k] / radius;
  }

  //  ADI: define before subscripting
  for (k = 0; k < 3; k++) {
    xhat[k] = -zhat[2] * zhat[k];
  }

  xhat[2]++;
  xnorm = norm(xhat);

  // compute gravitational acceleration in a local horizontal reference frame
  //  compute sin and cosine of latitude
  sinphi = reci[2] / radius;

  //  construct acceleration local horizontal n r direction
  accg_n = -398603.2 / pow(radius, 4.0) * sqrt(1.0 - sinphi * sinphi) *
    4.0680988767225E+7 * (3.0 * sinphi) * 0.00108263;
  accg_r = -398603.2 / pow(radius, 4.0) * 3.0 * 4.0680988767225E+7 * (0.5 * (3.0
    * (sinphi * sinphi) - 1.0)) * 0.00108263;

  //  accelerations in the eci frame
  //  ADI: define before subscripting
  //  compute radial frame unit vectors
  //  radial frame unit vectors: ex ey ez
  //   reci = eci position vector (kilometers)
  //   veci = eci velocity vector (kilometers/second)
  B = b_norm(reci);
  a[0] = reci[1] * veci_idx_2 - reci[2] * veci_idx_1;
  a[1] = reci[2] * veci_idx_0 - reci[0] * veci_idx_2;
  a[2] = reci[0] * veci_idx_1 - reci[1] * veci_idx_0;
  b_B = b_norm(a);
  for (k = 0; k < 3; k++) {
    b_xhat = xhat[k] / xnorm;
    ageci[k] = accg_n * b_xhat + accg_r * zhat[k];
    xhat[k] = b_xhat;
    zhat[k] = reci[k] / B;
    a[k] /= b_B;
  }

  ey[0] = a[1] * zhat[2] - a[2] * zhat[1];
  ey[1] = a[2] * zhat[0] - a[0] * zhat[2];
  ey[2] = a[0] * zhat[1] - a[1] * zhat[0];

  //  transform eci gravity vector to mee gravity components
  b_B = 0.0;
  for (k = 0; k < 3; k++) {
    b_B += ageci[k] * zhat[k];
  }

  accg[0] = b_B;
  b_B = 0.0;
  for (k = 0; k < 3; k++) {
    b_B += ageci[k] * ey[k];
  }

  accg[1] = b_B;
  b_B = 0.0;
  for (k = 0; k < 3; k++) {
    b_B += ageci[k] * a[k];
  }

  accg[2] = b_B;

  //  atmospheric drag
  //  ADI: No globals!
  //  global omega Cd
  //  velocity vector of atmosphere relative to spacecraft
  //  vs(1) = veci(1) + omega * reci(2);
  //  vs(2) = veci(2) - omega * reci(1);
  //  vs(3) = veci(3);
  //  ADI: vs must be defined before being subscripted
  xhat[0] = veci_idx_0 + 7.292115486E-5 * reci[1];
  xhat[1] = veci_idx_1 - 7.292115486E-5 * reci[0];
  xhat[2] = veci_idx_2;
  vrel = norm(xhat);

  //  acceleration
  eta = (1.0 + y[1] * cos(y[5])) + y[2] * sin(y[5]);
  ka = sqrt(y[3] * y[3] + y[4] * y[4]);
  b_B = ka * ka;
  B = eta / y[0];
  dv0[0] = 0.0;
  dv0[6] = 2.0 * y[0] / eta * sqrt(y[0] / 398603.2);
  dv0[12] = 0.0;
  dv0[1] = sqrt(y[0] / 398603.2) * sin(y[5]);
  dv0[7] = sqrt(y[0] / 398603.2) / eta * ((eta + 1.0) * cos(y[5]) + y[1]);
  dv0[13] = -sqrt(y[0] / 398603.2) * y[2] / eta * (y[3] * sin(y[5]) - y[4] * cos
    (y[5]));
  dv0[2] = -sqrt(y[0] / 398603.2) * cos(y[5]);
  dv0[8] = sqrt(y[0] / 398603.2) / eta * ((eta + 1.0) * sin(y[5]) + y[2]);
  dv0[14] = sqrt(y[0] / 398603.2) * y[1] / eta * (y[3] * sin(y[5]) - y[4] * cos
    (y[5]));
  dv0[3] = 0.0;
  dv0[9] = 0.0;
  dv0[15] = sqrt(y[0] / 398603.2) * (1.0 + b_B) * cos(y[5]) / 2.0 / eta;
  dv0[4] = 0.0;
  dv0[10] = 0.0;
  dv0[16] = sqrt(y[0] / 398603.2) * (1.0 + b_B) * sin(y[5]) / 2.0 / eta;
  dv0[5] = 0.0;
  dv0[11] = 0.0;
  dv0[17] = sqrt(y[0] / 398603.2) / eta * (y[3] * sin(y[5]) - y[4] * cos(y[5]));
  for (k = 0; k < 3; k++) {
    b_accg[k] = accg[k] + -2.0E-8 * xhat[k] / vrel;
  }

  dv2[0] = 0.0;
  dv2[1] = 0.0;
  dv2[2] = 0.0;
  dv2[3] = 0.0;
  dv2[4] = 0.0;
  dv2[5] = sqrt(398603.2 * y[0]) * (B * B);
  for (k = 0; k < 6; k++) {
    dv1[k] = 0.0;
    for (i1 = 0; i1 < 3; i1++) {
      dv1[k] += dv0[k + 6 * i1] * b_accg[i1];
    }

    yp[k] = dv1[k] + dv2[k];
  }
}

//
// File trailer for callODEFunctionNSM.cpp
//
// [EOF]
//
