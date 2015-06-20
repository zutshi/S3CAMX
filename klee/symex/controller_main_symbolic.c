
#include <klee/klee.h>
#include "controller.h"
int main() {
    INPUT_VAL iv;
    RETURN_VAL rv;

    // controller new state array
    int state_arr_[NUM_STATES];

    // controller output array
    int output_arr[NUM_OUTPUTS];

    // extraneous input arr
    int input_arr[NUM_INPUTS];

    // controller present state array
    //int state_arr[NUM_STATES] = { 1, 12, 123 };
    int state_arr[NUM_STATES];

    // plant state array
    int x_arr[NUM_X];

    int dummy_nextstate_arr[NUM_STATES];
    int dummy_output_arr[NUM_OUTPUTS];


#if CONTROLLER_MODE == UNROLL
"I can not be compiled"
#elif CONTROLLER_MODE == CONCOLIC
    // do nothing
#elif CONTROLLER_MODE == SYMBOLIC
    //make state symbolic
    klee_make_symbolic(state_arr, sizeof(state_arr), "state_arr");
#else
"I can not be compiled"
#endif

    // make X symbolic
    klee_make_symbolic(x_arr, sizeof(x_arr), "x_arr");

    // make extraneous inputs symbolic
    klee_make_symbolic(input_arr, sizeof(input_arr), "input_arr");

    klee_make_symbolic(dummy_nextstate_arr, sizeof(dummy_nextstate_arr), "dummy_nextstate_arr");
    klee_make_symbolic(dummy_output_arr, sizeof(dummy_output_arr), "dummy_output_arr");

    // not sure what the below commented code is showing...? Test it out?
    /*
    klee_make_symbolic(&s[0], sizeof(int), "s0");
    klee_make_symbolic(&x[0], sizeof(int), "x0");
    klee_make_symbolic(&s[1], sizeof(int), "s1");
    klee_make_symbolic(&x[1], sizeof(int), "x1");
    */

    /*
    s[0] = klee_int("s0");
    s[1] = klee_int("s1");
    x[0] = klee_int("x0");
    x[1] = klee_int("x1");
    */

    // write klee assumes
    // klee_assume((x[0] >= 0)&(s[0] >= 0)&(x[0] <= 10)&(s[0] <= 10));
    // klee_assume((x[1] >= 0)&(s[1] >= 0)&(x[1] <= 10)&(s[1] <= 10));

    /*
    klee_assume(x_arr[0] >= 2800);
    klee_assume(x_arr[0] <= 2900);

    klee_assume(state_arr[0] >= 0);
    klee_assume(state_arr[0] <= 0);
    */


//klee_assume(state_arr[2] >= 0);
//klee_assume(state_arr[2] <= 999);

//klee_assume(input_arr[0] >= 0);
//klee_assume(input_arr[0] <= 0);


    // controller init functions need to be defined
    controller_init();

    iv.state_arr = state_arr;
    iv.x_arr = x_arr;
    iv.input_arr = input_arr; 

    rv.state_arr = state_arr_;
    rv.output_arr = output_arr;

    // ignore return value.
    controller(&iv, &rv);

    //klee_assert(dummy_nextstate_arr[0] == state_arr_[0] & dummy_nextstate_arr[1] == state_arr_[1] & dummy_nextstate_arr[2] == state_arr_[2] & dummy_output_arr[0] == output_arr[0]);
    {
      int i = 0;
      int dummy_output_assert = 1;
      int dummy_state_assert = 1;
      for(i=0;i<NUM_OUTPUTS;i++){
        dummy_output_assert &= (dummy_output_arr[i] == output_arr[i]);
      }
      for(i=0;i<NUM_STATES;i++){
        dummy_state_assert &= (dummy_nextstate_arr[i] == state_arr_[i]);
      }
      /*
      int a1 = (dummy_output_arr[0] == output_arr[0]);
      int a2 = (dummy_nextstate_arr[0] == state_arr_[0]);
      int a3 = (dummy_nextstate_arr[1] == state_arr_[1]);
      int a4 = (dummy_nextstate_arr[2] == state_arr_[2]);
      klee_assert(a1 & a2 & a3 & a4);
      */
      klee_assert(dummy_output_assert & dummy_state_assert);
    }

    // add provided klee asserts
    //klee_assert(rv.output_arr[0] == 0U);

    return 0;
}
