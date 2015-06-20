import numpy as np

# Must satisfy the signature
# [t,X,D,P] = sim_function(T,X0,D0,P0,I0);


class SIM(object):
    def __init__(self, plt, pvt_init_data):
        toy_id = pvt_init_data
        if toy_id == 1:
            toy = toy1
        elif toy_id == 2:
            toy = toy2
        elif toy_id == 3:
            toy = toy3
        else:
            raise Exception('unknown toy id')

        def compute_output(x, u):
            #print x
            x9 = x[0]
            A, B = toy(x9)
            #xout = ignore
            # no change
            x[0] = x9
            # assign respective values
            x[1] = A
            x[2] = B
            # exists solely due to lack of mechanisms for checking
            # controller properties. So send the state to the plant
            # and then check!
            x[3] = u[0]
            #print u
            return x

        self.compute_output = compute_output

    def sim(self, TT, X0, D, P, U, I, property_checker, property_violated_flag):

        # ignore time, its a discrete computation.
        #Ti = TT[0]
        Tf = TT[1]

        X_ = self.compute_output(X0, U)

        if property_checker is not None:
            if property_checker(Tf, X_):
                property_violated_flag[0] = True

        dummy_D = np.zeros(D.shape)
        dummy_P = np.zeros(P.shape)
        ret_t = Tf
        ret_X = X_
        ret_D = dummy_D
        ret_P = dummy_P

        #PLT.plot(np.array(Tf), X_)
        #print X_

        return (ret_t, ret_X, ret_D, ret_P)


def toy1(x):
    x_sq = x**2
    A = x_sq - 10.0
    B = x_sq
    return A, B


def toy2(x):
    x_sq = x**2
    A = x_sq * x
    B = x_sq
    return A, B


def toy3(x):
    x_sq = x**2
    A = x_sq * np.sin(x)
    B = x_sq
    return A, B
