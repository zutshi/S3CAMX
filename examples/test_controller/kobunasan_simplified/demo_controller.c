#include <klee/klee.h>
#include "continuous_kobuna_simpleFP.h"      /* Model's header file */
#include "controller.h"


int main() {
    INPUT_VAL iv;
    RETURN_VAL rv;

    int state_arr_[NUM_STATES];
    int output_arr[NUM_OUTPUTS] = {0};

    int state_arr[NUM_STATES] = {0, 0, 0, 0};
    int x_arr[NUM_X];


    int input_arr_0[NUM_INPUTS];

#if MODE == UNROLL
    int input_arr_1[NUM_INPUTS];
    int input_arr_2[NUM_INPUTS];
    int input_arr_3[NUM_INPUTS];
    int input_arr_4[NUM_INPUTS];
    klee_make_symbolic(input_arr_1, sizeof(input_arr_1), "input_arr_1");
    klee_make_symbolic(input_arr_2, sizeof(input_arr_2), "input_arr_2");
    klee_make_symbolic(input_arr_3, sizeof(input_arr_3), "input_arr_3");
    klee_make_symbolic(input_arr_4, sizeof(input_arr_4), "input_arr_4");
#elif MODE == CONCOLIC
    // state is not symbolic, but concrete...no splicing occurs
#elif MODE == SYMBOLIC
    // make state symbolic
    klee_make_symbolic(state_arr, sizeof(state_arr), "state_arr");
#else
"I can not be compiled"
#endif

    controller_init();

    // make input symbolic
    klee_make_symbolic(input_arr_0, sizeof(input_arr_0), "input_arr_0");
    // make X symbolic

    //assumes on input_arr
    klee_assume((input_arr_0[0] <= 100)&(input_arr_0[0] >= 0)); klee_assume((input_arr_0[1] <= 100)&(input_arr_0[1] >= 0)); klee_assume((input_arr_0[2] <= 100)&(input_arr_0[2] >= 0)); klee_assume((input_arr_0[3] <= 100)&(input_arr_0[3] >= 0));
    //assumes on X

#if MODE == UNROLL
    klee_assume((input_arr_1[0] <= 100)&(input_arr_1[0] >= 0)); klee_assume((input_arr_1[1] <= 100)&(input_arr_1[1] >= 0)); klee_assume((input_arr_1[2] <= 100)&(input_arr_1[2] >= 0)); klee_assume((input_arr_1[3] <= 100)&(input_arr_1[3] >= 0));

    klee_assume((input_arr_2[0] <= 100)&(input_arr_2[0] >= 0)); klee_assume((input_arr_2[1] <= 100)&(input_arr_2[1] >= 0)); klee_assume((input_arr_2[2] <= 100)&(input_arr_2[2] >= 0)); klee_assume((input_arr_2[3] <= 100)&(input_arr_2[3] >= 0));

    klee_assume((input_arr_3[0] <= 100)&(input_arr_3[0] >= 0)); klee_assume((input_arr_3[1] <= 100)&(input_arr_3[1] >= 0)); klee_assume((input_arr_3[2] <= 100)&(input_arr_3[2] >= 0)); klee_assume((input_arr_3[3] <= 100)&(input_arr_3[3] >= 0));

    klee_assume((input_arr_4[0] <= 100)&(input_arr_4[0] >= 0)); klee_assume((input_arr_4[1] <= 100)&(input_arr_4[1] >= 0)); klee_assume((input_arr_4[2] <= 100)&(input_arr_4[2] >= 0)); klee_assume((input_arr_4[3] <= 100)&(input_arr_4[3] >= 0));
#elif MODE == CONCOLIC
    // state is not symbolic, but concrete...no assumptions are defined
#elif MODE == SYMBOLIC
    klee_assume((state_arr[0] <= 10)&(state_arr[0] >= 0)); klee_assume((state_arr[1] <= 10)&(state_arr[1] >= 0)); klee_assume((state_arr[2] <= 10)&(state_arr[2] >= 0)); klee_assume((state_arr[3] <= 10)&(state_arr[3] >= 0));
#else
    "I can not be compiled"
#endif

    iv.state_arr = state_arr;
    iv.x_arr = x_arr;

    rv.state_arr = state_arr_;

    rv.output_arr = output_arr;

    // ignore return value.
    iv.input_arr = input_arr_0; controller(&iv, &rv);
#if MODE == UNROLL
    iv.input_arr = input_arr_1; controller(&iv, &rv);
    iv.input_arr = input_arr_2; controller(&iv, &rv);
    iv.input_arr = input_arr_3; controller(&iv, &rv);
    iv.input_arr = input_arr_4; controller(&iv, &rv);
#endif
    klee_assert(rv.output_arr[0] == 0U);

    return 0;
}

