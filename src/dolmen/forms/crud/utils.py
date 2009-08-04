# -*- coding: utf-8 -*-

import grok
from zope.interface import implementedBy, providedBy
from zope.component import queryMultiAdapter, getGlobalSiteManager


def queryClassMultiAdapter(adapts, ob, interface, name=u''):
    sm = getGlobalSiteManager()
    klass = adapts[0]
    required = implementedBy(klass)
    lookfor = (required,) + tuple(providedBy(a) for a in adapts[1:])
    factory = sm.adapters.lookup(lookfor, interface, name)
    if factory is not None:
        return factory(ob, *adapts[1:])
    return None
