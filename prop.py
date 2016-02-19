import utils as U


class Property(object):
    def __init__(self, T, init_cons_list, init_cons, final_cons, ci, pi,
                 initial_discrete_state, initial_controller_state, MAX_ITER,
                 num_segments):
        self.T = T
        self.init_cons_list = init_cons_list
        self.init_cons = init_cons
        self.final_cons = final_cons
        self.ci = ci
        self.pi = pi
        self.initial_discrete_state = initial_discrete_state
        self.initial_controller_state = initial_controller_state
        self.MAX_ITER = MAX_ITER
        self.num_segments = num_segments

        self.sanity_check = U.assert_no_Nones
        #print init_cons.to_numpy_array()
        #print final_cons.to_numpy_array()
        #print ci.to_numpy_array()

        return

    def __repr__(self):
        v = vars(self)
        return ','.join(map(str, v.items()))
