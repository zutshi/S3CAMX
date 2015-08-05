/*
  Program:     fuzzy.c
  Written by:  Scott Brown

  2 input fuzzy controller to control inverted pendulum system.  Controller has
  5 membship functions for each input and 5 membership functions for the output.
  Center-of-gravity is used for defuzzification.
*/
# include "controller.h"
//#include <math.h>
//#include <stdlib.h>

//#define ENABLE_PRINTS

#ifdef ENABLE_PRINTS
  #include <stdio.h>
#endif

//#define FIX_POINT

/*
 * Warning: Overflow happens with CONVERSION_FACTOR = 1k and higher
 * This also leads to plant unstability.
 *
 * Corner cases can be seen with CONVERSION_FACTOR = 300 and seed48(0)
 * by plotting the control input
 */

#ifdef FIX_POINT
  #define CONVERSION_FACTOR (100)
#else
  #define CONVERSION_FACTOR (1.0)
#endif


#define MAX(A,B)  ((A) > (B) ? (A) : (B))
#define MIN(A,B)  ((A) < (B) ? (A) : (B))

#ifdef FIX_POINT
  #define PI (3.14159265359*CONVERSION_FACTOR)
#else
  #define PI 3.14159265359
#endif
//#define PI ((double)(3.14159265359*CONVERSION_FACTOR))


/************************************************************************************/

typedef struct in_mem {
  double width;         /* Input membership function width (1/2 of triangle base).  */
  double *center;       /* Center of each input membership function.                */
  double *dom;          /* Degree of membership for each membership function.       */
} IN_MEM;

typedef struct out_mem {
  double width;         /* Output membership function width (1/2 of triangle base). */
  double *center;       /* Center of each output membership function.               */
} OUT_MEM;

typedef struct fuz_sys {
  IN_MEM  *emem;        /* Groups all fuzzy system parameters in a single variable. */
  IN_MEM  *edotmem;
  OUT_MEM *outmem;
} FUZ_SYS;

/************************************************************************************/

/* Function Prototypes: */

void fuzzy_init(FUZ_SYS *fuzzy_system, IN_MEM *e, IN_MEM *edot, OUT_MEM *out);
double fuzzy_control(double e, double edot, FUZ_SYS *fuzzy_system);
void fuzzyify(double u, IN_MEM *mem);
double leftall(double u, double w, double c);
double rightall(double u, double w, double c);
double triangle(double u, double w, double c);
void match(const IN_MEM *emem, const IN_MEM *edotmem, int *pos);
double inf_defuzz(IN_MEM *emem, IN_MEM *edotmem, OUT_MEM *outmem, int *pos);

/************************************************************************************/

double fuzzy_control(double e, double edot, FUZ_SYS *fuzzy_system) {
  
/* Given crisp inputs e and edot, determine the crisp output u. */

  int pos[2];
  
  fuzzyify(e, fuzzy_system->emem);
  fuzzyify(edot, fuzzy_system->edotmem);
  match(fuzzy_system->emem, fuzzy_system->edotmem, pos);
  return inf_defuzz(fuzzy_system->emem, fuzzy_system->edotmem, fuzzy_system->outmem, pos); 
}

/************************************************************************************/

void fuzzyify(double u, IN_MEM *mem) {

/* Fuzzify the input u by determining the degree of membership for each membership
   function in mem. Assumes 5 membership functions, with first and last membership
   functions leftall and rightall respectively.  Other membership functions are
   triangular. */
 
  int i;

  mem->dom[0] = leftall(u, mem->width, mem->center[0]);
  for (i=1; i<4; i++) 
    mem->dom[i] = triangle(u, mem->width, mem->center[i]);
  mem->dom[4] = rightall(u, mem->width, mem->center[4]);

#ifdef ENABLE_PRINTS
  printf("======Fuzzify=====\n");
  for(i=0; i<5; i++)
  {
#ifdef FIX_POINT
    printf("%d, ", mem->dom[i]);
#else
    printf("%f, ", mem->dom[i]);
#endif
  }
  printf("\n\n");
#endif
}

/************************************************************************************/

double leftall(double u, double w, double c)

/* Determine degree of membership for a leftall membership function.
   NOTE:  u is input, c is mem. fun. center, and w is mem. fun. width. */

{
  if (u < c)
    return 1.0;
  else
    //return MAX(0,(1-(u-c)/w));
    return MAX(0,(1*CONVERSION_FACTOR-(u-c)*CONVERSION_FACTOR/w));
} 

/************************************************************************************/

double rightall(double u, double w, double c)
/* Determine degree of membership for a RIGHTALL membership function
   NOTE:  u is input, c is mem. fun. center, and w is mem. fun. width. */

{
  if (u >= c)
         return 1.0;
  else
         return MAX(0,(1*CONVERSION_FACTOR-(c-u)*CONVERSION_FACTOR/w));
}

/************************************************************************************/

double triangle(double u, double w, double c)

/* Determine degree of membership for a TRIANGLE membership function
   NOTE:  u is input, c is mem. fun. center, and w is mem. fun. width. */

{
  if (u >= c)
    return MAX(0,(1*CONVERSION_FACTOR-(u-c)*CONVERSION_FACTOR/w));
  else
    return MAX(0,(1*CONVERSION_FACTOR-(c-u)*CONVERSION_FACTOR/w));
}

/************************************************************************************/

void match(const IN_MEM *emem, const IN_MEM *edotmem, int *pos) {

/* For each universe of discourse, determine the index of the first membership function
   with a non-zero degree (i.e. match the rules to the current inputs to find which rules 
   are on).  These indices are used to determine which four rules to evaluate.  (NOTE: 
   A 2 input sytem with no more than 50% overlap for input membership functions only
   requires the evaluation of at most 4 rules.) */ 
  
  int i;

  for (i=0; i<5; i++) {
    if(emem->dom[i] != 0) {
      pos[0] = i;
      break;
    }
  }
  for (i=0; i<5; i++) {
    if(edotmem->dom[i] != 0) {
      pos[1] = i;
      break;
    }
  }
}

/************************************************************************************/

double inf_defuzz(IN_MEM *emem, IN_MEM *edotmem, OUT_MEM *outmem, int *pos) {

/* We use the degrees of membership found in the function match() to form the implied
   fuzzy sets. The correct output membership function for each rule is determined by
   adding (and saturating) a shifted version of the input membership function indices
   (this implements the typical pattern of linguistic-numeric indices in the body of 
   the table of rules).  In this way we compute the rule-base at every step, rather
   than storing the rule-base in a table.  Defuzzification is also performed using
   the center-of-gravity method.  A crisp output is returned. */


  double outdom, area, Atot = 0, WAtot = 0;
  int i, j, out_index;

  for(i=0; i<2; i++) {
    for(j=0; j<2; j++) {
      if ( ((pos[0]+i)<5) && ((pos[1]+j)<5)) { /* Check that bounds are not exceeded. */
        outdom = 0;

        /* Shift indices left. */
        out_index = ((pos[0]+i)-2) + ((pos[1]+j)-2); 

        /* Saturate */
        if (out_index < -2)
          out_index = -2;
        else if (out_index > 2)
          out_index = 2;

        /* Shift indices right.*/
        out_index += 2;

        /* Determine the certainty of the premise */
        outdom = MIN((emem->dom[pos[0]+i]), (edotmem->dom[pos[1]+j]));

        /* Defuzzify */
        area = 2 * outmem->width * (outdom - (outdom * outdom)/CONVERSION_FACTOR/2);
        Atot += area;
        WAtot += area*outmem->center[out_index];
      }
    }
  }
  /* Return the crisp value.  Minus sign required to give correct output for 
     pendulum system!  Note that this minus sign actually ensures that the table of
     indices works out as shown in class. */

#ifdef ENABLE_PRINTS
#ifdef FIX_POINT
  printf("WAtot=%d, Atot=%d\n", WAtot, Atot);
#else
  printf("WAtot=%f, Atot=%f\n", WAtot, Atot);
#endif
#endif
  return -(WAtot/Atot);
}
 
/************************************************************************************/ 

#if 0  /* Set to zero to call fuzzy_control() from another program. */ 

/* Test I/O behavior of fuzzy controller. */

int main(void) {

/* Test for input given below.  Output is -6.818182. */

  double e, edot, u;
  FUZ_SYS fuzzy_system;

  /* Crips inputs. */
  e = 0;                 
  edot = ((PI)/8.0 - (PI)/32);

  /* allocate static memory*/
  IN_MEM em, edotm;
  OUT_MEM outm;
  double e_center[5]={0,0,0,0,0};
  double e_dom[5]={0,0,0,0,0};
  double edot_center[5]={0,0,0,0,0};
  double edot_dom[5]={0,0,0,0,0};
  double out_center[5]={0,0,0,0,0};

  em.center = e_center;
  em.dom = e_dom;
  edotm.center = edot_center;
  edotm.dom = edot_dom;
  outm.center = out_center;
  /* mem alloc done */

  fuzzy_init(&fuzzy_system, &em, &edotm, &outm);
  u = fuzzy_control(e,edot,&fuzzy_system);

#ifdef ENABLE_PRINTS
#ifdef FIX_POINT
  printf("e = %d, edot = %d, u = %d\n",e,edot,u);
#else
  printf("e = %f, edot = %f, u = %f\n",e,edot,u/CONVERSION_FACTOR); 
#endif
#endif
  return 0;
}
#else
void controller_init(){
  //empty initializer
}

void* controller(INPUT_VAL* input, RETURN_VAL* ret_val)
{
  double e, edot, u;
  FUZ_SYS fuzzy_system;
  /* allocate static memory*/
  IN_MEM em, edotm;
  OUT_MEM outm;
  double e_center[5]={0,0,0,0,0};
  double e_dom[5]={0,0,0,0,0};
  double edot_center[5]={0,0,0,0,0};
  double edot_dom[5]={0,0,0,0,0};
  double out_center[5]={0,0,0,0,0};

#ifdef KLEE_ASSUMES
  /*
  klee_assume((input->x_arr[0] >= -100)&(input->x_arr[0] <= 100));
  klee_assume((input->x_arr[1] >= -60)&(input->x_arr[1] <= 60));
  klee_assume((input->x_arr[2] >= -100)&(input->x_arr[2] <= 150));
  */
  klee_assume((input->x_arr[0] >= 0)&(input->x_arr[0] <= 100));
  klee_assume((input->x_arr[1] >= -20)&(input->x_arr[1] <= 160));
  klee_assume((input->x_arr[2] >= -500)&(input->x_arr[2] <= 2000));
#endif

  /* Crisp inputs. */
  e = -input->x_arr[0];
  edot = -input->x_arr[1];
  //printf("e = %d, edot = %d\n", e, edot);

  em.center = e_center;
  em.dom = e_dom;
  edotm.center = edot_center;
  edotm.dom = edot_dom;
  outm.center = out_center;

  fuzzy_init(&fuzzy_system, &em, &edotm, &outm);
  // call the actual controller
  u = fuzzy_control(e,edot,&fuzzy_system);

  ret_val->output_arr[0] = u;

#ifdef ENABLE_PRINTS
#ifdef FIX_POINT
  printf("e = %d, edot = %d, u = %d\n",e,edot,u);
#else
  printf("e = %f, edot = %f, u = %f\n",e,edot,u); 
#endif
#endif


  // ignore third state input->x_arr[2]

  /* Below assumes are valid for 
   * e0     \in [-0.5, 0.5]
   * edot0  \in [-0.5, 0.5]
   * x0     \in [-0.5, 0.5]
   * T <= 3s, \delta_t = 0.01
   */
/*
  klee_assume((e >= -100)&(e <= 100));
  klee_assume((edot >= -60)&(edot <= 60));
  klee_assume((u >= -20*100)&(u <= 20*100));
*/
  /* Below assumes are valid for 
   * e0     \in [-0.5, 0.5]
   * edot0  \in [-0.5, 0.5]
   * x0     \in [-0.5, 0.5]
   * T <= 5s, \delta_t = 0.01
   */
  /*
  klee_assume((e >= -8*100)&(e <= 8*100));
  klee_assume((edot >= -12*100)&(edot <= 12*100));
  klee_assume((u >= -20*100)&(u <= 20*100));
  */


  return 0;
}
#endif

void fuzzy_init(FUZ_SYS *fuzzy_system, IN_MEM *em, IN_MEM *edotm, OUT_MEM *outm) {

/* Define the input and output membership functions. */  

  int i;

  /* Allocate memory for membership functions. */
  fuzzy_system->emem = em;
  fuzzy_system->edotmem = edotm;
  fuzzy_system->outmem = outm;

  /* Initialize for inverted pendulum. */
  fuzzy_system->emem->width = (PI)/4.0;  /* Width defined to be 1/2 of triangle base. */
  fuzzy_system->edotmem->width = (PI)/8.0;
  fuzzy_system->outmem->width = 10*CONVERSION_FACTOR;

  for (i=0; i<5; i++) {
    fuzzy_system->emem->center[i] = (-(PI)/2.0 + i*(PI)/4.0);
    fuzzy_system->edotmem->center[i] = (-(PI)/4.0 + i*(PI)/8.0);
    fuzzy_system->outmem->center[i] = (-20.0 + i*10.0)*CONVERSION_FACTOR;
#ifdef ENABLE_PRINTS
#ifdef FIX_POINT
    printf("%d %d %d\n", fuzzy_system->emem->center[i],fuzzy_system->edotmem->center[i],fuzzy_system->outmem->center[i]);
#else
    printf("%f %f %f\n", fuzzy_system->emem->center[i],fuzzy_system->edotmem->center[i],fuzzy_system->outmem->center[i]);
#endif
#endif
  }
}
