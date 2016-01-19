#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
traces.py
----------
Defines traces or trajectories of the system. Used only for plotting
as of now.
'''

import numpy as np
from scipy import io

## commented off because matplotlib is not installed for python installation
## used with matlab
#import matplotlib
## Force GTK3 backend. By default GTK2 gets loaded and conflicts with
## graph-tool
#matplotlib.use('GTK3Agg')
#global plt
#import matplotlib.pyplot as plt


class Trace(object):

    def __init__(self, num_dims, num_points):
        self.idx = 0
        self.t_array = np.empty(num_points)
        self.x_array = np.empty((num_points, num_dims.x))
        self.s_array = np.empty((num_points, num_dims.s))
        self.u_array = np.empty((num_points, num_dims.u))
        self.d_array = np.empty((num_points, num_dims.d))
        self.ci = np.empty((num_points, num_dims.ci))
        self.pi = np.empty((num_points, num_dims.pi))

    def append(
            self,
            s=None,
            u=None,
            x=None,
            ci=None,
            pi=None,
            t=None,
            d=None,
            ):
        #if s is None or u is None or r is None or x is None or ci is None \
        #    or pi is None or t is None or d is None:
        #    raise err.Fatal('one of the supplied arguement is None')

        i = self.idx
        self.t_array[i] = t
        self.x_array[i, :] = x
        self.s_array[i, :] = s
        self.u_array[i, :] = u
        self.ci[i, :] = ci
        self.pi[i, :] = pi
        self.idx += 1

#########################################
# replacement for plot_trace_list()
#########################################
# TODO: unfinished function...
# Need to take care of matplotlib format and test the function!!
    def plot(self, plot_cmd):
        raise NotImplementedError
        parsed_plot_cmd = None
        while(parsed_plot_cmd is None):
            plot_cmd = get_plot_cmd_from_stdin()
            parsed_plot_cmd = parse_plot_cmd(plot_cmd)

        x, y = parsed_plot_cmd
        plt.plot(x, y)

#         ###### used to generate heater plots for the rtss paper##############
#         plt.rc('text', usetex=True)
#         plt.rc('font', family='serif')
#         plt.title(r'Room-Heater-Thermostat: Random Simulations',fontsize=30)
#         plt.xlabel(r'Time (s)',fontsize=28)
#         plt.ylabel(r'Room Temp. ($^\circ$F)',fontsize=28)
#         plt.plot([0, 10], [76, 76], 'r-', lw=2)
#         plt.plot([0, 10], [52, 52], 'r-', lw=2)
#         #####################################################################

    # plt.figure()
    # AC = plt.gca()
    # plt.title('ci')

        #   AX_list[i+1].plot(x_array[:, 0], x_array[:, 1])

        # plt_x1 = AX1.plot(t_array, x_array[:, 1], label='x1')
        # plt_x2 = AX2.plot(t_array, x_array[:, 2], label='x2')
        # plt_x0x1 = AX0X1.plot(x_array[:, 0], x_array[:, 1], label='x0x1')

        # #plt_s0 = plt.plot(t_array, trace.s_array[:, 0], label='err')
        # plt_s1 = plt.plot(t_array, trace.s_array[:, 1], label='ref')
        # plt_u = AU.plot(t_array, trace.u_array[:, 0], label='u')
        # plt_ci = AC.plot(t_array, trace.ci[:, 0], label='ci')
        # print trace.s_array
        # plt.legend()
        # plt.legend([plt_x0, plt_x1, plt_s0, plt_s1], ['x0', 'x1', 's0', 's1'])
    # plt.plot(t_array, ref_signal, drawstyle='steps-post')
    # plt.autoscale()
        plt.show()

    def dump_matlab(self):
        data = {'T': self.t_array,
                'X': self.x_array,
                'S': self.s_array,
                'U': self.u_array,
                'CI': self.ci,
                'PI': self.pi}
        io.savemat('mat_file.mat', data, appendmat=False, format='5',
                   do_compression=False, oned_as='column')


    def __repr__(self):
        s = '''t
, {}, x
{}, s
{}, u
{}, ci
{}, pi
{}'''.format(
            self.t_array,
            self.x_array,
            self.s_array,
            self.u_array,
            self.ci,
            self.pi,
            )
        return s


def parse_plot_cmd(plot_cmd, trace_obj):
    if len(plot_cmd) != 4:
        print 'plot command NOT of length 4: {}'.format(plot_cmd)
        return None
    x_axis_str, x_idx, y_axis_str, y_idx = plot_cmd
    try:
        x_axis = getattr(trace_obj, x_axis_str)
        y_axis = getattr(trace_obj, y_axis_str)
    except AttributeError, e:
        print 'unexpected plot command received: {}'.format(plot_cmd)
        print e
        return None
    x_idx = int(x_idx)
    y_idx = int(y_idx)
    try:
        if x_axis_str != 't':
            x = x_axis[x_idx, :]
    except:
        print 'unexpected indices for the first var: {}'.format(plot_cmd)
        return None
    try:
        if y_axis_str != 't':
            y = y_axis[y_idx, :]
    except:
        print 'unexpected indices for the second var: {}'.format(plot_cmd)
        return None

    return x, y


def get_plot_cmd_from_stdin():
    plot_cmd_format = \
        '''########### plot command format ########## \n
           [t,x,s,u,ci,pi][0-n][t,x,s,u,ci,pi][0-n]   \n
           e.g. (a) phase plot,    x[1] vs x[0]: x0x1 \n
                (b) state vs time, t    vs x[0]: t0x0 \n
           ########################################## \n'''
    print plot_cmd_format
    corrected_plot_cmd = raw_input('please type the correct command:')
    return corrected_plot_cmd


def plot_trace_list(trace_list, plt, plot_figure_for_paper=False):
    '''
    @type plt: matplotlib.pyplot
    '''

    # plot for each plant state
    # NUM_PLOTS = num_dims.x+1

    # plot all continuous plant states against time
    NUM_PLOTS = trace_list[0].x_array.shape[1]
#     AX_list = []
    #plt.figure()
    #AX0X1 = plt.gca()

#     for i in range(NUM_PLOTS):
#         plt.figure()
#         ax = plt.gca()
#         AX_list.append(ax)
#         plt.title('x{}'.format(i))



#     for trace in trace_list:
#         x_array = trace.x_array
#         t_array = trace.t_array

#         # plt_x0 = AX0.plot(t_array, x_array[:, 10], label='x10')
#         for i in range(NUM_PLOTS):
#             AX_list[i].plot(t_array, x_array[:, i])

#         #plt_x0x1 = AX0X1.plot(x_array[:, 0], x_array[:, 1], label='x0x1')

#         # plt.legend([plt_x0, plt_x1, plt_s0, plt_s1], ['x0', 'x1', 's0', 's1'])

#     # plt.plot(t_array, ref_signal, drawstyle='steps-post')
#     # plt.autoscale()
#     plt.show()

    if plot_figure_for_paper:
        # count num of plotted sims
        ctr_total = 0
        import plothelper as ph
        line_list = []
        for i in range(NUM_PLOTS):
            plt.figure()
            ax = plt.gca()
            plt.title('x{}'.format(i))
            for trace in trace_list:
                x_array = trace.x_array
                t_array = trace.t_array
                if not (x_array[0, i] <= 70.0 and x_array[0, i] >= 69.9):
                    # select to plot with probability 20%
                    if np.random.random() >= 0.05:
                        continue
                line, = ax.plot(t_array, x_array[:, i])
                line_list.append(line)
                ctr_total += 1
            print('plotted {} sims'.format(ctr_total))
            ph.figure_for_paper(ax, line_list)
    else:
        for i in range(NUM_PLOTS):
            plt.figure()
            ax = plt.gca()
            plt.title('x{}'.format(i))
            for trace in trace_list:
                x_array = trace.x_array
                t_array = trace.t_array
                ax.plot(t_array, x_array[:, i])
            plt.show()
