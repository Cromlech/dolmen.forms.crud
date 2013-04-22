# -*- coding: utf-8 -*-

from dolmen.forms.base import Fields
from zope.interface import providedBy


def getAllFields(obj, *ignore):
    ifaces = tuple(providedBy(obj))
    return Fields(*ifaces).omit(*ignore)


def getFactoryFields(form, factory, *ignore):
    ifaces = factory.getInterfaces()
    if ifaces:
        fields = Fields(*ifaces).omit(*ignore)
        return fields
    return Fields()


def getObjectFields(form, obj, *ignore):
    fields = getAllFields(obj, *ignore)
    return fields
