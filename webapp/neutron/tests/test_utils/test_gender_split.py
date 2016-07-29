#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
import sys

from neutron.utils.gender_split import gender_split


class GenderSplitTestCase(unittest.TestCase):

    def test_invalid(self):
        self.assertRaises(ValueError, gender_split, "atleta")
        self.assertRaises(ValueError, gender_split, "atleta, dos, tres")

    if sys.version_info < (3, 0):
        def assertCountEqual(self, first, second, msg=None):
            return self.assertItemsEqual(first, second, msg)

    def test_regular(self):
        self.assertCountEqual(gender_split("zafio, fia"), ("zafio", "zafia"))
        self.assertCountEqual(gender_split("zagal, la"), ("zagal", "zagala"))
        self.assertCountEqual(gender_split("ciudadrealeño, ña"), ("ciudadrealeño", "ciudadrealeña"))
        self.assertCountEqual(gender_split("cingalés, sa"), ("cingalés", "cingalesa"))
        self.assertCountEqual(gender_split("cimarrón, na"), ("cimarrón", "cimarrona"))

    def test_mery(self):
        self.assertCountEqual(gender_split("sacristán, na"), ("sacristán", "sacristana"))
        self.assertCountEqual(gender_split("saltarín, na"), ("saltarín", "saltarina"))
        self.assertCountEqual(gender_split("sirviente, ta"), ("sirviente", "sirvienta"))
        self.assertCountEqual(gender_split("danzarín, na"), ("danzarín", "danzarina"))
        self.assertCountEqual(gender_split("dios, sa"), ("dios", "diosa"))
        self.assertCountEqual(gender_split("gigante, ta"), ("gigante", "giganta"))
        self.assertCountEqual(gender_split("guardián, na"), ("guardián", "guardiana"))
        self.assertCountEqual(gender_split("jefe, fa"), ("jefe", "jefa"))
        self.assertCountEqual(gender_split("infante, ta"), ("infante", "infanta"))
        self.assertCountEqual(gender_split("alazán, na"), ("alazán", "alazana"))
        self.assertCountEqual(gender_split("alcahuete, ta"), ("alcahuete", "alcahueta"))
        self.assertCountEqual(gender_split("alemán, na"), ("alemán", "alemana"))
        self.assertCountEqual(gender_split("regordete, ta"), ("regordete", "regordeta"))
        self.assertCountEqual(gender_split("parlanchín, na"), ("parlanchín", "parlanchina"))
        self.assertCountEqual(gender_split("presidente, ta"), ("presidente", "presidenta"))
        self.assertCountEqual(gender_split("nene, na"), ("nene", "nena"))
        self.assertCountEqual(gender_split("mastín, na"), ("mastín", "mastina"))
        self.assertCountEqual(gender_split("musulmán, na"), ("musulmán", "musulmana"))
        self.assertCountEqual(gender_split("cacique, ca"), ("cacique", "cacica"))
