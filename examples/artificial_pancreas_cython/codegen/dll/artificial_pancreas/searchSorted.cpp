//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: searchSorted.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//

// Include Files
#include "artificial_pancreas.h"
#include "searchSorted.h"
#include <stdio.h>

// Function Definitions

//
// Function: searchSorted
//  find max_i array(i) <= val
//  arr is sorted ascending
// Arguments    : const double arr[2]
//                double val
// Return Type  : double
//
double searchSorted(const double arr[2], double val)
{
  double idx;
  double l;
  double u;
  double m;
  l = 1.0;
  u = 3.0;
  if (arr[0] > val) {
    idx = -1.0;
  } else if (arr[1] < val) {
    idx = 2.0;
  } else {
    while (l < u - 1.0) {
      m = floor((1.0 + u) / 2.0);
      if (arr[(int)m - 1] <= val) {
        l = m;
      } else {
        // % arr(m) >= val
        u = m;
      }
    }

    idx = l;
  }

  return idx;
}

//
// File trailer for searchSorted.cpp
//
// [EOF]
//
