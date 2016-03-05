#!/usr/bin/env python
# -*- coding: utf-8 -*-


from random import Random
from scipy.stats import beta
import io
import PIL

# Import matplotlib, not to render windows: http://stackoverflow.com/questions/27147300/how-to-clean-images-in-python-django
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class RandomWeighted(Random):
    def weighted_choice(self, choices):
        total = sum(w for c, w in choices)
        r = self.uniform(0, total)
        upto = 0
        for c, w in choices:
            if upto + w >= r:
                return c
            upto += w
        assert False, "Shouldn't get here"

    def beta_ppf(self, a, b):
        return beta.ppf(self.random(), a, b)


class Histogram(object):
    def __init__(self, data, bins=25):
        self.data = data
        self.bins = bins

    def savefig(self, filename, **kwargs):
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.hist(self.data, self.bins)
        fig.suptitle(kwargs.get('title', None))
        plt.savefig(filename, **kwargs)

    def get_img_buffer(self, **kwargs):
        buffer = io.BytesIO()
        self.savefig(buffer, format='png', **kwargs)
        return buffer