# -*- coding: utf-8 -*-

import re
import os.path
import unittest

from pkg_resources import resource_listdir
from zope.testing import doctest, module
from zope.app.testing import functional

ftesting_zcml = os.path.join(os.path.dirname(__file__), 'ftesting.zcml')
FunctionalLayer = functional.ZCMLLayer(
    ftesting_zcml, __name__, 'FunctionalLayer', allow_teardown=True
    )

def suiteFromPackage(name):
    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = 'dolmen.forms.crud.ftests.%s.%s' % (name, filename[:-3])
        test = doctest.DocTestSuite(
            dottedname,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
            )
        test.layer = FunctionalLayer

        suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in ['adder']:
        suite.addTest(suiteFromPackage(name))
    readme = functional.FunctionalDocFileSuite('../README.txt')
    readme.layer = FunctionalLayer
    suite.addTest(readme)
    return suite
