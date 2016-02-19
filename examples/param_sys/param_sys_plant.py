
# Must satisfy the signature
# [t,X,D,P] = sim_function(T,X0,D0,P0,I0);

import numpy as np
from scipy.integrate import ode
import scipy.linalg as lg

import matplotlib.pyplot as PLT


class SIM(object):
    def __init__(self, plt, pvt_init_data):

        self.sims = [self.sim1, self.sim2]

    def sim1(self, TT, X0, D, P, U, I, property_checker, property_violated_flag):
        return self.sim_(TT, X0, D, P, U, I, property_checker, property_violated_flag, dyn1)

    def sim2(self, TT, X0, D, P, U, I, property_checker, property_violated_flag):
        return self.sim_(TT, X0, D, P, U, I, property_checker, property_violated_flag, dyn2)

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
        #PLT.plot(plot_data[0] + Ti, plot_data[1][:, 0])
        #PLT.plot(plot_data[0] + Ti, plot_data[1][:, 1])
        #PLT.plot(plot_data[1][:, 0], plot_data[1][:, 1])
        ##PLT.plot(plot_data[0] + Ti, np.tile(U, plot_data[0].shape))

        return (ret_t, ret_X, ret_D, ret_P)

    def sim_(self, TT, X0, D, P, U, I, property_checker, property_violated_flag, dyn_):
        # atol = 1e-10
        rtol = 1e-5

        num_dim_x = len(X0)
        plot_data = [np.empty(0, dtype=float), np.empty((0, num_dim_x), dtype=float)]

        # tt,YY,dummy_D,dummy_P
        solver = ode(dyn_).set_integrator('dopri5', rtol=rtol)

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
        #PLT.plot(plot_data[0] + Ti, plot_data[1][:, 0])
        #PLT.plot(plot_data[0] + Ti, plot_data[1][:, 1])
        #PLT.plot(plot_data[1][:, 0], plot_data[1][:, 1])
        ##PLT.plot(plot_data[0] + Ti, np.tile(U, plot_data[0].shape))

        return (ret_t, ret_X, ret_D, ret_P)


A1 = np.matrix([[1, -10], [1, 1]])
A2 = np.matrix([[1, 1], [1, 1]])*0.3
AA = lg.block_diag(A1, A2)


def dyn(t, x, u):
    #u = np.matrix([u[0], 0.0]).T
    x = np.matrix(x).T
    X_ = AA*x
    return np.array(X_.T)


# State Space Modeling Template
# dx/dt = Ax + Bu
# y = Cx + Du
def dyn1(t, x, u):
    #u = np.matrix([u[0], 0.0]).T
    x = np.matrix(x).T
    X_ = A1*x
    return np.array(X_.T)


def dyn2(t, x, u):
    #u = np.matrix([u[0], 0.0]).T
    x = np.matrix(x).T
    X_ = A2*x
    return np.array(X_.T)


def solout_fun(property_checker, violating_state, plot_data):

    def solout(t, Y):
        plot_data[0] = np.concatenate((plot_data[0], np.array([t])))
        plot_data[1] = np.concatenate((plot_data[1], np.array([Y])))
        return 0

    return solout
