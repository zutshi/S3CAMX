#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


# TODO: all states flying around....split it into controller and plant state array!

class StateArray(object):

    # t: time
    # x: continous plant state [change to x]
    # d: discrete plant state
    # s: controller state
    # u: controller output
    # pi: plant disturbance
    # pvt: plant private state [plant simulator can associate pvt states?]
    # ci: controller disturbance

    def __init__(
            self,
            t,
            x,
            d,
            pvt,
            s=None,
            u=None,
            pi=None,
            ci=None):

        # self.sanity_chec()

        # ##!!##logger.debug('sanity_check() disabled!')

        # TODO: why have the time array? whats the use?
        # time array

        self.t = t

        # numpy arr

        self.cont_states = x

        # numpy arr

        self.discrete_states = d
        self.pvt_states = pvt
        self.controller_states = s
        self.controller_outputs = u
        self.plant_extraneous_inputs = pi
        self.controller_extraneous_inputs = ci

    @property
    def n(self):

        # number of states, find from the number of continous states
        # This is OK, as the sanity check has verified that all are equal

        return len(self.cont_states)

    def iterable(self):
        i = 0
        while i < self.n:
            yield State(  # self.controller_extraneous_inputs[i],
                          # self.plant_extraneous_inputs[i],
                          # self.controller_outputs[i]
                          # self.plant_extraneous_inputs[i],
                self.t[i],
                self.cont_states[i],
                self.discrete_states[i],
                self.pvt_states[i],
                self.controller_extraneous_inputs[i],
                self.controller_states[i],
                self.plant_extraneous_inputs[i],
                self.controller_outputs[i],
                )
            i += 1
        return

    def __getitem__(self, key):
        i = key

#        if isinstance(i, slice):
#            # Get the start, stop, and step from the slice
#            i.start
#            i.step
#            i.stop
#            return StateArray(t,
#                    x,
#                    d,
#                    pvt,
#                    s=None,
#                    u=None,
#                    pi=None,
#                    ci=None)
#
#        elif isinstance(key, int):
#            if key < 0:  # Handle negative indices
#                key += len(self)
#            if key >= len(self):
#                raise IndexError("The index {} is out of range.".format(key))
#            return self.getData(key)  # Get the data from elsewhere
#        else:
#            raise TypeError("Invalid argument type.")

        return StateArray(
            t=self.t[i],
            x=self.cont_states[i],
            d=self.discrete_states[i],
            pvt=self.pvt_states[i],
            s=self.controller_states[i],
            u=self.controller_outputs[i],
            pi=self.plant_extraneous_inputs[i],
            ci=self.controller_extraneous_inputs[i],
            )

    # not a good idea to return another class object! Creates issues with list
    # pseudoi indexing functionality

#        return State(self.t[i],
#                self.cont_states[i],
#                self.discrete_states[i],
#                self.pvt_states[i],
#                None,
#                self.controller_states[i],
#                None,
#                self.controller_outputs[i])

    def __setitem__(self, key, value):
        raise NotImplementedError
        i = key
        State(
            self.t[i],
            self.cont_states[i],
            self.discrete_states[i],
            self.pvt_states[i],
            None,
            self.controller_states[i],
            None,
            self.controller_outputs[i],
            )

    def __deleteitem__(self, key, value):
        raise NotImplementedError

    def __repr__(self):
        s = ''
        s += '''t_array:
{}
'''.format(self.t)
        s += '''plant_state_array
{}
'''.format(self.cont_states)
        s += '''discrete_state_array
{}
'''.format(self.discrete_states)
        s += '''pvt_state_array
{}
'''.format(self.pvt_states)
        s += '''controller_state_array
{}
'''.format(self.controller_states)
        s += '''controller_output_array
{}
'''.format(self.controller_outputs)
        s += \
            '''plant_extraneous_inputs_array
{}
'''.format(self.plant_extraneous_inputs)
        s += \
            '''controller_extraneous_inputs_array
{}
'''.format(self.controller_extraneous_inputs)
        return s


class State(object):

    def __init__(
            self,
            t,
            x,
            d,
            pvt,
            ci,
            s,
            pi,
            u,
            ):

        self.t = t  # time
        self.x = x  # continuous states
        self.d = d  # plant discrete states
        self.pvt = pvt  # plant pvt_states

#        self.e = pi # disturbance

        self.s = s  # controller states
        self.u = u  # controller output
        self.pi = pi
        self.ci = ci

    def __repr__(self):
        l = []
        l.append('t=' + str(self.t))
        l.append('x=' + str(self.x))
        l.append('d=' + str(self.d))
        l.append('pvt=' + str(self.pvt))
        l.append('ci=' + str(self.ci))
        l.append('s=' + str(self.s))
        l.append('pi=' + str(self.pi))
        l.append('u=' + str(self.u))
        return '(' + ','.join(l) + ')'
