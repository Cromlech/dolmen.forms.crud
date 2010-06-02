# -*- coding: utf-8 -*-

from dolmen.forms.base import set_fields_data
from dolmen.forms.crud import ObjectInitializedEvent

from zope.event import notify
from zope.lifecycleevent import Attributes
from zope.component import getGlobalSiteManager
from zope.interface import implementedBy, providedBy


# This class will go away, with the use of dolmen.content >= 0.3
def notify_object_creation(fields, content, data):
    """Builds a list of descriptions, made of Attributes objects, defining
    the changes made on the content and the related interface.
    """
    changes = set_fields_data(fields, content, data)
    if changes:
        descriptions = []
        for interface, names in changes.items():
            descriptions.append(Attributes(interface, *names))
        notify(ObjectInitializedEvent(content, *descriptions))
        return descriptions
    return None


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
