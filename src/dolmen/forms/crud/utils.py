# -*- coding: utf-8 -*-

from martian.util import isclass
from dolmen.content import get_schema
from dolmen.forms.crud.interfaces import IFieldsCustomization
from zeam.form.base import Fields
from zope.component import getSiteManager, queryMultiAdapter
from zope.interface import implementedBy, providedBy


def queryClassMultiAdapter(adapts, interface, factory_cls=None, name=u''):
    """This function searches the component registry for any adapter
    registered for an instance of the given class. It lookups and returns
    it correctly factored.
    """
    sm = getSiteManager()
    klass = adapts[0]

    if factory_cls is None:
        factory_cls = klass

    required = implementedBy(klass)
    lookfor = (required,) + tuple(providedBy(a) for a in adapts[1:])
    factory = sm.adapters.lookup(lookfor, interface, name)
    if factory is not None:
        return factory(factory_cls, *adapts[1:])
    return None


def getSchemaFields(form, component, *ignore):
    if isclass(component):
        lookup = queryClassMultiAdapter
    else:
        lookup = queryMultiAdapter

    ifaces = get_schema(component)
    if ifaces:
        fields = Fields(*ifaces).omit(*ignore)
        modifier = lookup((component, form, form.request),
                          IFieldsCustomization)
        if modifier is not None:
            return modifier(fields)
        return fields
    return Fields()
