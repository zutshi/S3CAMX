
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

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val);
void controller_init();
