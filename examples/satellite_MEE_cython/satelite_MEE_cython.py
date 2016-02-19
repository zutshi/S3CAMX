#!/usr/bin/env python

#TODO: UNTESTED

import sat
import matplotlib.pyplot as plt


class SIM(object):

    def __init__(self, plt, pvt_init_data):
        sat.init()
        self.plt = plt
        self.dense_traces = 0

    def __del__(self):
        sat.terminate()

    def sim(self, TT, X0, D, P, U, I, property_checker, property_violated_flag):
        (t_, X_, D_, P_, pvf) = sat.sim(TT[0], TT[1], X0,
                                        D=0, P=0, U=0, I=0, pc=0,
                                        dense_traces=self.dense_traces)
        if pvf == 1:
            property_violated_flag[0] = 1
        return (t_, X_, D_, P_)


def plot3(a, b, c, mark="o", col="r"):
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.gcf()
    ax = Axes3D(fig)
    ax.scatter(a, b, c, marker=mark, color=col)


# X = np.array([2689.06, 2726.88, 6049.935, -6.53545, -1.16479, 3.40109])
# D = 0
# delta_t = 50
# t = 0
# T = delta_t

# D=D; P=0; U=0; I=0; pc=0

# XX = []
# tt = []

# MAX_T = 8000

# for i in range(0, MAX_T, delta_t):
#     (t_, X_, D_, P_, pvf) = sat.sim(t+i, T+i, X, D, P, U, I, pc)
#     XX.append(X_)
#     tt.append(t_)
#     X = X_[-1, :]

# aXX = np.vstack(XX)
# att = np.hstack(tt)

#print aXX
#print att

#plt.figure()
#plot3(aXX[:, 0], aXX[:, 1], aXX[:, 2])
#plt.show()
