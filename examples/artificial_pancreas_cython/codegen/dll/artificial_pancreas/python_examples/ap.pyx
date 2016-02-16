import numpy as np

#Initialize the application.
#You do not need to do this more than one time.
def init():
    artificial_pancreas_initialize()

#Invoke the entry-point functions.
#You can call entry-point functions multiple times.
def sim(t, T, XX, D, P, U, I, pc):
    #t = 0
    #T = 10

    cdef double cXX[3]
    cXX = XX
    #XX = np.array([100, 90, 0])

    cdef double cD[24]
    cD = D #D = np.array([720, 0, 40] + [0]*21)

    #P = 0
    #U = 0
    #I = 10
    #pc = 0.0

    cdef double tt
    #YY = np.array([0.,0.,0.])
    cdef double YY[3]
    cdef double pvf
    cdef double D_[24]# = np.zeros((24,1))
    cdef double P_

    #cdef double *my_array = <double *>malloc(number * sizeof(double))


    artificial_pancreas(t, T, cXX, cD, P, U, I, pc, &tt, YY, D_, &P_, &pvf)
    return tt, YY, D_, P_, pvf

#Terminate the application.
#You do not need to do this more than one time.
def terminate():
    artificial_pancreas_terminate()

def hello():
    print 'hello!'
