###############################################################################
# File name: external_interface.py
# Author: Aditya
# Python Version: 2.7
#
#                       #### Description ####
# Provides an external interface to simulate a system described in native
# format.
# TODO: Currently provides only a one shot simulator, which can simulate the
# system between t = [0, tf].
# If desired, this can be extended to provide a simulator which can be called
# multiple times from t = [t0, tf]
###############################################################################

import loadsystem
import simulatesystem as simsys
import err

# TODO: REMOVE numpy dependance!!
import numpy as np
import logging

# start logger

FORMAT = '[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s'
FORMAT2 = '%(levelname) -10s %(asctime)s %(module)s:\
           %(lineno)s %(funcName)s() %(message)s'

logging.basicConfig(filename='log.secam', filemode='w', format=FORMAT2,
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


#TODO: no need for a full fledged class, can be something more efficient?
class SimState(object):
    def __init__(self, s=None, d=None, pvt=None):
        self.s = s
        self.d = d
        self.pvt = pvt
        return


def load_system(file_path):
    sys, prop = loadsystem.parse(file_path)
    sys.init_sims(plt_lib=None, psim_args=None)
    # useful to talk about the parameterization of ci without talking about
    # delta_t
    prop.delta_t = sys.delta_t
    #step_sim = simsys.get_step_simulator(
    #    sys.controller_sim,
    #    sys.plant_sim,
    #    sys.delta_t)
    #trace = sim(py_x, t0, tf, py_u, pvt);

    #system_sim = simsys.get_system_simulator(step_sim, sys.delta_t, sys.num_dims)

    system_sim = simsys.get_system_simulator(sys)

    # simstate encapsulates pvt, s, d,
    def one_shot_sim(x, t0, tf, w, simstate=None):
        if t0 != 0:
            raise err.Fatal('t0 must be 0!')
        else:
            # TODO: construct numpy arrays in loadsystem
            # This will require changing code into quite  afew
            # places...carefull!
            s = np.array(prop.initial_controller_state)
            d = np.array(prop.initial_discrete_state)
            pvt = np.zeros(1)
            ci_array = w
            return system_sim(x, s, d, pvt, t0, tf, ci_array)

    return one_shot_sim, prop
