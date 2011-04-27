# -*- coding: utf-8 -*-

from dolmen.forms.base import Fields
from dolmen.forms.crud.interfaces import IFieldsCustomization
from zope.component import getGlobalSiteManager, queryMultiAdapter
from zope.interface import providedBy


def lookup_customization(factory, form, request):
    """This function searches the component registry for any adapter
    registered for an instance of the given class. It lookups and returns
    it correctly factored.
    """
    sm = getGlobalSiteManager()

    adapts = (form, request)
    required = factory.getInterfaces()
    
    lookfor = (required,) + tuple(providedBy(a) for a in adapts)
    adapter = sm.adapters.lookup(lookfor, IFieldsCustomization, '')
    if adapter is not None:
        return adapter(factory, *adapts)
    return None


def getAllFields(obj, *ignore):
    ifaces = tuple(providedBy(obj))
    return Fields(*ifaces).omit(*ignore)


def getFactoryFields(form, factory, *ignore):
    ifaces = factory.getInterfaces()
    if ifaces:
        fields = Fields(*ifaces).omit(*ignore)
        modifier = lookup_customization(factory, form, form.request)
        if modifier is not None:
            return modifier(fields)
        return fields
    return Fields()


def getObjectFields(form, obj, *ignore):
    fields = getAllFields(obj, *ignore)
    modifier = queryMultiAdapter(
        (obj, form, form.request), IFieldsCustomization)
    if modifier is not None:
        return modifier(fields)
    return fields
