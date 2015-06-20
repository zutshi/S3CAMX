// TODO: generate the num satate macros automatically

#include <klee/klee.h>
#define NUM_STATES (4)
#define NUM_OUTPUTS (1)
#define NUM_INPUTS (8)
#define NUM_X (0)

typedef struct{
    int* state_arr;
    unsigned char* output_arr;
}RETURN_VAL;

typedef struct{
    int* input_arr;
    int* state_arr;
    int* x_arr;
}INPUT_VAL;

void* controller(INPUT_VAL* iv, RETURN_VAL* rv);
