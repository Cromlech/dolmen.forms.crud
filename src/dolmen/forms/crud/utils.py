# -*- coding: utf-8 -*-

from zope.component import getGlobalSiteManager
from zope.interface import implementedBy, providedBy


def queryClassMultiAdapter(adapts, ob, interface, name=u''):
    """This function searches the component registry for any adapter
    registered for an instance of the given class. It lookups and returns
    it correctly factored.
    """
    sm = getGlobalSiteManager()
    klass = adapts[0]
    required = implementedBy(klass)
    lookfor = (required,) + tuple(providedBy(a) for a in adapts[1:])
    factory = sm.adapters.lookup(lookfor, interface, name)
    if factory is not None:
        return factory(ob, *adapts[1:])
    return None
