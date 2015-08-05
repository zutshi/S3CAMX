// TODO: generate the num satate macros automatically

//#define NUM_STATES ()
//#define NUM_OUTPUTS ()
//#define NUM_INPUTS ()
//#define NUM_X ()

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
