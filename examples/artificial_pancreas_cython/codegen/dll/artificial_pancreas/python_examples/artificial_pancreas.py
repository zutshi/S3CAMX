#!/usr/bin/env python

import ap
import numpy as np
import matplotlib.pyplot as plt

#ap.hello()

#Initialize the application.
#You do not need to do this more than one time.

#TODO: not done yet. Figuring out the artificial_pancreas() signature!
ap.init()

#Invoke the entry-point functions.
#You can call entry-point functions multiple times.
X = np.array([100, 90, 0])
D = np.array([720, 0, 40] + [0]*21)

delta_t = 10

t=0; T=delta_t; X=X; D=D; P=0; U=0; I=10; pc=0
#(tt, YY, D_, P_, pvf) =

XX = []
tt = []

for i in range(0, 720, delta_t):
    (t_, X_, D_, P_, pvf) = ap.sim(t+i, T+i, X, D, P, U, I, pc)
    D = D_
    X = X_
    XX += [X_]
    tt.append(t_)

aXX = np.array(XX)
att = np.array(tt)

#print aXX
#print att

plt.figure()
plt.plot(att, aXX[:, 0])
plt.show()


#Terminate the application.
#You do not need to do this more than one time.
ap.terminate()
