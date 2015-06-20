#!/usr/bin/python
# -*- coding: utf-8 -*-
from blessings import Terminal
from progressbar import ProgressBar

import time

term = Terminal()


class Writer(object):

    """Create an object with a write method that writes to a
    specific place on the screen, defined at instantiation.

    This is the glue between blessings and progressbar.
    """

    def __init__(self, location):
        """
        Input: location - tuple of ints (x, y), the position
                        of the bar in the terminal
        """

        self.location = location

    def write(self, string):
        with term.location(*self.location):
            print string


HORIZONTAL_OFFSET = 100


class ProgBar(object):

    def __init__(self, len_list):
        self.pbar_list = []
        self.pbar_val = [0] * len(len_list)
        for i in range(len(len_list)):
            writer = Writer((HORIZONTAL_OFFSET, i + 20))
            pbar = ProgressBar(fd=writer)
            pbar.start()
            self.pbar_list.append(pbar)
        self.len_list = len_list

    def update(self, pbar_id):
        pbar = self.pbar_list[pbar_id]
        self.pbar_val[pbar_id] += 1
        val = self.pbar_val[pbar_id]

#        print val

        total_len = self.len_list[pbar_id]
        pbar.update(float(val) / float(total_len) * 100.0)


if __name__ == '__main__':
    writer1 = Writer((0, 10))
    writer2 = Writer((0, 20))

    pbar1 = ProgressBar(fd=writer1)
    pbar2 = ProgressBar(fd=writer2)

    pbar1.start()
    pbar2.start()

    for i in range(100):
        pbar1.update(i)
        pbar2.update(i)
        time.sleep(0.02)

    # pbar1.finish()
    # pbar2.finish()

# TODO: pbar.finish() is not provided!
