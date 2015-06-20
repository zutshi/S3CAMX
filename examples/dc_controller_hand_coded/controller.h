// TODO: generate the num satate macros automatically

#define UNROLL (0)
#define CONCOLIC (1)
#define SYMBOLIC (2)

//#define MODE (CONCOLIC)
#define CONTROLLER_MODE SYMBOLIC

#define NUM_STATES (3)
#define NUM_OUTPUTS (1)
#define NUM_INPUTS (1)
#define NUM_X (2)

typedef struct{
    int* state_arr;
    int* output_arr;
}RETURN_VAL;

typedef struct{
    int* input_arr;
    int* state_arr;
    int* x_arr;
}INPUT_VAL;

void* controller(INPUT_VAL* iv, RETURN_VAL* rv);
void controller_init();
