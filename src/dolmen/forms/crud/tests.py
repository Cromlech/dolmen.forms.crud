# -*- coding: utf-8 -*-

import doctest
import unittest
from zope.component.eventtesting import setUp


def test_suite():
    suite = unittest.TestSuite()
    readme = doctest.DocFileSuite(
        'README.txt', globs={'__name__': 'dolmen.forms.crud.tests'},
        setUp=setUp,
        optionflags=(doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE))
    suite.addTest(readme)
    return suite
