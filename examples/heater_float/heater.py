# Must satisfy the signature
# [t,X,D,P] = sim_function(T,X0,D0,P0,I0);

import numpy as np
from scipy.integrate import ode

#import matplotlib.pyplot as plt


class SIM(object):

    def __init__(self, plt, pvt_init_data):
        pass

    def sim(self, TT, X0, D, P, U, I, property_checker, property_violated_flag):
        # atol = 1e-10
        rtol = 1e-5

        num_dim_x = len(X0)
        plot_data = [np.empty(0, dtype=float), np.empty((0, num_dim_x), dtype=float)]

        # tt,YY,dummy_D,dummy_P
        solver = ode(dyn).set_integrator('dopri5', rtol=rtol)

        Ti = TT[0]
        Tf = TT[1]
        T = Tf - Ti

        if property_checker:
            violating_state = [()]
            #solver.set_solout(solout_fun(property_checker, violating_state, plot_data))  # (2)

        solver.set_initial_value(X0, t=0.0)
        solver.set_f_params(U)
        X_ = solver.integrate(T)
        # Y = C*x + D*u

        if property_checker is not None:
            if property_checker(Tf, X_):
                property_violated_flag[0] = True

        dummy_D = np.zeros(D.shape)
        dummy_P = np.zeros(P.shape)
        ret_t = Tf
        ret_X = X_
        # ret_Y = Y
        ret_D = dummy_D
        ret_P = dummy_P

        #plt.plot(plot_data[0] + Ti, plot_data[1][:, 0])
        ##plt.plot(plot_data[1][:, 0], plot_data[1][:, 1])
        ##plt.plot(plot_data[0] + Ti, np.tile(U, plot_data[0].shape))

        return (ret_t, ret_X, ret_D, ret_P)


def dyn(t, x, u):
    if u == 1:
        x = 0.1*(100.0 - x)   # 100
    elif u == 2:
        x = 0.1*(70.1 - x)  # 70
    elif u == 0:
        x = 0.50*(20.0 - x)    # 20
    else:
        print 'error: u =', u
        raise NotImplementedError
    return x


def solout_fun(property_checker, violating_state, plot_data):

    def solout(t, Y):

        plot_data[0] = np.concatenate((plot_data[0], np.array([t])))
        plot_data[1] = np.concatenate((plot_data[1], np.array([Y])))

        # print Y
        # print t, Y

#        if property_checker(t, Y):
#            pvf_local[0] = True
#            violating_state[0] = (np.copy(t), np.copy(Y))
#
#            # print 'violation found:', violating_state[0]

        return 0

    return solout
