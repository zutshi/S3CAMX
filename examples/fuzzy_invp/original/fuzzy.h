
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

void fuzzy_init(FUZ_SYS *fuzzy_system);
void fuzzy_free(FUZ_SYS *fuzzy_system);
double fuzzy_control(double e, double edot, FUZ_SYS *fuzzy_system);
void fuzzyify(double u, IN_MEM *mem);
double leftall(double u, double w, double c);
double rightall(double u, double w, double c);
double triangle(double u, double w, double c);
void match(const IN_MEM *emem, const IN_MEM *edotmem, int *pos);
double inf_defuzz(IN_MEM *emem, IN_MEM *edotmem, OUT_MEM *outmem, int *pos);

/************************************************************************************/
