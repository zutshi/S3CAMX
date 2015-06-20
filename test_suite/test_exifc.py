###############################################################################
# File name: test_exifc.py
# Author: Aditya
# Python Version: 2.7
#
#                       #### Description ####
# Test system loading and simulation using external_interface.py
###############################################################################

import matplotlib
# Force GTK3 backend. By default GTK2 gets loaded and conflicts with
# graph-tool
matplotlib.use('GTK3Agg')
#global plt
import matplotlib.pyplot as plt
import numpy as np
import time

import external_interface as exifc
import sample
import traces


# TODO: test all examples using the examplel isting
def main():
    example_list = []
    one_shot_sim, prop = exifc.load_system('./examples/heater_float/heater.tst')
    example_list.append((one_shot_sim, prop))
    one_shot_sim, prop = exifc.load_system('./examples/dc_motor_float/dci.tst')
    example_list.append((one_shot_sim, prop))
    one_shot_sim, prop = exifc.load_system('./examples/toy_model_10u/toy_model_10u.tst')
    example_list.append((one_shot_sim, prop))
    #one_shot_sim, prop = exifc.load_system('./examples/heater/heater.tst')
    #one_shot_sim, prop = exifc.load_system('./examples/dc_controller_hand_coded_input/dci.tst')

    for example in example_list:
        one_shot_sim, prop = example
        NUM_SIMS = 1
        x0 = sample.sample_ival_constraints(prop.init_cons, NUM_SIMS)

        w0 = sample.sample_ival_constraints(prop.ci, np.ceil(prop.T/prop.ci_zoh_time))

        trace_list = []
        tic = time.time()
        for i in xrange(NUM_SIMS):
            trace = one_shot_sim(x0[i], 0.0, prop.T, w0)
            trace_list.append(trace)
        toc = time.time()
        print 'time taken for simulations: {}s'.format(toc-tic)
        traces.plot_trace_list(trace_list, plt)

if __name__ == '__main__':
    main()
