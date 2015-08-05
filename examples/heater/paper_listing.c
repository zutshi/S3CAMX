#include "controller.h"
#define CONVERSION_FACTOR (10)

void controller_init(){
}

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
{

  int room_temp;
  int chatter_detect;
  int previous_command_to_heater;
  int on_counter, off_counter;
  int command_to_heater;
  int burnout_time=5;
  int chatter_limit=2;
  int MAX_TEMP=700, MED_TEMP=660;

  room_temp = input->x_arr[0];
  chatter_detect = input->state_arr[0];
  previous_command_to_heater = input->state_arr[1];
  on_counter = input->state_arr[2];
  off_counter = input->state_arr[3];

  if(room_temp >= MED_TEMP && room_temp < MAX_TEMP)
  {
    command_to_heater = 2;
  }
  else if(room_temp >= MAX_TEMP)
  {
    command_to_heater = 0;
  }
  else if(room_temp < MED_TEMP)
  {
      command_to_heater = 1;
  }
  else
    command_to_heater = previous_command_to_heater;
  


  if(off_counter >= 5 || on_counter >= 5)
    chatter_detect = 0;

//  if((command_to_heater > 0 && previous_command_to_heater == 0)
//      || (command_to_heater == 0 && previous_command_to_heater > 0))
  if(command_to_heater != previous_command_to_heater)
    chatter_detect++;


  if(chatter_detect > chatter_limit)
  {
    //printf("chattering\n");
    command_to_heater = previous_command_to_heater;
  }

  // safety! Prevent heater meltdown.
  // if the heater is on for too long, stop
  if(on_counter >= burnout_time)
  {
    command_to_heater = 0;
  }

  if(command_to_heater == 0)
  {
    on_counter = 0;
    off_counter++;
  }
  else
  {
    on_counter++;
    off_counter = 0;
  }

  ret_val->output_arr[0] = command_to_heater * CONVERSION_FACTOR;
  ret_val->state_arr[0] = chatter_detect;
  ret_val->state_arr[1] = command_to_heater;
  ret_val->state_arr[2] = on_counter;
  ret_val->state_arr[3] = off_counter;
  return (void*)0;
}
