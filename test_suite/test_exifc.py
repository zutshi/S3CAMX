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
    systems = [
        './examples/fuzzy_invp/fuzzy_invp.tst',
        './examples/heater/heater.tst',
        './examples/dc_motor/dci.tst',
        './examples/toy_model_10u/toy_model_10u.tst',
        './examples/heat/heat.tst',
        './examples/spi/spi.tst',
            ]

    for s in systems:
        one_shot_sim, prop = exifc.load_system(s)
        NUM_SIMS = 1
        x0 = sample.sample_ival_constraints(prop.init_cons, NUM_SIMS)

        w0 = sample.sample_ival_constraints(prop.ci, np.ceil(prop.T/prop.delta_t))

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
