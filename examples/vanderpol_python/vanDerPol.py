#!/usr/bin/python
# -*- coding: utf-8 -*-
# Must satisfy the signature
# [t,X,D,P] = sim_function(T,X0,D0,P0,I0);

import numpy as np
from scipy.integrate import ode


#import matplotlib.pyplot as plt


class SIM(object):

    def __init__(self, plt, plant_pvt_init_data):
        pass

    def sim(self, TT, XX, D, P, U, I, property_checker, property_violated_flag):

        # local prop vio flag

        pvf_local = [False]

        # print TT[0]
        # print XX

        plot_data = [np.empty(1, dtype=float), np.empty((0, 2), dtype=float)]

        # atol = 1e-10

        rtol = 1e-6
        if property_checker is not None:
            max_step = 1e-2
        else:
            max_step = 0.0
        nsteps = 1000

        # tt,YY,dummy_D,dummy_P
        # The orer of these calls is strict... do not change
        # (1):set_integrator -> (2):set_solout -> (3):set_initial_value

        solver = ode(dyn).set_integrator('dopri5', rtol=rtol, max_step=max_step,
                                         nsteps=nsteps)  # (1)
        if property_checker:
            violating_state = [()]
            solver.set_solout(solout_fun(property_checker, pvf_local,
                              violating_state, plot_data))  # (2)
        solver.set_initial_value(XX, 0.0)  # (3)

        Ti = TT[0]
        Tf = TT[1]
        T = Tf - Ti

        # print '='*40, 'result', '='*40
        # print T

        Y = solver.integrate(T)
        if pvf_local[0]:

            # TODO: changing t will mess up 'n' calculaitons in the
            # abstraction? Not changing will cause issues? Figure a way out!
            # t = violating_state[0][0]
            # print 'violating_state:', violating_state[0]
            # print 'setting Y', violating_state[0]

            Y = violating_state[0][1]
        else:
            if property_checker is not None:
                if property_checker(Tf, Y):
                    pvf_local[0] = True

        # print Y
        # print '='*80

        ret_t = Tf
        ret_X = Y
        ret_D = D
        ret_P = P
        if pvf_local[0]:
            property_violated_flag[0] = True

        # print plot_data[1]
        #plt.plot(plot_data[1][:,0], plot_data[1][:,1])
        # print 'sim:',ret_X, pvf_local[0]

        return (ret_t, ret_X, ret_D, ret_P)


def dyn(t, X):
    x1 = X[0]
    x2 = X[1]
    y1 = x2
    y2 = 5.0 * (1 - x1 ** 2) * x2 - x1
    return np.array([y1, y2])


def solout_fun(
        property_checker,
        pvf_local,
        violating_state,
        plot_data,
        ):

    def solout(t, Y):

        plot_data[0] = np.concatenate((plot_data[0], np.array([t])))
        plot_data[1] = np.concatenate((plot_data[1], np.array([Y])))

        # print Y
        # print t, Y

        if property_checker(t, Y):
            pvf_local[0] = True
            violating_state[0] = (np.copy(t), np.copy(Y))

            # print 'violation found:', violating_state[0]

        return 0

    return solout


def sim_unfinished_everystep(T, XX, D, P, U, I):
    sol = []

    # atol = 1e-10

    rtol = 1e-6

    # set rtol and force a maximum of 1 step per call...

    solver = ode(dyn).set_integrator('dopri5', rtol=rtol, nsteps=1)
    solver.set_initial_value(XX, 0.0)

    while solver.t < T:
        solver.integrate(T, step=True)
        sol.append([solver.t, solver.y])

    dummy_D = np.zeros(D.shape)
    dummy_P = np.zeros(P.shape)
    ret_t = T
    ret_X = Y
    ret_D = dummy_D
    ret_P = dummy_P
    return (ret_t, ret_X, ret_D, ret_P)


# def dyn(t, X):
#    Y(1) = X(2);
#    Y(2) = 5 * (1 - X(1)^2) * X(2) - X(1);
#    return Y

# import numpy as np
# from scipy.integrate import ode
# import matplotlib.pyplot as plt
# import warnings
#
#
# def logistic(t, y, r):
#     return r * y * (1.0 - y)
#
# r = .01
# t0 = 0
# y0 = 1e-5
# t1 = 5000.0
#
##backend = 'vode'
# backend = 'dopri5'
##backend = 'dop853'
#
# solver = ode(logistic).set_integrator(dopri15, nsteps=1)
#
# solver.set_initial_value(y0, t0).set_f_params(r)
## suppress Fortran-printed warning
# solver._integrator.iwork[2] = -1
#
# sol = []
# warnings.filterwarnings("ignore", category=UserWarning)
# while solver.t < t1:
#     solver.integrate(t1, step=True)
#     sol.append([solver.t, solver.y])
# warnings.resetwarnings()
# sol = np.array(sol)
#
# plt.plot(sol[:,0], sol[:,1], 'b.-')
# plt.show()

# 'dopri5'
#
# This is an explicit runge-kutta method of order (4)5 due to Dormand & Prince
# (with stepsize control and dense output).  Authors:
# E. Hairer and G. Wanner Universite de Geneve, Dept. de Mathematiques CH-1211
# Geneve 24, Switzerland e-mail: ernst.hairer@math.unige.ch,
# gerhard.wanner@math.unige.ch This code is described in [HNW93].
# This integrator accepts the following parameters in set_integrator() method
# of the ode class: atol : float or sequence absolute tolerance for solution
# rtol : float or sequence relative tolerance for solution
# nsteps : int Maximum number of (internally defined) steps allowed during one
#           call to the solver.
# first_step : float
# max_step : float
# safety : float Safety factor on new step selection (default 0.9)
# ifactor : float
# dfactor : float Maximum factor to increase/decrease step size by in one step
# beta : float Beta parameter for stabilised step size control.
# verbosity : int Switch for printing messages (< 0 for no messages).
