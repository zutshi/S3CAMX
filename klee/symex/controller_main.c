
#include <klee/klee.h>
#include "controller_main.h"
int main() {
    INPUT_VAL iv;
    RETURN_VAL rv;

    // controller new state array
    int state_arr_[NUM_STATES];

    // controller output array
    int output_arr[NUM_OUTPUTS];

    // extraneous input arr, TODO:add later
    //int input_arr[NUM_INPUTS];

    // controller present state array
    //int state_arr[NUM_STATES] = { 1, 12, 123 };
    int state_arr[NUM_STATES];

    // plant state array
    int x_arr[NUM_X];

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
    // make extraneous inputs symbolic: TODO:add later
    klee_make_symbolic(input_arr, sizeof(input_arr), "input_arr");

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
    klee_assume(x_arr[0] >= 1790);
klee_assume(x_arr[0] <= 1821);
klee_assume(state_arr[0] >= 0);
klee_assume(state_arr[0] <= 0);
klee_assume(input_arr[0] >= 0);
klee_assume(input_arr[0] <= 0);


    // controller init functions need to be defined
    controller_init();

    iv.state_arr = state_arr;
    iv.x_arr = x_arr;
    //TODO: add later
    //iv.input_arr = input_arr; 

    rv.state_arr = state_arr_;
    rv.output_arr = output_arr;

    // ignore return value.
    controller(&iv, &rv);

    // add provided klee asserts
    //klee_assert(rv.output_arr[0] == 0U);

    return 0;
}
