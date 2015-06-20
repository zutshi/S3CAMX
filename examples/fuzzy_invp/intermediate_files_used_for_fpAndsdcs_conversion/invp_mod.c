/*
 * The same as the origianl, but the interface has been changed to work with
 * the new style controller: fuzzy_controller.c
 */

/*
  Program:     rk4.c
  Written by:  Scott Brown

  Fourth Order Runge-Kutta Algorithm, for use with single-input systems.

  Function rk4(double *t, double *y, double u, double h, int n) is called
  with the 5 arguments indicated.  Note that the first two arguments are
  pointers.  Also note that no values are returned.  Derivatives must first
  be defined in function deriv.  Time is updated within rk4 call, so should
  not be updated by programmer in calling loop.  The arguments for rk4() are
  defined below:

           double *t  :  pointer to time
           double *y  :  pointer to states
           double  u  :  system input (for discrete simulations)
           double  h  :  integration step size
           int     n  :  system order

  The parameter u is useful for simulating discrete-time systems or physical
  systems in a laboratory.  For continuous system simulation the input should
  be calculated within the deviv() function.
*/

/***************************************************************************
*********/

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include "controller.h"

/***************************************************************************
*********/

/* Data Types */

typedef struct rk_struct {
  double *f1;    /* Pointers to the Runge-Kutta coefficient arrays. */
  double *f2;
  double *f3;
  double *f4;
  double *arg2;  /* Pointer to a temporary vector used in several functions. */
} RK_STRUCT;

/***************************************************************************
*********/

/* Application dependent area; change as necessary. */

//#include "fuzzy.h"    /* Include fuzzy functions. */

/* Global Variables */

//FUZ_SYS fuzzy_system; /* Define fuzzy_system as a global variable.  */
double input;         /* System input; used to store input to file. */

/***************************************************************************
*********/

/* Function Prototypes */

void rk4(RK_STRUCT *rks, double *t, double *y, double u, double h, int n);
void deriv(double t, const double *y, double u, double *ydot);
void F1(double t, const double *y, double u, double h, int n, double *f1);
void F2(double t, const double *y, double u, double h, int n,
        const double *f1, double *f2, double *arg2);
void F3(double t, const double *y, double u, double h, int n,
        const double *f2, double *f3, double *arg2);
void F4(double t, const double *y, double u, double h, int n,
        const double *f3, double *f4, double *arg2);
void rk_init(RK_STRUCT *rks, int n);
void rk_free(RK_STRUCT *rks);

/***************************************************************************
*********/

/* Implementation */

void deriv(double t, const double *y, double u, double *ydot) {
  int e_edot_[2], u_;
  INPUT_VAL iv;
  RETURN_VAL rv;

  /* This is where the derivative is defined:  xdot = f(t,x,u). */

  /* Example:  xdot = A*x + b*u (time invariant system)

  ydot[0] = -2*y[0] + -u;          | -2   0   0 |      | -1 |
  ydot[1] = -3*y[1] + 2*u;       A=|  0  -3   0 |,   B=|  2 |
  ydot[2] = -4*y[2] + u;           |  0   0  -4 |      |  1 |

  */

   /*******  INSERT YOUR DERIVATIVE DEFINITION HERE:  ********/

  double e,edot;

  /* Determine the system input u.  Because the system is continuous, the input
     is calculated within the deriv() function.  For discrete time systems, the
     input can be calculated and passed to deriv() via the u paramater. */

  e = -y[0];
  edot = -y[1];
  e_edot_[0] = (int)(e*CONVERSION_FACTOR);
  e_edot_[1] = (int)(edot*CONVERSION_FACTOR);
  //u = fuzzy_control(e,edot,&fuzzy_system);
  iv.x_arr = e_edot_;
  rv.output_arr = &u_;

  controller(&iv, &rv);
  u = ((double)u_)/CONVERSION_FACTOR;
  
  input = u; /* Store u in input for plotting. */

  /* Inverted pendulum dynamics. */

  ydot[0] = y[1];
  ydot[1] =
(9.8*sin(y[0]) + cos(y[0])*(-y[2] -
0.25*pow(y[1],2.0)*sin(y[0]))/1.5)/(.5*(4.0/3.0 - 1.0/3.0*pow(cos(y[0]),2.0)));
  ydot[2] = 100.0*u -100.0*y[2];  /* Actuator dynamics */

}

/***************************************************************************
*********/

void rk4(RK_STRUCT *rks, double *t, double *y, double u, double h, int n) {

  int i;

  /* Determine Runge-Kutta Coefficients. */

  F1(*t,y,u,h,n,rks->f1);
  F2(*t,y,u,h,n,rks->f1,rks->f2,rks->arg2);
  F3(*t,y,u,h,n,rks->f2,rks->f3,rks->arg2);
  F4(*t,y,u,h,n,rks->f3,rks->f4,rks->arg2);

  /* Update time and output values. */

  *t += h;
  for (i = 0; i < n; i++) {
    y[i] += (1.0/6.0)*(rks->f1[i] + 2*(rks->f2[i]) + 2*(rks->f3[i]) +
rks->f4[i]);
  }
}

/***************************************************************************
*********/

void F1(double t, const double *y, double u, double h, int n, double *f1) {
  int i;
  deriv(t,y,u,f1);
  for (i = 0; i < n; i++) {
    f1[i] = h*f1[i];
  }
}

/***************************************************************************
*********/

void F2(double t, const double *y, double u, double h, int n,
        const double *f1, double *f2, double *arg2) {

  int i;

  for (i = 0; i < n; i++) {
    arg2[i] = y[i] + 0.5*f1[i];
  }

  deriv((t+0.5*h), arg2, u, f2);

  for (i = 0; i < n; i++) {
    f2[i] = h*f2[i];
  }
}

/***************************************************************************
*********/

void F3(double t, const double *y, double u, double h, int n,
       const double *f2, double *f3, double *arg2) {

  int i;

  for (i = 0; i < n; i++) {
    arg2[i] = y[i] + 0.5*f2[i];
  }

  deriv((t+0.5*h), arg2, u, f3);

  for (i = 0; i < n; i++) {
    f3[i] = h*f3[i];
  }
}

/***************************************************************************
*********/

void F4(double t, const double *y, double u, double h, int n,
        const double *f3, double *f4, double *arg2) {

  int i;

  for (i = 0; i < n; i++) {
    arg2[i] = y[i] + f3[i];
  }

  deriv((t+h), arg2, u, f4);

  for (i = 0; i < n; i++) {
    f4[i] = h*f4[i];
  }
}

/***************************************************************************
*********/

void rk_init(RK_STRUCT *rks, int n) {

 /* Allocate memory. */

  if (!(rks->f1 = (double *) malloc(n*sizeof(double)))) {
    printf("Error allocating memory.\n");
    exit(1);
  }
  if (!(rks->f2 = (double *) malloc(n*sizeof(double)))) {
    printf("Error allocating memory.\n");
    exit(1);
  }
  if (!(rks->f3 = (double *) malloc(n*sizeof(double)))) {
    printf("Error allocating memory.\n");
    exit(1);
  }
  if (!(rks->f4 = (double *) malloc(n*sizeof(double)))) {
    printf("Error allocating memory.\n");
    exit(1);
  }
  if (!(rks->arg2 = (double *) malloc(n*sizeof(double)))) {
    printf("Error allocating memory.\n");
    exit(1);
  }
}
/***************************************************************************
*********/

void rk_free(RK_STRUCT *rks) {

  /* Free allocated memory */

  free(rks->f1);
  free(rks->f2);
  free(rks->f3);
  free(rks->f4);
  free(rks->arg2);
}
/***************************************************************************
*********/

#if 1  /* Undefine main() to call rk4.c from another program. */

/* Simulate the pendulum system with fuzzy controller. */

int main(void) {

  int MAX_SIMS = 10;//MAX_SAMPLES;
  int num_sims = 0;

  double
    u,
    t,
    h = 0.001,             /* Integration step size.  */
    //y[3] = {0.1,0.0,0.0},  /* Initial conditions.     */
    y[3],
    tmax = 100;              /* Simulation time period. */

  double yl[3] = {-.3, -0.3, -0.0},
         yh[3] = {0.3, 0.3, 0.0};

  int n = 3;                 /* System order. */

  RK_STRUCT rks;

  FILE *fp;

  if (!(fp = fopen("output_fp","w"))) {
    printf("Can't open file.\n");
    exit(1);
  }

  /* Initialization area. */
  rk_init(&rks,n);
  //fuzzy_init(&fuzzy_system);

  //srand48(time(NULL));
  srand48(0);

  while(num_sims < MAX_SIMS)
  {
    t = 0;
    u = 0;
    y[0] = yl[0] + drand48() * (yh[0] - yl[0]);
    y[1] = yl[1] + drand48() * (yh[1] - yl[1]);
    y[2] = yl[2] + drand48() * (yh[2] - yl[2]);
    /* Simulate For tmax seconds. */
    while(t<tmax) {
      /* Note: u is not used here, as it is calculated inside the derivative
  function. */
      rk4(&rks,&t,y,u,h,n);
      if(((int)(t*1000))%10 == 0)
        fprintf(fp,"%f %f %f %f %f\n",t,y[0],y[1],y[2],input);
    }
    num_sims++;
  }

  /* Clean up. */
  //fuzzy_free(&fuzzy_system);
  rk_free(&rks);
  fclose(fp);
  return 0;
}

#endif

/***************************************************************************
*********/

/* END */
