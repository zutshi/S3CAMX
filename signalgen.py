#!/usr/bin/python
# -*- coding: utf-8 -*-
import random


# All signals are discrete and simulate zoh sampler's output

def random_signal_generator(
    N,
    l,
    h,
    seed=None,
    ):
    r = random.Random()
    if seed:
        r.seed(seed)
    for i in xrange(N):
        yield l + r.random() * (h - l)


def rate_limited_random_signal_generator():
    raise NotImplementedError


