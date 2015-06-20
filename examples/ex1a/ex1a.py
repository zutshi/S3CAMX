#!/usr/bin/python
# -*- coding: utf-8 -*-
# Must satisfy the signature
# [t,X,D,P] = sim_function(T,X0,D0,P0,I0);

import numpy as np
from scipy.integrate import ode

import matplotlib.pyplot as plt


def sim(TT, XX, D, P, U, I, property_checker, property_violated_flag):
    # local prop vio flag

    plot_data = [np.empty(0, dtype=float), np.empty((0, 1), dtype=float)]

    # atol = 1e-10

    rtol = 1e-4
    max_step = 0.0
    nsteps = 10000

    # tt,YY,dummy_D,dummy_P
    # The orer of these calls is strict... do not change
    # (1):set_integrator -> (2):set_solout -> (3):set_initial_value

    solver = ode(dyn).set_integrator('dopri5', rtol=rtol, max_step=max_step,
                                     nsteps=nsteps)  # (1)
    if property_checker:
        violating_state = [()]
        solver.set_solout(solout_fun(property_checker, violating_state,
                                     plot_data))  # (2)
    solver.set_initial_value(XX, 0.0)  # (3)

    Ti = TT[0]
    Tf = TT[1]
    T = Tf - Ti

    # switch mode at t = \tau
    if XX[0] >= 2.80 and XX[0] <= 2.801:
        D = 1

    solver.set_f_params(D)
    Y = solver.integrate(T)

    if property_checker is not None:
        if property_checker(Tf, Y):
            property_violated_flag[0] = True

    ret_t = Tf
    ret_X = Y
    ret_D = D
    ret_P = P

    #print 't', plot_data[0]
    #print 'Y', plot_data[1][:,0]
    plt.plot(plot_data[0] + Ti, plot_data[1][:, 0])

    return (ret_t, ret_X, ret_D, ret_P)


def dyn(t, X, D):
    a = 1
    b = -10
    x = X[0]
    if D == 0:
        x_dot = a
    else:
        x_dot = b
    return np.array([x_dot])


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
