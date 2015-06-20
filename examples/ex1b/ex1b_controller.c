#include "controller.h"

void controller_init(){

}

void* controller(INPUT_VAL *iv, RETURN_VAL *rv){
  int x = iv->x_arr[0];
  int u;
  //int ci = iv->input_arr[0];
  // assuming CONVERSION_FACTOR = 1000
  // if (x >= 2.8 && x <= 3.0)
//  if (x >= 2800 && x <= 3000)

  if (x >= 2800 && x <= 2805)
    //u = -1000 + x;
    u = -10000;
  else
    //u = 1000 + x;
    u = 1000;
  rv->output_arr[0] = u;
  rv->state_arr[0] = 0;

  return (void*)0;
}

