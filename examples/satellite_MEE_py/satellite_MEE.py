# Must satisfy the signature
# [t,X,D,P] = sim_function(T,X0,D0,P0,I0);

import numpy as np
from numpy import linalg
from scipy.integrate import ode

#import matplotlib.pyplot as plt


class SIM(object):

    def __init__(self, plt, pvt_init_data):
        self.mu = 398603.2 # earth gravitational constant (km**3/sec**2)
        self.J2 = 0.00108263
        self.Re = 6378.165 # earth equatorial radius (kilometers)
        self.omega = 7.292115486e-5#% earth inertial rotation rate (radians/second)
        self.Cd = 2.0e-8 # coef. of atmospheric drag
        self.plt = plt

    def sim(self, TT, X0, D, P, U, I, property_checker, property_violated_flag):
        #atol = 1e-12
        rtol = 1e-6

        num_dim_x = len(X0)
        plot_data = [np.empty(0, dtype=float), np.empty((0, num_dim_x), dtype=float)]

        # tt,YY,dummy_D,dummy_P
        solver = ode(self.ode_mee).set_integrator('dopri5', rtol=rtol)

        Ti = TT[0]
        Tf = TT[1]
        T = Tf - Ti

        if property_checker:
            violating_state = [()]
            solver.set_solout(solout_fun(property_checker, violating_state, plot_data))  # (2)

        ###################
        ###################
        t0 = 0.0
        reci0 = X0[0:3]
        veci0 = X0[3:6]
        #coordinate transformation from Cartesian state to MEE state
        mee0 = self.eci2mee(reci0, veci0)

        solver.set_initial_value(mee0, t=t0)
        solver.set_f_params(U)
        mee = solver.integrate(T)

        #mee = mee
        (reci, veci) = self.mee2eci(mee)
        #print '='*20
        #print reci
        #print veci
        #print '='*20
        X_ = np.concatenate((reci, veci))
        #print X_
        #t_arr = tt[-1]
        ###################
        ###################

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

        #self.plt.plot(plot_data[0] + Ti, plot_data[1][:, 0])
        #self.plt.plot(plot_data[1][:, 0], plot_data[1][:, 1])
        ##plt.plot(plot_data[0] + Ti, np.tile(U, plot_data[0].shape))

        return (ret_t, ret_X, ret_D, ret_P)

    def ode_mee(self, t, x, u):
        mu = self.mu
        J2 = self.J2
        Re = self.Re

        # compute eci state vector
        (reci, veci) = self.mee2eci(x)
        #compute disturbing acceleration
        accg = self.acc_gravity(reci, veci)
        accd = self.acc_drag(reci, veci)
        ad = accg + accd

        eta = 1+x[1] * np.cos(x[5])+x[2] * np.sin(x[5])
        ka = np.sqrt(x[3] ** 2+x[4] ** 2)
        s_2 = 1 + ka ** 2
        A = np.array([
                [0, 2 * x[0]/eta * np.sqrt(x[0]/mu), 0],
                [np.sqrt(x[0]/mu) * np.sin(x[5]), np.sqrt(x[0]/mu)/eta * ((eta+1) * np.cos(x[5])+x[1]), -np.sqrt(x[0]/mu) * x[2]/eta * (x[3] * np.sin(x[5])-x[4] * np.cos(x[5]))],
                [-np.sqrt(x[0]/mu) * np.cos(x[5]), np.sqrt(x[0]/mu)/eta * ((eta+1) * np.sin(x[5])+x[2]), np.sqrt(x[0]/mu) * x[1]/eta * (x[3] * np.sin(x[5])-x[4] * np.cos(x[5]))],
                [0, 0, np.sqrt(x[0]/mu) * s_2 * np.cos(x[5])/2/eta],
                [0, 0, np.sqrt(x[0]/mu) * s_2 * np.sin(x[5])/2/eta],
                [0, 0, np.sqrt(x[0]/mu)/eta * (x[3] * np.sin(x[5])-x[4] * np.cos(x[5]))]
                ])
        b = np.array([0, 0, 0, 0, 0, np.sqrt(mu * x[0]) * (eta/x[0])**2])
        dx = np.dot(A, ad) + b
        return dx

    def acc_drag(self, reci, veci):
        # atmospheric drag
        omega = self.omega
        Cd = self.Cd
        # velocity vector of atmosphere relative to spacecraft
        vs = np.array([
                veci[0] + omega * reci[1],
                veci[1] - omega * reci[0],
                veci[2]
            ])
        vrel = linalg.norm(vs)
        # acceleration
        accd = (-Cd*vs/vrel).T
        return accd

    def acc_gravity(self, reci, veci):
        #compute acceleration caused by J2
        mu = self.mu
        J2 = self.J2
        Re = self.Re

        radius = linalg.norm(reci)
        # construct unit vectors for local horizontal frame
        zhat = -reci / radius
        zdotr = zhat[2]

        xhat = -zdotr * zhat

        xhat[2] += 1.0

        xnorm = linalg.norm(xhat)
        xhat = xhat / xnorm

        #compute gravitational acceleration in a local horizontal reference frame
        # compute np.sin and np.conp.sine of latitude
        np.sinphi = reci[2] / radius
        np.cosphi = np.sqrt(1.0 - np.sinphi**2)
        P2 = 1/2*(3*np.sinphi**2-1)
        dP2 = 3*np.sinphi

        # construct acceleration local horizontal n r direction
        accg_n = -mu/(radius**4)*np.cosphi*(Re**2)*dP2*J2
        accg_r = -mu/(radius**4)*3*(Re**2)*P2*J2

        # accelerations in the eci frame
        ageci = accg_n * xhat + accg_r * zhat

        # compute radial frame unit vectors

        (ex, ey, ez) = self.eci2rdl(reci, veci)

        # transform eci gravity vector to mee gravity components
        accg = np.array([np.dot(ageci, ex), np.dot(ageci, ey), np.dot(ageci, ez)]).T
        return accg

    def atan3(self, a, b):
        ###########################################
        # four quadrant inverse tangent
        # input
        #  a = np.sine of angle
        #  b = np.conp.sine of angle
        # output
        #  y = angle (radians; 0 =< c <= 2 * pi)
        # Orbital Mechanics with MATLAB
        ###########################################

        epsilon = 0.0000000001
        pidiv2 = 0.5 * np.pi

        if abs(a) < epsilon:
            y = (1 - np.sign(b)) * pidiv2
        else:
            c = (2 - np.sign(a)) * pidiv2
            if abs(b) < epsilon:
                y = c
            else:
                y = c + np.sign(a) * np.sign(b) * (np.abs(np.arctan(a / b)) - pidiv2)
        return y

    def eci2mee(self, reci, veci):
        mu = self.mu
        # convert eci state vector to
        # modified equinoctial elements
        # input
        #  mu   = gravitational constant (km**3/sec**2)
        #  reci = eci position vector (kilometers)
        #  veci = eci velocity vector (kilometers/second)
        # output
        #  mee(1) = semiparameter (kilometers)
        #  mee(2) = f equinoctial element
        #  mee(3) = g equinoctial element
        #  mee(4) = h equinoctial element
        #  mee(5) = k equinoctial element
        #  mee(6) = true longitude (radians)
        # Orbital Mechanics with MATLAB
        ###############################

        radius = linalg.norm(reci)
        hv = np.cross(reci, veci)
        hmag = linalg.norm(hv)
        pmee = hmag**2 / mu
        rdotv = np.dot(reci, veci)
        rzerod = rdotv / radius
        eccen = np.cross(veci, hv)
        uhat = reci / radius
        vhat = (radius * veci - rzerod * reci) / hmag
        eccen = eccen / mu - uhat

        # unit angular momentum vector
        hhat = hv / linalg.norm(hv)

        # compute kmee and hmee
        denom = 1.0 + hhat[2]
        kmee = hhat[0] / denom
        hmee = -hhat[1] / denom

        # construct unit vectors in the equinoctial frame
        fhat = np.array([1.0 - kmee**2 + hmee**2, 2.0 * kmee * hmee, -2.0 * kmee])
        ghat = np.array([fhat[1], 1.0 + kmee**2 - hmee**2, 2.0 * hmee])
        ssqrd = 1.0 + kmee**2 + hmee**2

        # linalg.normalize
        fhat = fhat / ssqrd
        ghat = ghat / ssqrd

        # compute fmee and gmee
        fmee = np.dot(eccen, fhat)
        gmee = np.dot(eccen, ghat)

        # compute true longitude
        np.cosl = uhat[0] + vhat[1]
        np.sinl = uhat[1] - vhat[0]
        lmee = self.atan3(np.sinl, np.cosl)

        # load modified equinoctial orbital elements array
        mee = np.array([pmee, fmee, gmee, hmee, kmee, lmee])
        return mee

    def eci2rdl(self, reci, veci):
        # radial frame unit vectors: ex ey ez
        #  reci = eci position vector (kilometers)
        #  veci = eci velocity vector (kilometers/second)
        ex = reci / linalg.norm(reci)
        a = np.cross(reci, veci)
        ez = a / linalg.norm(a)
        ey = np.cross(ez, ex)
        return (ex, ey, ez)

    def mee2eci(self, mee):
        mu = self.mu
        #transformation from mee to Cartitien r,v
        eta = 1+mee[1]*np.cos(mee[5])+mee[2]*np.sin(mee[5])
        r = mee[0]/eta
        alpha = mee[3]**2-mee[4]**2
        ka = np.sqrt(mee[3]**2+mee[4]**2)
        s_2 = 1+ka**2
        reci = np.array([
                r/s_2*(np.cos(mee[5])+alpha*np.cos(mee[5])+2*mee[3]*mee[4]*np.sin(mee[5])),
                r/s_2*(np.sin(mee[5])-alpha*np.sin(mee[5])+2*mee[3]*mee[4]*np.cos(mee[5])),
                2*r/s_2*(mee[3]*np.sin(mee[5])-mee[4]*np.cos(mee[5]))
                ]).T
        veci = np.array([
                -1/s_2*np.sqrt(mu/mee[0])*(np.sin(mee[5])+alpha*np.sin(mee[5])-2*mee[3]*mee[4]*np.cos(mee[5])+mee[2]-2*mee[1]*mee[3]*mee[4]+alpha*mee[2]),
                -1/s_2*np.sqrt(mu/mee[0])*(-np.cos(mee[5])+alpha*np.cos(mee[5])+2*mee[3]*mee[4]*np.sin(mee[5])-mee[1]+2*mee[2]*mee[3]*mee[4]+alpha*mee[1]),
                2/s_2*np.sqrt(mu/mee[0])*(mee[3]*np.cos(mee[5])+mee[4]*np.sin(mee[5])+mee[1]*mee[3]+mee[2]*mee[4])
                ]).T
        return (reci, veci)


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
