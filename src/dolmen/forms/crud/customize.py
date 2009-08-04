# -*- coding: utf-8 -*-

import grokcore.component as grok
from dolmen.forms.crud import IForm, IFieldsCustomization
from zope.interface import Interface


class FieldsCustomizer(grok.MultiAdapter):
    grok.baseclass()
    grok.adapts(Interface, IForm, Interface)
    grok.implements(IFieldsCustomization)

    def __init__(self, context, form, request):
        self.context = context
        self.form = form
        self.request = request
    
    def __call__(self, fields):
        raise NotImplementedError("""Implement your own.""")
