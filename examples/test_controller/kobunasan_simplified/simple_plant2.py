# Must satisfy the signature
# [t,X,D,P] = sim_function(T,X0,D0,P0,I0);

import numpy as np
from scipy.integrate import ode

MODE_1 = 1
MODE_2 = 2


# Simple Plant has no dynamics...
def sim(T, XX, D, P, U, I, property_checker, property_violated_flag):
#    X01 = [5 5]
#    A1 = [0 1;-1.1 0]
# u = 1
# C = [1 0]
# x' = Ax
# y=Cx

#   X02 = [10 10]
#   A2 = [-.1 0;0 -.1]
#C = [1 0]

    x = XX
    if D == MODE_1:
        y = x**2 - 10
    elif D == MODE_2:
        y = x**2
    else:
        raise Exception('nknown discrete mode')
    t = 1.0

    if property_checker:
        property_checker()
        property_violated_flag[0]

    dummy_D = np.zeros(D.shape)
    dummy_P = np.zeros(P.shape)
    ret_t = T
    ret_X = numpy.array(y)
    ret_D = dummy_D
    ret_P = dummy_P
    return (ret_t, ret_X, ret_D, ret_P)




def solout_fun(property_checker, property_violated_flag):
    def solout(t, Y):
        if property_checker(t, Y):
            property_violated_flag[0] = True
            print t, Y
        return 0
    return solout
