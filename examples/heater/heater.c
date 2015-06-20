// Must include controller.h
#include "controller.h"

//#define DEBUG

#ifdef DEBUG
  #include<stdio.h>
#endif

//#define KLEE_ASSUMES
/*
#ifdef KLEE_ASSUMES
  #include<klee/klee.h>
#endif
*/
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
  //int burnout_time=5;
  int chatter_limit=2;
  int MAX_TEMP=700, MED_TEMP=660;

#ifdef KLEE_ASSUMES
  /*
  klee_make_symbolic(&burnout_time, sizeof(burnout_time), "burnout_time");
  klee_make_symbolic(&chatter_limit, sizeof(chatter_limit), "chatter_limit");

  klee_make_symbolic(&MAX_TEMP, sizeof(MAX_TEMP), "MAX_TEMP");
  klee_make_symbolic(&MED_TEMP, sizeof(MED_TEMP), "MED_TEMP");
  klee_make_symbolic(&MIN_TEMP, sizeof(MIN_TEMP), "MIN_TEMP");

  klee_assume((chatter_limit >= 0) & (chatter_limit <= 100));
  klee_assume((burnout_time > chatter_limit+2) & (burnout_time <= 100));
  klee_assume((MAX_TEMP >= 700) & (MAX_TEMP <= 1000));
  klee_assume((MED_TEMP >= 600) & (MED_TEMP < 700));
  klee_assume((MIN_TEMP >= -10) & (MIN_TEMP < 600));
*/
/*
  // room temp
  klee_assume((input->x_arr[0] >= 0) & (input->x_arr[0] <= 1000));
  // chatter_detect
  klee_assume((input->state_arr[0] >= 0)&(input->state_arr[0] <= 20));
  // previous_command_to_heater
  klee_assume((input->state_arr[1] >= 0)&(input->state_arr[1] <= 2));
  // on_counter
  klee_assume((input->state_arr[2] >= 0) & (input->state_arr[2] <= 20));
  //
  klee_assume((input->state_arr[3] >= 0) & (input->state_arr[3] <= 20));
*/
#endif

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
/*
  if(on_counter >= burnout_time)
  {
    command_to_heater = 0;
  }
*/
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

#ifdef DEBUG
  printf("room_temp = %d\t", room_temp);
  printf("on_counter = %d\t", on_counter);
  printf("off_counter = %d\t", off_counter);
  printf("chatter_detect = %d\t", chatter_detect);
  printf("command_to_heater = %d\n", command_to_heater);
  printf("========================================\n");
#endif
/*
#ifdef KLEE_ASSUMES
  klee_assert(on_counter <= burnout_time);
#endif
*/
  return (void*)0;
}
