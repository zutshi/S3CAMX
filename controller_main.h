// TODO: generate the file automatically!

#define UNROLL (0)
#define CONCOLIC (1)
#define SYMBOLIC (2)

//#define MODE (CONCOLIC)
#define CONTROLLER_MODE SYMBOLIC

#define NUM_STATES (1)
#define NUM_OUTPUTS (1)
#define NUM_INPUTS (0)
#define NUM_X (1)

// DO NOT change structure signatures without modifying csim.py and controlifc.py !!!!!!

int input_arr[1];

typedef struct{
    int* state_arr;
    int* output_arr;
}RETURN_VAL;

typedef struct{
    //int* input_arr;
    int* state_arr;
    int* x_arr;
}INPUT_VAL;

void* controller(INPUT_VAL* iv, RETURN_VAL* rv);
void controller_init();
