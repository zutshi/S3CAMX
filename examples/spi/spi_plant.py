
# Must satisfy the signature
# [t,X,D,P] = sim_function(T,X0,D0,P0,I0);

import numpy as np
from scipy.integrate import ode

import matplotlib.pyplot as PLT


class SIM(object):
    def __init__(self, plt, pvt_init_data):
        pass

    def sim(self, TT, X0, D, P, U, I, property_checker, property_violated_flag):
        #print I
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
            solver.set_solout(solout_fun(property_checker, violating_state, plot_data))  # (2)

        solver.set_initial_value(X0, t=0.0)
        solver.set_f_params(U)
        X_ = solver.integrate(T)

        if property_checker is not None:
            if property_checker(Tf, X_):
                property_violated_flag[0] = True

        dummy_D = np.zeros(D.shape)
        dummy_P = np.zeros(P.shape)
        ret_t = Tf
        ret_X = X_
        ret_D = dummy_D
        ret_P = dummy_P

        # TODO: plotting needs to be fixed
        PLT.plot(plot_data[0] + Ti, plot_data[1][:, 0])
        #PLT.plot(plot_data[0] + Ti, plot_data[1][:, 1])
        #PLT.plot(plot_data[1][:, 0], plot_data[1][:, 1])
        ##PLT.plot(plot_data[0] + Ti, np.tile(U, plot_data[0].shape))

        return (ret_t, ret_X, ret_D, ret_P)


def sign(c):
    if c > 0:
        return 1
    elif c < 0:
        return -1
    else:
        return 0


# State Space Modeling Template
# dx/dt = Ax + Bu
# y = Cx + Du
def dyn(t, X, u):
    x2 = u
    X_ = np.array([x2])
    #u = np.matrix([u[0], 0.0]).T
    #x = np.matrix(x).T
    #X_ = A*x + B*u
    #return np.array(X_.T)
    return X_


def solout_fun(property_checker, violating_state, plot_data):

    def solout(t, Y):
        plot_data[0] = np.concatenate((plot_data[0], np.array([t])))
        plot_data[1] = np.concatenate((plot_data[1], np.array([Y])))
        return 0

    return solout
