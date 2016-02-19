from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
import numpy as np
cimport numpy as np

# Required to call np.import_array()
# else, segfaults!
# Reference: https://github.com/cython/cython/wiki/tutorials-numpy
np.import_array()


#Initialize the application.
#You do not need to do this more than one time.
def init():
    satellite_MEE_initialize()

#Invoke the entry-point functions.
#You can call entry-point functions multiple times.
def sim(t, T, XX, D, P, U, I, pc, dense_traces):
    cdef double cXX[6]
    cXX = XX
    #XX = np.array([100, 90, 0])


    cdef emxArray_real_T *tt
    #YY = np.array([0.,0.,0.])
    cdef emxArray_real_T *YY
    cdef double pvf
    cdef double P_
    D_ = 0.0

    emxInitArray_real_T(&tt, 1);
    emxInitArray_real_T(&YY, 2);

    #print t, T, cXX
    satellite_MEE(t, T, cXX, D, P, U, I, pc, dense_traces, tt, YY, &D_, &P_, &pvf);

    #cdef double *YY_data = <double*> PyMem_Malloc(YY.allocatedSize * sizeof(double))

    #print 'numdim:', YY.numDimensions
    #print 'size:', YY.size[0], YY.size[1]
    #print 'allocSize:', YY.allocatedSize

    # TODO: cannot execute the below call!
    # error: cannot send accross C pointers
    #YY_Data = c2python_array(YY)
    cdef np.npy_intp dims[2]
    # Matlab stores arrays rowise: [r0;r1;r2;...]
    # Do transpose shenanigans to get it in numpy format
    dims[0] = YY.size[1]
    dims[1] = YY.size[0]
    YY_data = np.PyArray_SimpleNewFromData(2, dims, np.NPY_DOUBLE, YY.data)
    # Create a copy as we need to de-allocate the memory
    # TODO: can we avoid that somehow? Hand over the memory to
    # Python's GC?
    YY_data = YY_data.T.copy()
    #print YY_data.T


    cdef np.npy_intp tdims[1]
    tdims[0] = tt.size[0]
    tt_data = np.PyArray_SimpleNewFromData(1, tdims, np.NPY_DOUBLE, tt.data)
    tt_data = tt_data.copy()

    emxDestroyArray_real_T(YY);
    emxDestroyArray_real_T(tt);

    return tt_data, YY_data, 0, 0, pvf

    #return tt, YY, D_, P_, pvf

#Terminate the application.
#You do not need to do this more than one time.
def terminate():
    satellite_MEE_terminate()

def hello():
    print 'hello-sat!'

# # Reference:
# http://stackoverflow.com/questions/30357115/pyarray-simplenewfromdata-example
# http://docs.scipy.org/doc/numpy-1.10.1/user/c-info.how-to-extend.html

# def c2python_array(emxArray_real_T *YY):
#     #PyObject * PyArray_SimpleNewFromData( int nd, npy_intp* dims, int typenum, void* data)
#     nd = 2
#     cdef int dims[2];
#     dims[0] = YY.size[0]
#     dims[1] = YY.size[1];
#     return PyArray_SimpleNewFromData(nd, dims, NPY_FLOAT64, YY.data)
