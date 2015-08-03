
# Must satisfy the signature
# [t,X,D,P] = sim_function(T,X0,D0,P0,I0);

import numpy as np
from scipy.integrate import ode
#import matplotlib.pyplot as PLT

import heat as H


class SIM(object):

    def __init__(self, plt, plant_pvt_init_data):
        benchmark_id = plant_pvt_init_data
        #mat_dict = H.get_params(benchmark_id)
        mat_dict = H.get_params(benchmark_id)

        Amat = mat_dict['Amat']
        cvec = mat_dict['cvec']
        bvec = mat_dict['bvec']
        rooms = mat_dict['rooms']
        u = mat_dict['u']

        #get = mat_dict['get']
        #dif = mat_dict['dif']
        #h = mat_dict['h']
        #off = mat_dict['off']
        #on = mat_dict['on']

        #xinit = mat_dict['xinit']
        #lower = mat_dict['lower']

        # conversions
        #Amat = Amat)
        cvec = cvec[:, 0]
        bvec = bvec[:, 0]
        u = u[0][0]
        rooms = rooms[0][0]

        # State Space Modeling Template
        # dx/dt = Ax + Bu
        # y = Cx + Du
        def dyn(t, x, hvec):
            #X = np.matrix(x).T
            X = x
            # swap i and j to get desired order
            #print
            #print np.matrix([[X[i] - X[j] for j in range(rooms)] for i in range(rooms)])
            #X = ['x0', 'x1', 'x2']
            #xj_xi_mat = [[X[j] + '-' + X[i] for j in range(rooms)] for i in range(rooms)]
            #print xj_xi_mat
            #print Amat
            #exit()
            xj_xi_mat = np.array([[X[j] - X[i] for j in range(rooms)] for i in range(rooms)])
            #print 'Amat', Amat
            #print 'xjxi', xj_xi_mat
            #print 'cvec', cvec
            #print 'hvec', hvec
            #print 'bvec', bvec
            #print 'u', u
            X_ = cvec * hvec + bvec * (u - x) + np.sum(Amat * xj_xi_mat, axis=1)
#            X2_ = (np.dot(Amat, xj_xi_mat)).sum(axis=1, keepdims=True)
#            print
#            print 'xj_xi_mat', xj_xi_mat
#            print 'x', x
#            print 'X1_', X1_
#            print 'Amat', Amat
#            print 'X2_', Amat * xj_xi_mat
#            print 'X2_sum', X2_
#            print 'X_', X_
#            exit()
            return np.array(X_.T)

        self.dyn = dyn
        #self.plt = PLT#plt

    def sim(self, TT, X0, D, P, U, I, property_checker, property_violated_flag):
        # atol = 1e-10
        rtol = 1e-5

        num_dim_x = len(X0)
        plot_data = [np.empty(0, dtype=float), np.empty((0, num_dim_x), dtype=float)]

        # tt,YY,dummy_D,dummy_P
        solver = ode(self.dyn).set_integrator('dopri5', rtol=rtol)

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

        #self.plt.plot(plot_data[0] + Ti, plot_data[1][:, 0])
        #plt.plot(plot_data[0] + Ti, plot_data[1][:, 1])
        #plt.plot(plot_data[1][:, 0], plot_data[1][:, 1])
        ##plt.plot(plot_data[0] + Ti, np.tile(U, plot_data[0].shape))

        return (ret_t, ret_X, ret_D, ret_P)


def solout_fun(property_checker, violating_state, plot_data):

    def solout(t, Y):
        plot_data[0] = np.concatenate((plot_data[0], np.array([t])))
        plot_data[1] = np.concatenate((plot_data[1], np.array([Y])))
        return 0

    return solout
