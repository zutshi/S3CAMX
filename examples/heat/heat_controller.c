
#include "controller.h"
#include "heat.h"

void controller_init(){
}

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
{
  int i, j;

  int x[NUM_ROOMS];
  int h[NUM_ROOMS];
  int h_state[NUM_ROOMS] = {0};

  // initialize
  for(i=0;i < NUM_ROOMS;i++){
      x[i] = input->x_arr[i];
      h[i] = input->int_state_arr[i];
      //h_state[i] = input->int_state_arr[NUM_ROOMS + i];
  }

  //_ = input->float_state_arr[];

  int h0_, h1_, h2_;
  //_ = input->input_arr[];

  // compute

  for(i=0; i < NUM_ROOMS; i++){
      if(x[i] <= GET[i] && !h[i]){
          for(j=0; j < NUM_ROOMS; j++){
              if(x[j] - x[i] >= DIFF[i] && h[j]){
                  h[i] = 1;
                  h[j] = 0;
              }
          }
      }
  }

  for(i=0; i < NUM_ROOMS; i++){
      if(x[i] >= OFF[i])
          h_state[i] = 0;
      if(x[i] <= ON[i])
          h_state[i] = 1;
  }

  for(i=0;i < NUM_ROOMS;i++){
      ret_val->output_arr[i] = h[i] && h_state[i];
      ret_val->int_state_arr[i] = h[i];
      //ret_val->int_state_arr[NUM_ROOMS + i] = h_state[i];
  }

  //ret_val->int_state_arr[] = _;

  return (void*)0;
}
