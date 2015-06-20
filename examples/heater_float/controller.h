// TODO: generate the num satate macros automatically

#define NUM_STATES (4)
#define NUM_OUTPUTS (1)
#define NUM_INPUTS (1)
#define NUM_X (1)

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
