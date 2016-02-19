

cdef extern from 'rtwtypes.h':
    ctypedef unsigned char boolean_T

cdef extern from 'satellite_MEE_types.h':
    struct emxArray_real_T:
        double *data
        int *size
        int allocatedSize
        int numDimensions
        boolean_T canFreeData

cdef extern from 'satellite_MEE_emxAPI.h':
    extern void emxInitArray_real_T(emxArray_real_T **pEmxArray, int numDimensions)
    extern void emxDestroyArray_real_T(emxArray_real_T *emxArray)

cdef extern from 'satellite_MEE.h':
    extern void satellite_MEE(double t, double T, const double XX[6], double D, double P, double U, double I, double pc, double dense_traces, emxArray_real_T * t_arr, emxArray_real_T *x_arr, double *D_, double *P_, double *prop_violated_flag)

cdef extern from 'satellite_MEE_initialize.h':
    extern void satellite_MEE_initialize()

cdef extern from 'satellite_MEE_terminate.h':
    extern void satellite_MEE_terminate()
