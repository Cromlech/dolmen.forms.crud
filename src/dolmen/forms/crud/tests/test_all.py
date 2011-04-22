# -*- coding: utf-8 -*-

import doctest
import unittest


def test_suite():
    suite = unittest.TestSuite()
    readme = doctest.DocFileSuite(
        '../README.txt', globs={'__name__': 'dolmen.forms.crud.tests'},
        optionflags=(doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE))
    suite.addTest(readme)
    return suite
