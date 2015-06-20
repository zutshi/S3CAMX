#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches


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


