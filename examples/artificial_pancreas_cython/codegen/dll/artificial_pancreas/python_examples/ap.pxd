
#cdef extern from "artificial_pancreas_ifc.h":
cdef extern from 'artificial_pancreas.h':

    extern void artificial_pancreas(double t_start, double T_end, const double XX[3], double D[24], double P, double U, double I, double property_check, double *tt, double YY[3], double D_[24], double *P_, double *prop_violated_flag)

    extern double mealEvents(double t, const double mealData_times[2])

cdef extern from 'artificial_pancreas_initialize.h':
    extern void artificial_pancreas_initialize()

cdef extern from 'artificial_pancreas_terminate.h':
    extern void artificial_pancreas_terminate()

