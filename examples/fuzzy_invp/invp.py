import numpy as np
from scipy.integrate import ode

import matplotlib.pyplot as plt


def sim(TT, X0, D, P, U, I, property_checker, property_violated_flag):
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

    #plt.plot(plot_data[0] + Ti, plot_data[1][:, 1])
    #plt.plot(plot_data[0] + Ti, plot_data[1][:, 2])
    ##plt.plot(plot_data[1][:, 0], plot_data[1][:, 1])

    return (ret_t, ret_X, ret_D, ret_P)


#def dyn(double t, const double *y, double u, double *ydot):
def dyn(t, x, u):

    #/* This is where the derivative is defined:  xdot = f(t,x,u). */

    #/* Example:  xdot = A*x + b*u (time invariant system)

    # ydot[0] = -2*y[0] + -u;          | -2   0   0 |      | -1 |
    # ydot[1] = -3*y[1] + 2*u;       A=|  0  -3   0 |,   B=|  2 |
    # ydot[2] = -4*y[2] + u;           |  0   0  -4 |      |  1 |

    # */

    # /*******  INSERT YOUR DERIVATIVE DEFINITION HERE:  ********/

    # double e,edot;

    # /* Determine the system input u.  Because the system is continuous, the input
    #   is calculated within the deriv() function.  For discrete time systems, the
    #   input can be calculated and passed to deriv() via the u paramater. */

    # e = -x[0]; edot = -x[1];

    # /* Inverted pendulum dynamics. */
    #
    # xdot = np.zeros(x.size)

    xdot_0 = x[1]
    xdot_1 = (9.8*np.sin(x[0]) + np.cos(x[0])*(-x[2] - 0.25*(x[1]**2.0)*np.sin(x[0]))/1.5)\
        / (0.4*(4.0/3.0 - 1.0/3.0*(np.cos(x[0])**2.0)))
    xdot_2 = 100.0*u - 100.0*x[2]  # /* Actuator dynamics */
    # return xdot
    return np.array([xdot_0, xdot_1, xdot_2])


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
