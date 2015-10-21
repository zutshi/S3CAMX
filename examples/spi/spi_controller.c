#include "controller.h"

void controller_init(){
}

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
{
  double ci = input->input_arr[0];
  double u;
  if(ci > 0)      u = 1.0;
  else if(ci < 0) u = -1.0;
  else u = 0.0;
  ret_val->output_arr[0] = u;

  return (void*)0;
}
