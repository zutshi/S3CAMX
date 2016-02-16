//
// Academic License - for use in teaching, academic research, and meeting
// course requirements at degree granting institutions only.  Not for
// government, commercial, or other organizational use.
// File: fprintf.cpp
//
// MATLAB Coder version            : 3.0
// C/C++ source code generated on  : 16-Feb-2016 13:40:36
//

// Include Files
#include "artificial_pancreas.h"
#include "fprintf.h"
#include "fileManager.h"
#include <stdio.h>

// Function Definitions

//
// Arguments    : double varargin_1
// Return Type  : void
//
void b_fprintf(double varargin_1)
{
  FILE * b_NULL;
  boolean_T autoflush;
  FILE * filestar;
  static const char cfmt[62] = { 'W', 'a', 'r', 'n', 'i', 'n', 'g', ':', ' ',
    'I', 'n', 's', 'u', 'l', 'i', 'n', ' ', 'b', 'a', 's', 'a', 'l', ' ', 'f',
    'o', 'r', ' ', 't', 'i', 'm', 'e', ' ', '%', 'f', ' ', 'i', 's', ' ', 'p',
    'r', 'o', 'b', 'l', 'e', 'm', 'a', 't', 'i', 'c', '.', ' ', 'U', 's', 'i',
    'n', 'g', ' ', '%', 'f', ' ', '\x0a', '\x00' };

  b_NULL = NULL;
  fileManager(&filestar, &autoflush);
  if (filestar == b_NULL) {
  } else {
    fprintf(filestar, cfmt, varargin_1, 0.0);
    fflush(filestar);
  }
}

//
// Arguments    : double varargin_1
// Return Type  : void
//
void c_fprintf(double varargin_1)
{
  FILE * b_NULL;
  boolean_T autoflush;
  FILE * filestar;
  static const char cfmt[35] = { 'W', 'a', 'r', 'n', 'i', 'n', 'g', ':', ' ',
    'o', 'u', 't', ' ', 'o', 'f', ' ', 'm', 'e', 'a', 'l', 'R', 'A', ' ', '@',
    ' ', 't', 'i', 'm', 'e', ' ', '%', 'f', ' ', '\x0a', '\x00' };

  b_NULL = NULL;
  fileManager(&filestar, &autoflush);
  if (filestar == b_NULL) {
  } else {
    fprintf(filestar, cfmt, varargin_1);
    fflush(filestar);
  }
}

//
// File trailer for fprintf.cpp
//
// [EOF]
//
