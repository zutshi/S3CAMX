#!/usr/bin/env python

import sat
import numpy as np
import matplotlib.pyplot as plt

def plot3(a,b,c,mark="o",col="r"):
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.gcf()
    ax = Axes3D(fig)
    ax.scatter(a, b, c,marker=mark,color=col)

#Initialize the application.
#You do not need to do this more than one time.

sat.init()

#Invoke the entry-point functions.
#You can call entry-point functions multiple times.


X = np.array([2689.06, 2726.88, 6049.935, -6.53545, -1.16479, 3.40109])
D = 0
delta_t = 50
t = 0
T = delta_t

D=D; P=0; U=0; I=0; pc=0

XX = []
tt = []

MAX_T = 8000
dense_traces = 1
for i in range(0, MAX_T, delta_t):
    (t_, X_, D_, P_, pvf) = sat.sim(t+i, T+i, X, D, P, U, I, pc, dense_traces)
    XX.append(X_)
    tt.append(t_)
    X = X_[-1, :]

aXX = np.vstack(XX)
att = np.hstack(tt)

#print aXX
#print att

#plt.figure()
#plot3(aXX[:, 0], aXX[:, 1], aXX[:, 2])
#plt.show()

#Terminate the application.
#You do not need to do this more than one time.
sat.terminate()


