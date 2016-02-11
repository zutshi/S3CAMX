#!/usr/bin/python
# -*- coding: utf-8 -*-
# Must satisfy the signature
# [t,X,D,P] = sim_function(T,X0,D0,P0,I0);

import numpy as np
cimport numpy as np

from scipy.integrate import ode
from scipy.integrate import odeint
from pyodeint import integrate_adaptive  # also: integrate_predefined

import copy_reg as cr
import types

cdef extern from "math.h":
    double pow(double, double)

DTYPE = np.int
# "ctypedef" assigns a corresponding compile-time type to DTYPE_t. For
# every type in the numpy module there's a corresponding compile-time
# type with a _t-suffix.
ctypedef np.double_t DTYPE_t

def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

cr.pickle(types.MethodType, _pickle_method)


class SIM(object):

    def __init__(self, plt, pvt_init_data):
        pass

    def sim(*args):
        #return sim_pyodeint(*args)
        #return sim_scipy_odeint(*args)
        return sim_scipy_integrate_ode(*args)


# uses pyodeint
def sim_pyodeint(self, TT, X0, D, P, U, I, property_checker, property_violated_flag):

    atol = 1e-12
    rtol = 1e-8

    num_dim_x = len(X0)
    plot_data = [np.empty(0, dtype=float), np.empty((0, num_dim_x), dtype=float)]


    Ti = TT[0]
    Tf = TT[1]
    T = Tf - Ti

    if property_checker:
        violating_state = [()]

    tout, X_, info = integrate_adaptive(dyn_pyodeint, None, X0, 0, T, 1e-2, atol, rtol, method='dopri5')

    X_ = X_[-1]

    if property_checker is not None:
        if property_checker(Tf, X_):
            property_violated_flag[0] = True

    dummy_D = np.zeros(D.shape)
    dummy_P = np.zeros(P.shape)
    ret_t = Tf
    ret_X = X_
    ret_D = dummy_D
    ret_P = dummy_P

    return (ret_t, ret_X, ret_D, ret_P)


# uses scipy.integrate.odeint
def sim_scipy_odeint(self, TT, X0, D, P, U, I, property_checker, property_violated_flag):

    rtol = 1e-6
    if property_checker is not None:
        max_step = 1e-2
    else:
        max_step = 0.0

    num_dim_x = len(X0)
    plot_data = [np.empty(0, dtype=float), np.empty((0, num_dim_x), dtype=float)]


    Ti = TT[0]
    Tf = TT[1]
    T = np.arange(0, Tf - Ti, 1e-2)

    if property_checker:
        violating_state = [()]
    X_ = odeint(dyn_scipy_odeint, X0, T, args=(U,), rtol=rtol, hmax=max_step)
    X_ = X_[-1]

    if property_checker is not None:
        if property_checker(Tf, X_):
            property_violated_flag[0] = True

    dummy_D = np.zeros(D.shape)
    dummy_P = np.zeros(P.shape)
    ret_t = Tf
    ret_X = X_
    ret_D = dummy_D
    ret_P = dummy_P

    return (ret_t, ret_X, ret_D, ret_P)

# uses scipy.integrate.ode
def sim_scipy_integrate_ode(self, TT, X0, D, P, U, I, property_checker, property_violated_flag):
    # atol = 1e-10
    rtol = 1e-6
    if property_checker is not None:
        max_step = 1e-2
    else:
        max_step = 0.0
    nsteps = 1000
    num_dim_x = len(X0)
    plot_data = [np.empty(0, dtype=float), np.empty((0, num_dim_x), dtype=float)]

    solver = ode(dyn_scipy_ode).set_integrator('dopri5', rtol=rtol, max_step=max_step)  # (1)

    Ti = TT[0]
    Tf = TT[1]
    T = Tf - Ti

    if property_checker:
        violating_state = [()]

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

    return (ret_t, ret_X, ret_D, ret_P)

def dyn_non_opt(t, X, u):
    x1 = X[0]
    x2 = X[1]
    y1 = x2
    y2 = 5.0 * (1 - x1 ** 2) * x2 - x1
    return np.array([y1, y2])


def dyn_scipy_ode(__, np.ndarray X, _):
    # Bad things happen when you modify the passed in X.
    # So, make a copy!
    X = X.copy()
    X[0], X[1] = (X[1], 5.0 * (1 - pow(X[0], 2)) * X[1] - X[0])
    return X

def dyn_scipy_odeint(np.ndarray X, _, __):
    # Bad things happen when you modify the passed in X.
    # So, make a copy!
    X = X.copy()
    X[0], X[1] = (X[1], 5.0 * (1 - pow(X[0], 2)) * X[1] - X[0])
    return X


def dyn_pyodeint(_, X, dydt):
    dydt[0] = X[1]
    dydt[1] = 5.0 * (1 - pow(X[0], 2)) * X[1] - X[0]
