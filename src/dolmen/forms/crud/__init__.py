#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory
i18n = MessageFactory("dolmen.forms.crud")

from dolmen.forms.crud.interfaces import IAdding, IFactoryAdding
from dolmen.forms.crud.actions import (
    AddAction, UpdateAction, DeleteAction, CancelAction)
from dolmen.forms.crud.components import Display, Add, Edit, Delete
