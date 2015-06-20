
#include "continuous_kobuna_FP.h"      /* Model's header file */
#include "controller.h"

int main() {
    INPUT_VAL iv;
    RETURN_VAL rv;

    int state_arr_[NUM_STATES];
    unsigned char output_arr[NUM_OUTPUTS] = {0U};

    int state_arr[NUM_STATES] = {0, 0, 0, 0};
    int x_arr[NUM_X];


    int input_arr_0[NUM_INPUTS];
    int input_arr_1[NUM_INPUTS];
    int input_arr_2[NUM_INPUTS];
    
    int input_arr_3[NUM_INPUTS];
    int input_arr_4[NUM_INPUTS];


    controller_init();


//    klee_make_symbolic(state_arr, sizeof(state_arr), "state_arr");
//    klee_make_symbolic(x_arr, sizeof(x_arr), "x_arr");
//    klee_make_symbolic(input_arr, sizeof(input_arr), "input_arr");


    klee_make_symbolic(input_arr_0, sizeof(input_arr_0), "input_arr_0");
    klee_make_symbolic(input_arr_1, sizeof(input_arr_1), "input_arr_1");
    klee_make_symbolic(input_arr_2, sizeof(input_arr_2), "input_arr_2");
    klee_make_symbolic(input_arr_3, sizeof(input_arr_3), "input_arr_3");
    klee_make_symbolic(input_arr_4, sizeof(input_arr_4), "input_arr_4");

/*  
    klee_assume((input_arr[0] <= 100)&(input_arr[0] >= 0));
    klee_assume((input_arr[1] <= 100)&(input_arr[1] >= 0));
    klee_assume((input_arr[2] <= 100)&(input_arr[2] >= 0));
    klee_assume((input_arr[3] <= 100)&(input_arr[3] >= 0));
    klee_assume((input_arr[4] <= 100)&(input_arr[4] >= 0));
    klee_assume((input_arr[5] <= 100)&(input_arr[5] >= 0));
    klee_assume((input_arr[6] <= 100)&(input_arr[6] >= 0));
    klee_assume((input_arr[7] <= 100)&(input_arr[7] >= 0));
*/

    klee_assume((input_arr_0[0] <= 100)&(input_arr_0[0] >= 0));
    klee_assume((input_arr_0[1] <= 100)&(input_arr_0[1] >= 0));
    klee_assume((input_arr_0[2] <= 100)&(input_arr_0[2] >= 0));
    klee_assume((input_arr_0[3] <= 100)&(input_arr_0[3] >= 0));
    klee_assume((input_arr_0[4] <= 100)&(input_arr_0[4] >= 0));
    klee_assume((input_arr_0[5] <= 100)&(input_arr_0[5] >= 0));
    klee_assume((input_arr_0[6] <= 100)&(input_arr_0[6] >= 0));
    klee_assume((input_arr_0[7] <= 100)&(input_arr_0[7] >= 0));
/*
    klee_assume((input_arr_1[0] <= 100)&(input_arr_1[0] >= 0));
    klee_assume((input_arr_1[1] <= 100)&(input_arr_1[1] >= 0));
    klee_assume((input_arr_1[2] <= 100)&(input_arr_1[2] >= 0));
    klee_assume((input_arr_1[3] <= 100)&(input_arr_1[3] >= 0));
    klee_assume((input_arr_1[4] <= 100)&(input_arr_1[4] >= 0));
    klee_assume((input_arr_1[5] <= 100)&(input_arr_1[5] >= 0));
    klee_assume((input_arr_1[6] <= 100)&(input_arr_1[6] >= 0));
    klee_assume((input_arr_1[7] <= 100)&(input_arr_1[7] >= 0));

    klee_assume((input_arr_2[0] <= 100)&(input_arr_2[0] >= 0));
    klee_assume((input_arr_2[1] <= 100)&(input_arr_2[1] >= 0));
    klee_assume((input_arr_2[2] <= 100)&(input_arr_2[2] >= 0));
    klee_assume((input_arr_2[3] <= 100)&(input_arr_2[3] >= 0));
    klee_assume((input_arr_2[4] <= 100)&(input_arr_2[4] >= 0));
    klee_assume((input_arr_2[5] <= 100)&(input_arr_2[5] >= 0));
    klee_assume((input_arr_2[6] <= 100)&(input_arr_2[6] >= 0));
    klee_assume((input_arr_2[7] <= 100)&(input_arr_2[7] >= 0));

    klee_assume((input_arr_3[0] <= 100)&(input_arr_3[0] >= 0));
    klee_assume((input_arr_3[1] <= 100)&(input_arr_3[1] >= 0));
    klee_assume((input_arr_3[2] <= 100)&(input_arr_3[2] >= 0));
    klee_assume((input_arr_3[3] <= 100)&(input_arr_3[3] >= 0));
    klee_assume((input_arr_3[4] <= 100)&(input_arr_3[4] >= 0));
    klee_assume((input_arr_3[5] <= 100)&(input_arr_3[5] >= 0));
    klee_assume((input_arr_3[6] <= 100)&(input_arr_3[6] >= 0));
    klee_assume((input_arr_3[7] <= 100)&(input_arr_3[7] >= 0));

    klee_assume((input_arr_4[0] <= 100)&(input_arr_4[0] >= 0));
    klee_assume((input_arr_4[1] <= 100)&(input_arr_4[1] >= 0));
    klee_assume((input_arr_4[2] <= 100)&(input_arr_4[2] >= 0));
    klee_assume((input_arr_4[3] <= 100)&(input_arr_4[3] >= 0));
    klee_assume((input_arr_4[4] <= 100)&(input_arr_4[4] >= 0));
    klee_assume((input_arr_4[5] <= 100)&(input_arr_4[5] >= 0));
    klee_assume((input_arr_4[6] <= 100)&(input_arr_4[6] >= 0));
    klee_assume((input_arr_4[7] <= 100)&(input_arr_4[7] >= 0));
*/
//    iv.state_arr = state_arr;
//    iv.x_arr = x_arr;

//    rv.state_arr = state_arr_;

    rv.output_arr = output_arr;

    // ignore return value.
    iv.input_arr = input_arr_0;
    controller(&iv, &rv);
/*
    iv.input_arr = input_arr_1;
    controller(&iv, &rv);

    iv.input_arr = input_arr_2;
    controller(&iv, &rv);

    iv.input_arr = input_arr_3;
    controller(&iv, &rv);

    iv.input_arr = input_arr_4;
    controller(&iv, &rv);
*/
    klee_assert(rv.output_arr[0] == 0U);

    return 0;
}

