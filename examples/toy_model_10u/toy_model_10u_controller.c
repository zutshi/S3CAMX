
#include "controller.h"

#define H (90)
#define L (10)

void controller_init(){
}

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
{
  double xB = input->x_arr[2];
  double xA = input->x_arr[1];

  double w1 = input->input_arr[0];
  double w2 = input->input_arr[1];
  double w3 = input->input_arr[2];
  double w4 = input->input_arr[3];
  double w5 = input->input_arr[4];
  double w6 = input->input_arr[5];
  double w7 = input->input_arr[6];
  double w8 = input->input_arr[7];

  double Y;

 if ((w1 < H) || (w2 > L) 
         || ((w3 < H) || (w4 > L)) 
         || ((w5 < H) || (w6 > L)) 
         || ((w7 < H) || (w8 > L))) {

          Y = xB;
        } else {
          Y = xA;
        }


  ret_val->output_arr[0] = Y;

  return (void*)0;
}
