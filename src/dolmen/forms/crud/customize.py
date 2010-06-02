# -*- coding: utf-8 -*-

import grokcore.component as grok
from zeam.form.base.interfaces import IFormCanvas
from dolmen.forms.crud import IFieldsCustomization


class FieldsCustomizer(grok.MultiAdapter):
    grok.baseclass()
    grok.adapts(None, IFormCanvas, None)
    grok.implements(IFieldsCustomization)

    def __init__(self, context, form, request):
        self.context = context
        self.form = form
        self.request = request

    def __call__(self, fields):
        raise NotImplementedError("""Implement your own.""")
