// Must include controller.h
#include "controller.h"

#ifdef DEBUG
  #include<stdio.h>
#endif

void controller_init(){
}

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
{

  double room_temp;
  int chatter_detect;
  int previous_command_to_heater;
  int on_counter, off_counter;
  int command_to_heater;
  int chatter_limit=2;
  double MAX_TEMP=70.0, MED_TEMP=66.0;

  room_temp =                   input->x_arr[0];

  chatter_detect =              input->int_state_arr[0];
  previous_command_to_heater =  input->int_state_arr[1];
  on_counter =                  input->int_state_arr[2];
  off_counter =                 input->int_state_arr[3];

  if(room_temp >= MED_TEMP && room_temp < MAX_TEMP)
    command_to_heater = 2;
  else if(room_temp >= MAX_TEMP)
    command_to_heater = 0;
  else if(room_temp < MED_TEMP)
      command_to_heater = 1;
  else
    command_to_heater = previous_command_to_heater;
  
  if(off_counter >= 5 || on_counter >= 5)
    chatter_detect = 0;

  if(command_to_heater != previous_command_to_heater)
    chatter_detect++;

  if(chatter_detect > chatter_limit)
    command_to_heater = previous_command_to_heater;

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

  ret_val->output_arr[0] = (double)command_to_heater;
  ret_val->int_state_arr[0] = chatter_detect;
  ret_val->int_state_arr[1] = command_to_heater;
  ret_val->int_state_arr[2] = on_counter;
  ret_val->int_state_arr[3] = off_counter;

#ifdef DEBUG
  printf("room_temp = %d\t", room_temp);
  printf("on_counter = %d\t", on_counter);
  printf("off_counter = %d\t", off_counter);
  printf("chatter_detect = %d\t", chatter_detect);
  printf("command_to_heater = %d\n", command_to_heater);
  printf("========================================\n");
#endif
  return (void*)0;
}
