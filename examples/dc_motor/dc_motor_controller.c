// Must include controller.h
#include "controller.h"
//#include<stdio.h>

#define SAT (20.0)
#define UPPER_SAT (SAT)
#define LOWER_SAT (-SAT)

void controller_init(){
}

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
{
  double pid_op = 0.0;
  double KP = 40.0;
  double KI = 1.0;
  double error, error_i;

  double y = input->x_arr[0];
  // get the previous error
  double error_i_prev = input->float_state_arr[0];
  //double ref = input->input_arr[0];
  double ref = 1.0;

  //printf("S_VAL = %d\n", input->state_arr[0]);
  // error computation is affected by bounded sensor noise
  error = ref - (y + input->input_arr[0]);
  // to illustrate: ei += e*Ki
  error_i = error * KI + error_i_prev;
  error_i_prev = error_i;

  pid_op = error * KP + error_i * KI;

  if(pid_op > UPPER_SAT)
    pid_op = UPPER_SAT;
  else if(pid_op < LOWER_SAT)
    pid_op = LOWER_SAT;
  else
    pid_op = pid_op;

  ret_val->output_arr[0] = pid_op;
  ret_val->float_state_arr[0] = error_i_prev;
//  printf("integral error: %d\n", error_i_prev);
  //ret_val->state_arr[1] = ref;
  
  return (void*)0;
}
