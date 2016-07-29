#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
import unittest

from neutron.utils.gender_split import gender_split


class GenderSplitTestCase(unittest.TestCase):

    def test_invalid(self):
        self.assertRaises(ValueError, gender_split, "atleta")
        self.assertRaises(ValueError, gender_split, "atleta, dos, tres")

    def test_regular(self):
        self.assertItemsEqual(gender_split("zafio, fia"), ["zafio", "zafia"])
        self.assertItemsEqual(gender_split("zagal, la"), ["zagal", "zagala"])
        self.assertItemsEqual(gender_split("ciudadrealeño, ña"), ["ciudadrealeño", "ciudadrealeña"])
        self.assertItemsEqual(gender_split("cingalés, sa"), ["cingalés", "cingalesa"])
        self.assertItemsEqual(gender_split("cimarrón, na"), ["cimarrón", "cimarrona"])

    def test_mery(self):
        self.assertItemsEqual(gender_split("sacristán, na"), ["sacristán", "sacristana"])
        self.assertItemsEqual(gender_split("saltarín, na"), ["saltarín", "saltarina"])
        self.assertItemsEqual(gender_split("sirviente, ta"), ["sirviente", "sirvienta"])
        self.assertItemsEqual(gender_split("danzarín, na"), ["danzarín", "danzarina"])
        self.assertItemsEqual(gender_split("dios, sa"), ["dios", "diosa"])
        self.assertItemsEqual(gender_split("gigante, ta"), ["gigante", "giganta"])
        self.assertItemsEqual(gender_split("guardián, na"), ["guardián", "guardiana"])
        self.assertItemsEqual(gender_split("jefe, fa"), ["jefe", "jefa"])
        self.assertItemsEqual(gender_split("infante, ta"), ["infante", "infanta"])
        self.assertItemsEqual(gender_split("alazán, na"), ["alazán", "alazana"])
        self.assertItemsEqual(gender_split("alcahuete, ta"), ["alcahuete", "alcahueta"])
        self.assertItemsEqual(gender_split("alemán, na"), ["alemán", "alemana"])
        self.assertItemsEqual(gender_split("regordete, ta"), ["regordete", "regordeta"])
        self.assertItemsEqual(gender_split("parlanchín, na"), ["parlanchín", "parlanchina"])
        self.assertItemsEqual(gender_split("presidente, ta"), ["presidente", "presidenta"])
        self.assertItemsEqual(gender_split("nene, na"), ["nene", "nena"])
        self.assertItemsEqual(gender_split("mastín, na"), ["mastín", "mastina"])
        self.assertItemsEqual(gender_split("musulmán, na"), ["musulmán", "musulmana"])
        self.assertItemsEqual(gender_split("cacique, ca"), ["cacique", "cacica"])
