// Must include controller.h
#include "controller.h"
//#include<stdio.h>

#define SAT (20)
#define CONVERSION_FACTOR (1000)
#define UPPER_SAT (SAT * CONVERSION_FACTOR)
#define LOWER_SAT (-UPPER_SAT)

void controller_init(){
}

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
{

  int pid_op = 0;
  int KP = 40;
  int KI = 1;
  int error, error_i;

  int y = input->x_arr[0];
  // get the previous error
  int error_i_prev = input->state_arr[0];
  //int ref = input->input_arr[0];
  int ref = 1000;

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
  ret_val->state_arr[0] = error_i_prev;
//  printf("integral error: %d\n", error_i_prev);
  //ret_val->state_arr[1] = ref;
  
  return (void*)0;
}
