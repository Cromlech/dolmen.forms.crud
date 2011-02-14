# -*- coding: utf-8 -*-

import doctest
import unittest
import zope.component

from dolmen.forms.crud import tests
from zope.component import eventtesting
from zope.component.interfaces import IComponentLookup
from zope.component.testlayer import ZCMLFileLayer
from zope.interface import Interface
from zope.site.folder import rootFolder
from zope.site.site import LocalSiteManager, SiteManagerAdapter
from zope.traversing.testing import setUp as traversingSetUp


class DolmenFormsCrudLayer(ZCMLFileLayer):
    """The dolmen.forms.crud main test layer.
    """

    def setUp(self):
        ZCMLFileLayer.setUp(self)
        eventtesting.setUp()
        traversingSetUp()
        zope.component.hooks.setHooks()

        # Set up site manager adapter
        zope.component.provideAdapter(
            SiteManagerAdapter, (Interface,), IComponentLookup)

        # Set up site
        site = rootFolder()
        site.setSiteManager(LocalSiteManager(site))
        zope.component.hooks.setSite(site)

    def tearDown(self):
        ZCMLFileLayer.tearDown(self)
        zope.component.hooks.resetHooks()
        zope.component.hooks.setSite()


def test_suite():
    suite = unittest.TestSuite()
    readme = doctest.DocFileSuite(
        '../README.txt', globs={'__name__': 'dolmen.forms.crud.tests'},
        optionflags=(doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE))
    readme.layer = DolmenFormsCrudLayer(tests)
    suite.addTest(readme)
    return suite
