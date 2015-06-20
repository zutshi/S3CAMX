# Must satisfy the signature
# [t,X,D,P] = sim_function(T,X0,D0,P0,I0);

import numpy as np

MODE_0 = 0
MODE_1 = 1


# Simple Plant has no dynamics...
def sim(TT, XX, D, P, U, I, property_checker, property_violated_flag):

    t,T = TT
    x = XX
    if D == MODE_0:
        y = x**2 - 10 - U
    elif D == MODE_1:
        y = x**2
    else:
        raise Exception('unknown discrete mode: {}'.format(D))

    if property_checker:
        property_checker()
        property_violated_flag[0]

    dummy_P = np.zeros(P.shape)
    ret_t = T
    ret_X = np.array(y)
    ret_D = D
    ret_P = dummy_P
    return (ret_t, ret_X, ret_D, ret_P)
