# -*- coding: utf-8 -*-

import doctest
import unittest
import dolmen.forms.crud
from zope.i18n.interfaces.locales import ILocale
from zope.component.testlayer import ZCMLFileLayer
from zope.component import provideAdapter
from zope.interface import Interface


def get_locale(request):
    return locales.getLocale()


class TestLayer(ZCMLFileLayer):

    def setUp(self):
        ZCMLFileLayer.setUp(self)
        provideAdapter(get_locale, (Interface,), ILocale)


def test_suite():
    suite = unittest.TestSuite()
    readme = doctest.DocFileSuite(
        'README.txt', globs={'__name__': 'dolmen.forms.crud.tests'},
        optionflags=(doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE))
    suite.addTest(readme)
    suite.layer = TestLayer(dolmen.forms.crud)
    return suite
