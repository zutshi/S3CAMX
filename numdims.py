'''
numdims.py
----------
Defines the Number of dimensions structure used accross the project.
'''

# TODO: consider using a named tuple instead?

class NumDims:

    def __init__(
        self,
        si=None,
        sf=None,
        s=None,
        u=None,
        x=None,
        pi=None,
        ci=None,
        d=None,
        pvt=None,
        ):

        self.si = si  # conrtoller states
        self.sf = sf  # conrtoller states
        self.s = s  # conrtoller states
        self.u = u  # controller outputs
        self.x = x  # plant states
        self.pi = pi  # plant disturbance
        self.ci = ci  # control disturbance
        self.d = d  # discrete
        self.pvt = pvt  # pvt
        return
