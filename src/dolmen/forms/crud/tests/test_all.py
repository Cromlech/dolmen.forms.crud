# -*- coding: utf-8 -*-

import re
import os.path
import unittest

from zope.testing import doctest
from zope.app.testing import functional

ftesting_zcml = os.path.join(os.path.dirname(__file__), 'ftesting.zcml')
FunctionalLayer = functional.ZCMLLayer(
    ftesting_zcml, __name__, 'FunctionalLayer', allow_teardown=True
    )

def test_suite():
    suite = unittest.TestSuite()
    readme = functional.FunctionalDocFileSuite(
        '../README.txt',
        globs={'__name__': 'dolmen.forms.crud.tests'}
        )
    readme.layer = FunctionalLayer
    suite.addTest(readme)
    return suite
