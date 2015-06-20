
//#include<stdio.h>


#define NUM_STATES (3)
#define NUM_OUTPUTS (2)
#define NUM_INPUTS (1)
#define NUM_X (5)

// DO NOT change structure signatures without modifying csim.py and controlifc.py !!!!!!

typedef struct{
    int* int_state_arr;
    double* float_state_arr;
    double* output_arr;
}RETURN_VAL;

typedef struct{
    double* input_arr;
    int* int_state_arr;
    double* float_state_arr;
    double* x_arr;
}INPUT_VAL;

void* controller(INPUT_VAL* iv, RETURN_VAL* rv);
void controller_init();


void controller_init(){}

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
{
    ret_val->int_state_arr[0] = input->int_state_arr[0] + 2000;
    ret_val->int_state_arr[1] = input->int_state_arr[1] + 2000;
    ret_val->int_state_arr[2] = input->int_state_arr[2] + 2000;

    ret_val->float_state_arr[0] = input->float_state_arr[0] + 1000.0;
    ret_val->float_state_arr[1] = input->float_state_arr[1] + 1000.0;
    ret_val->float_state_arr[2] = input->float_state_arr[2] + 1000.0;
    ret_val->float_state_arr[3] = input->float_state_arr[3] + 1000.0;

    ret_val->output_arr[0] = input->x_arr[0]
                             + input->x_arr[1]
                             + input->x_arr[2]
                             + input->x_arr[3]
                             + input->x_arr[4];
    
    ret_val->output_arr[1] = input->input_arr[0];

    return (void*)0;
}
