#!/usr/bin/env python
# -*- coding: utf-8 -*-


from random import Random


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