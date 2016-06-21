#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np


def rectangle(fig, cons, fc):
    xidx = 0
    yidx = 1
    verts = [(cons.l[xidx], cons.l[yidx]), (cons.l[xidx], cons.h[yidx]),
             (cons.h[xidx], cons.h[yidx]), (cons.h[xidx], cons.l[yidx]), (0.0,
             0.0)]  # left, bottom
                    # left, top
                    # right, top
                    # right, bottom
                    # ignored

#    verts = [
#        (center[0] - e[0], center[1] - e[1]),  # left, bottom
#        (center[0] - e[0], center[1] + e[1]),  # left, top
#        (center[0] + e[0], center[1] + e[1]),  # right, top
#        (center[0] + e[0], center[1] - e[1]),  # right, bottom
#        (0., 0.), # ignored
#        ]

    codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO,
             Path.CLOSEPOLY]

    path = Path(verts, codes)

#    fig = plt.figure()

    ax = fig.add_subplot(111)
    patch = patches.PathPatch(path, facecolor=fc, lw=2)

#    plt.gca(fig)

    ax.add_patch(patch)

#    ax.set_xlim(-10,10)
#    ax.set_ylim(-10,10)

    return


def draw_arrow(fig, coord1, coord2):
    xidx = 0
    yidx = 1
    ax = fig.add_subplot(111)
    ax.arrow(
        coord1[xidx],
        coord1[yidx],
        coord2[xidx] - coord1[xidx],
        coord2[yidx] - coord1[yidx],
        head_width=0.01,
        head_length=0.01,
        fc='k',
        ec='k',
        )
    return


# ##### used to generate heater plots for the rtss paper##############
def figure_for_paper(ax, line_list):
    #p = spi_params()
    p = heater_params()
    p.pretty_plot(ax, line_list)
    return


def spi_params():
    p = PlotParams()
    p.filepath = '/home/zutshi/work/RA/cpsVerification/HyCU/papers/mining_djikstra/hscc_2016/spi_new'
    # Font sizes
    p.title = r'SPI: Symbolic Execution'
    p.xlabel = r'Time (s)'
    p.ylabel = r'$x$'
    p.xlim = [0, 50]
    p.ylim = [-30, 25]

    def plot_prop():
        #plot max min temp
        plt.plot([0, 50], [20, 20], 'r-', lw=2)

    p.prop_fun = plot_prop()
    return p


# To generate HSCC 2016 fig, execute secam with :
# ./secam.py -f ./examples/heater/heater.tst -s # 2000 -p --seed 1
def heater_params():
    p = PlotParams()
    p.filepath = '/home/zutshi/work/RA/cpsVerification/HyCU/papers/mining_djikstra/hscc_2016/heater_100'
    # Font sizes
    p.title = r'Room-Heater-Thermostat: Random Simulations'
    p.xlabel = r'Time (s)'
    p.ylabel = r'Room Temp. ($^\circ$F)'
    p.yticks = np.array([50, 52, 55, 60, 65, 70, 75])
    p.xlim = [0, 10]
    p.ylim = [50, 80]

    def plot_prop():
        #plot max min temp
        plt.plot([0, 10], [52, 52], 'r-', lw=2)

    p.prop_fun = plot_prop
    return p


class PlotParams(object):
    def __init__(self):
        self.filepath = None
        self.title_size = 20
        self.label_szie = 18
        self.major_tick_size = 14
        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.labelpad = 20
        self.linecolor = 'blue'
        self.linewidth = 1
        self.xticks = None
        self.yticks = None
        self.xlim = None
        self.ylim = None
        self.prop_fun = None

    def pretty_plot(self, ax, line_list):
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        plt.title(self.title, fontsize=self.title_size)
        # change font sizes for the labels and also set padding
        # between the plots and the label; else they are too close.
        plt.xlabel(self.xlabel, fontsize=self.label_szie, labelpad=self.labelpad)
        plt.ylabel(self.ylabel, fontsize=self.label_szie, labelpad=self.labelpad)

        # set custom Title position; originally the title is too close
        # to the plot.
        ttl = ax.title
        ttl.set_position([0.5, 1.05])

        if self.prop_fun:
            self.prop_fun()

        # change tick fonts
        plt.tick_params(axis='both', which='major', labelsize=self.major_tick_size)
        #plt.tick_params(axis='both', which='minor', labelsize=1)

        # specify ticks explicitly
        if self.yticks is not None:
            plt.yticks(self.yticks)
        if self.xticks is not None:
            plt.xticks(self.xticks)

        # set axes range
        if self.xlim is not None:
            ax.set_xlim(self.xlim)
        if self.ylim is not None:
            ax.set_ylim(self.ylim)
        #fig.tight_layout()
        #####################################################################

        for line in line_list:
            line.set_color(self.linecolor)
            line.set_linewidth(self.linewidth)
    #     for trace in trace_list:
    #         x_array = trace.x_array
    #         t_array = trace.t_array
    #         ax.plot(t_array, x_array[:, idx], 'b-', lw=1)


#       fig = plt.gcf()
#       plt.show()  # replaces current figure with a new blank
#       figure and savefig saves a blank figure.
#       Hence. should be using fig.savefig(), but for some reasons, it
#       ignores bbox_inches='tight'. Need to investigate further!
        ans = raw_input('save images?(no?): ')
        if ans.lower() != 'no':
            print('saving png...')
            plt.savefig(self.filepath+'.png', bbox_inches='tight')
            print('saving pdf...')
            plt.savefig(self.filepath+'.pdf', bbox_inches='tight')
        plt.show()
