#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory
i18n = MessageFactory("dolmen.forms.crud")

from dolmen.forms.crud.interfaces import (
    IAdding, IFactoryAdding, IFieldsCustomization)
from dolmen.forms.crud.addview import Adder
from dolmen.forms.crud.actions import (
    AddAction, UpdateAction, DeleteAction, CancelAction)
from dolmen.forms.crud.crudforms import (
    ApplicationForm, Display, Add, Edit, Delete)
from dolmen.forms.crud.customize import FieldsCustomizer
