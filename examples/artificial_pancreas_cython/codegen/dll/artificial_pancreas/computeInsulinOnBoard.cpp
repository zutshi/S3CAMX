//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: computeInsulinOnBoard.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//

// Include Files
#include "artificial_pancreas.h"
#include "computeInsulinOnBoard.h"
#include "ppval.h"
#include <stdio.h>

// Function Definitions

//
// Arguments    : const double bolus_times[2]
//                const double bolus_values[2]
//                const double T_data[]
//                const int T_size[1]
//                const double iValues_data[]
//                double curTime
// Return Type  : double
//
double computeInsulinOnBoard(const double bolus_times[2], const double
  bolus_values[2], const double T_data[], const int T_size[1], const double
  iValues_data[], double curTime)
{
  double iob;
  int i;
  double t0_coefs[80] = { -1.4285714285714287E-5, -3.0612244897959182E-5,
    -3.2653061224489766E-5, -4.8979591836734617E-6, -7.6190476190476349E-6,
    9.5238095238095027E-6, -2.8571428571428493E-5, 2.2857142857142794E-5,
    8.571428571428615E-6, -6.1224489795918405E-6, 1.6326530612244924E-5,
    -6.12244897959185E-6, 8.571428571428554E-6, 2.4489795918367516E-6,
    2.4234693877551E-7, -8.5978835978836E-8, 1.9841269841269839E-7,
    -3.3068783068783069E-8, 6.6137566137566138E-8, 0.0, 0.0004285714285714286,
    0.00073469387755102037, 0.00048979591836734648, -7.34693877551022E-5,
    -3.8095238095237814E-5, -0.00019047619047619029, 0.00028571428571428465,
    -0.00051428571428571322, -0.00017142857142857229, 6.12244897959184E-5,
    -0.00024489795918367373, 0.000122448979591837, -8.5714285714285536E-5,
    3.2653061224489563E-5, 5.6122448979591911E-6, 8.3333333333333354E-6,
    -1.7857142857142855E-5, 3.9682539682539681E-6, -3.9682539682539681E-6, 0.0,
    0.0, 0.0042857142857142859, 0.00979591836734694, 0.00979591836734694,
    0.0068571428571428577, 0.0038095238095238108, 0.0028571428571428554, 0.0,
    -0.0034285714285714254, -0.0042857142857142868, -0.0048979591836734709,
    -0.0048979591836734691, -0.0042857142857142842, -0.0034285714285714288,
    -0.002040816326530612, -0.00042857142857142871, -0.00035714285714285725,
    -0.00035714285714285714, -0.0002380952380952381, 0.0, 0.0,
    0.028571428571428571, 0.11428571428571428, 0.22857142857142856,
    0.31428571428571428, 0.37142857142857144, 0.4, 0.42857142857142855, 0.4,
    0.35714285714285715, 0.31428571428571428, 0.25714285714285712,
    0.21428571428571427, 0.17142857142857143, 0.14285714285714285,
    0.085714285714285715, 0.071428571428571425, 0.028571428571428571,
    0.014285714285714285, 0.0 };

  double t0_breaks[21] = { 0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0,
    90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 180.0, 240.0, 300.0, 360.0, 420.0,
    720.0 };

  int b_i;
  double tip;
  iob = 0.0;
  for (i = 0; i < 2; i++) {
    if (bolus_times[i] <= curTime) {
      iob += bolus_values[i] * 60.0 / 5.0 * ppval(t0_breaks, t0_coefs, curTime -
        bolus_times[i]);

      // % Convert bolus in U/hr by assuming it was delivered in 5 minutes
    }
  }

  if (T_size[0] > 2) {
    for (i = 0; i < 40; i++) {
      b_i = (T_size[0] - i) - 1;
      if (T_data[b_i] <= curTime) {
        tip = T_data[b_i];
      } else {
        tip = curTime;
      }

      if (tip < curTime) {
        iob += ppval(t0_breaks, t0_coefs, curTime - 0.5 * (T_data[b_i - 1] + tip))
          * iValues_data[b_i - 1];
      }
    }
  }

  return iob;
}

//
// File trailer for computeInsulinOnBoard.cpp
//
// [EOF]
//
